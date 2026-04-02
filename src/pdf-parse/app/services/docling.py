from io import BytesIO

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.io import DocumentStream
from fastapi import HTTPException, UploadFile

# from app.schemas.extract import ExtractionResponse
from app.schemas.extract import (
    BaseMeta,
    BoundingBox,
    CoordOriginEnum,
    ExtractionResponse,
    GroupTypeEnum,
    KVGroup,
    ListGroup,
    Page,
    PageMeta,
    ParsedGroups,
    ParsedTable,
    ParseSectionHeader,
    TableRow,
    TableRowMeta,
)
from app.services.provider import ExtractionProvider


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

    def parse_section_headers(self, texts: list) -> dict[str, list[ParseSectionHeader]]:
        output = {}
        try:
            for text in texts:
                label = text.get("label", "")
                if label == "section_header":
                    meta = text.get("prov", [{}])[0]
                    bbox = meta.get("bbox", {})
                    page_no = str(meta.get("page_no", -1))
                    section_header_bbox = BoundingBox(
                        left=bbox.get("l", -1),
                        top=bbox.get("t", -1),
                        bottom=bbox.get("b", -1),
                        right=bbox.get("r", -1),
                        coord_origin=bbox.get(
                            "coord_origin", CoordOriginEnum.BOTTOMLEFT
                        ),
                    )
                    section_header_output = ParseSectionHeader(
                        data=text.get("text", ""),
                        meta=BaseMeta(bbox=section_header_bbox, page_number=page_no),
                    )
                    output_for_page = output.get(page_no, [])
                    output_for_page.append(section_header_output)
                    output[page_no] = output_for_page

        except Exception as e:
            print("Failed to parse section headers")
            print(e)
        return output

    def parse_groups(self, groups: list, texts: list) -> dict[str, ParsedGroups]:
        output: dict[str, ParsedGroups] = {}
        try:
            for group in groups:
                # each group has a label mentioning if the group is a
                # 1) key_value_area: an alternating pair of keys and values
                # 2) list: Just a string of texts
                label = group.get("label", "list")
                parsed_kv_group = {}
                parsed_list_group = []
                temp_key = ""
                page_no = -1
                group_children = group.get("children", [])
                is_kv_pair = (
                    label == GroupTypeEnum.KVArea and len(group_children) % 2 == 0
                )
                for index, child in enumerate(group_children):
                    child_ref = str(child.get("$ref", ""))
                    if "texts" in child_ref:
                        text_index = int(child_ref.split("/")[2])
                        text_obj = texts[text_index]
                        final_text = text_obj.get("text", "")
                        if page_no == -1:
                            meta = text_obj.get("prov", [{}])[0]
                            page_no = meta.get("page_no", -1)
                        if is_kv_pair:
                            if index % 2 == 0:
                                temp_key = final_text
                            else:
                                parsed_kv_group[temp_key] = final_text
                        else:
                            parsed_list_group.append(final_text)

                group_output = None
                if parsed_kv_group:
                    group_output = KVGroup(data=parsed_kv_group)
                if parsed_list_group:
                    group_output = ListGroup(data=parsed_list_group)

                if page_no > -1 and group_output:
                    key = str(page_no)
                    if not output.get(key, []):
                        output[key] = ParsedGroups(
                            meta=BaseMeta(page_number=key), data=[group_output]
                        )
                    else:
                        output[key].data.append(group_output)
        except Exception as e:
            print("group parsing failed")
            print(e)

        return output

    def parse_tables(self, tables) -> dict[str, list[ParsedTable]]:
        output = {}
        try:
            for table in tables:
                meta = table.get("prov", [{}])[0]
                table_data = table.get("data", {})
                page_no = str(meta.get("page_no", -1))
                output_for_page = output.get(page_no, [])
                table_meta = BaseMeta(page_number=page_no)
                table_output = ParsedTable(meta=table_meta, data=[])
                for index, grid in enumerate(table_data.get("grid", [])):
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
                        cell_data = cell.get("text", "")
                        if cell_data:
                            cell_bbox = cell.get("bbox", {})
                            if table_row_meta.row_section is None:
                                table_row_meta.row_section = cell.get(
                                    "row_section", False
                                )
                            if table_row_meta.row_header is None:
                                table_row_meta.row_header = cell.get(
                                    "row_header", False
                                )
                            if table_row_meta.column_header is None:
                                table_row_meta.column_header = cell.get(
                                    "column_header", False
                                )
                            table_row.data.append(cell_data)
                            # To get the bounding box of the row, we need to collate the
                            # boxes of each cell in a row. We take min of left and top
                            # coords and max of bottom and right coords
                            row_bbox.left = min(row_bbox.left, cell_bbox.get("l", -1))
                            row_bbox.top = min(row_bbox.top, cell_bbox.get("t", -1))
                            row_bbox.right = max(row_bbox.right, cell_bbox.get("r", -1))
                            row_bbox.bottom = max(
                                row_bbox.bottom, cell_bbox.get("b", -1)
                            )
                    table_row_meta.bbox = row_bbox
                    table_output.data.append(table_row)
                output_for_page.append(table_output)
                output[page_no] = output_for_page
        except Exception as e:
            print("table parsing failed")
            print(e)
        return output

    # TODO: replace return type from dict to ExtractionResponse once mapping is fixed
    async def extract(self, file: UploadFile) -> dict:
        if file.size is None or file.filename is None:
            raise HTTPException(404, "Please use a valid file")
        if file.size > 5 * 1024 * 1024:
            raise HTTPException(413, "Please use files under 5 MB")
        content = await file.read()
        stream = DocumentStream(name=file.filename or "", stream=BytesIO(content))
        result = self.converter.convert(stream)
        doc = result.document
        # TODO: fix the mapping to the response object
        # return ExtractionResponse(pages=doc.pages, tables=doc.tables)
        return doc.export_to_dict()

    async def normalise_extraction(
        self, raw_extraction_data: dict
    ) -> ExtractionResponse:
        output = ExtractionResponse()
        try:
            pages = raw_extraction_data.get("pages", {})
            groups = raw_extraction_data.get("groups", [])
            texts = raw_extraction_data.get("texts", [])
            tables = raw_extraction_data.get("tables", [])
            groups = self.parse_groups(groups, texts)
            section_headers = self.parse_section_headers(texts)
            tables = self.parse_tables(tables)
            for key, values in pages.items():
                skip_key = True
                str_page_no = str(key)
                page_output = Page(
                    meta=PageMeta(
                        size=values.get("size", {}),
                        page_number=key,
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
        except Exception as e:
            print("Failed to normalise output")
            print(e)
        return output
