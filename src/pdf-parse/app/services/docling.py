import asyncio
import logging
from io import BytesIO

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc.document import (
    DoclingDocument,
    TableItem,
)
from docling_core.types.doc.labels import DocItemLabel
from docling_core.types.io import DocumentStream
from fastapi import HTTPException, UploadFile

# from app.schemas.extract import ExtractionResponse
from app.schemas.docling import DoclingGroups, DoclingTexts
from app.schemas.extract import (
    BaseMeta,
    BoundingBox,
    CoordOriginEnum,
    ExtractionResponse,
    GroupTypeEnum,
    Page,
    PageMeta,
    PageSize,
    ParsedGroups,
    ParsedKVGroup,
    ParsedListGroup,
    ParsedTable,
    ParseSectionHeader,
    TableRow,
    TableRowMeta,
)
from app.services.provider import ExtractionProvider

logger = logging.getLogger("uvicorn")


class DoclingExtractionProvider(ExtractionProvider):
    def __init__(self):
        pipeline_options = PdfPipelineOptions()
        # assumes the the PDF is text based and not images
        pipeline_options.do_ocr = False
        pipeline_options.do_table_structure = True
        # disables image extraction
        pipeline_options.generate_picture_images = False

        self.converter = DocumentConverter(
            allowed_formats=[InputFormat.PDF],
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            },
        )

    def parse_section_headers(
        self, texts: DoclingTexts
    ) -> dict[str, list[ParseSectionHeader]]:
        output = {}
        for text in texts:
            label = text.label
            if label == DocItemLabel.SECTION_HEADER:
                meta = text.prov[0]
                bbox = meta.bbox
                page_no = str(meta.page_no)
                section_header_bbox = BoundingBox(
                    left=bbox.l,
                    top=bbox.t,
                    bottom=bbox.b,
                    right=bbox.r,
                    coord_origin=CoordOriginEnum(value=bbox.coord_origin.value),
                )
                section_header_output = ParseSectionHeader(
                    data=text.text,
                    meta=BaseMeta(bbox=section_header_bbox, page_number=page_no),
                )
                output_for_page = output.get(page_no, [])
                output_for_page.append(section_header_output)
                output[page_no] = output_for_page
        return output

    def parse_groups(
        self, groups: DoclingGroups, texts: DoclingTexts
    ) -> dict[str, ParsedGroups]:
        output: dict[str, ParsedGroups] = {}
        for group in groups:
            # each group has a label mentioning if the group is a
            # 1) key_value_area: an alternating pair of keys and values
            # 2) list: Just a string of texts
            label = group.label
            parsed_kv_group = {}
            parsed_list_group = []
            temp_key = ""
            page_no = -1
            group_children = group.children
            is_kv_pair = label == GroupTypeEnum.KVArea and len(group_children) % 2 == 0
            for index, child in enumerate(group_children):
                child_ref = str(child.cref)
                if "texts" in child_ref:
                    text_index = int(child_ref.split("/")[2])
                    text_obj = texts[text_index]
                    final_text = text_obj.text
                    if page_no == -1:
                        meta = text_obj.prov[0]
                        page_no = meta.page_no
                    if is_kv_pair:
                        if index % 2 == 0:
                            temp_key = final_text
                        else:
                            parsed_kv_group[temp_key] = final_text
                    else:
                        parsed_list_group.append(final_text)

            group_output = None
            if parsed_kv_group:
                group_output = ParsedKVGroup(data=parsed_kv_group)
            if parsed_list_group:
                group_output = ParsedListGroup(data=parsed_list_group)

            if page_no > -1 and group_output:
                key = str(page_no)
                if not output.get(key, []):
                    output[key] = ParsedGroups(
                        meta=BaseMeta(page_number=key), data=[group_output]
                    )
                else:
                    output[key].data.append(group_output)

        return output

    def parse_tables(self, tables: list[TableItem]) -> dict[str, list[ParsedTable]]:
        output = {}
        for table in tables:
            meta = table.prov[0]
            table_data = table.data
            page_no = str(meta.page_no)
            output_for_page = output.get(page_no, [])
            table_meta = BaseMeta(page_number=page_no)
            table_output = ParsedTable(meta=table_meta, data=[])
            for index, grid in enumerate(table_data.grid):
                row_number = index
                row_bbox = BoundingBox(
                    left=float("inf"),
                    top=float("inf"),
                    right=float("-inf"),
                    bottom=float("-inf"),
                    coord_origin=CoordOriginEnum.TOPLEFT,
                )
                table_row_meta = TableRowMeta(bbox=row_bbox, raw_row_idx=row_number)
                table_row = TableRow(meta=table_row_meta, data=[])
                for cell in grid:
                    cell_data = cell.text
                    cell_bbox = cell.bbox
                    if cell_data and cell_bbox:
                        if table_row_meta.row_section is None:
                            table_row_meta.row_section = cell.row_section
                        if table_row_meta.row_header is None:
                            table_row_meta.row_header = cell.row_header
                        if table_row_meta.column_header is None:
                            table_row_meta.column_header = cell.column_header
                        table_row.data.append(cell_data)
                        # To get the bounding box of the row, we need to collate the
                        # boxes of each cell in a row. We take min of left and top
                        # coords and max of bottom and right coords
                        row_bbox.left = min(row_bbox.left, cell_bbox.l)
                        row_bbox.top = min(row_bbox.top, cell_bbox.t)
                        row_bbox.right = max(row_bbox.right, cell_bbox.r)
                        row_bbox.bottom = max(row_bbox.bottom, cell_bbox.b)
                table_row_meta.bbox = row_bbox
                table_output.data.append(table_row)
            output_for_page.append(table_output)
            output[page_no] = output_for_page
        return output

    async def extract(self, file: UploadFile) -> ExtractionResponse:
        if file.size is None or file.filename is None:
            raise HTTPException(400, "Please use a valid file")
        if file.size > 5 * 1024 * 1024:
            raise HTTPException(413, "Please use files under 5 MB")
        content = await file.read()
        stream = DocumentStream(name=file.filename or "", stream=BytesIO(content))
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, self.converter.convert, stream)
        doc = result.document
        return await self.normalise_extraction(doc)

    async def normalise_extraction(
        self, raw_extraction_data: DoclingDocument
    ) -> ExtractionResponse:
        output = ExtractionResponse()
        # extract objects from the docling document
        pages = raw_extraction_data.pages
        groups = raw_extraction_data.groups
        texts = raw_extraction_data.texts
        tables = raw_extraction_data.tables

        # parse raw objects to ExtractionResponse format
        groups = self.parse_groups(groups, texts)
        section_headers = self.parse_section_headers(texts)
        tables = self.parse_tables(tables)

        # loop through the pages to create output object
        for key, values in pages.items():
            skip_key = True
            str_page_no = str(key)
            page_size = PageSize(
                width=values.size.width,
                height=values.size.height,
            )
            page_output = Page(
                meta=PageMeta(
                    size=page_size,
                    page_number=str_page_no,
                )
            )
            if str_page_no in section_headers:
                skip_key = False
                page_output.section_headers = section_headers.get(str_page_no, [])
            if str_page_no in groups:
                skip_key = False
                page_output.groups = groups.get(str_page_no, None)
            if str_page_no in tables:
                skip_key = False
                page_output.tables = tables.get(str_page_no, [])
            if not skip_key:
                output[str_page_no] = page_output
        return output
