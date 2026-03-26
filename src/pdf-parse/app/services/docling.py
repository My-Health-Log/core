from io import BytesIO

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.io import DocumentStream
from fastapi import HTTPException, UploadFile

# from app.schemas.extract import ExtractionResponse
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

    def parse_section_headers(self, texts: list) -> dict[str, list]:
        output = {}
        try:
            for text in texts:
                label = text.get("label", "")
                if label == "section_header":
                    meta = text.get("prov", [{}])[0]
                    page_no = str(meta.get("page_no", -1))
                    output_for_page = output.get(page_no, [])
                    if not output_for_page:
                        output_for_page = []
                    output_for_page.append(text.get("text", []))
                    output[page_no] = output_for_page

        except Exception as e:
            print("Failed to parse section headers")
            print(e)
        print(output)
        return output

    def parse_groups(self, groups: list, texts: list) -> dict[str, dict | list]:
        output = {}
        try:
            for group in groups:
                ref = group.get("self_ref", "#")
                # each group has a label mentioning if the group is a
                # 1) key_value_area: an alternating pair of keys and values
                # 2) list: Just a string of texts
                label = group.get("label", "list")
                parse_dict = {}
                parse_list = []
                temp_key = ""
                page_no = -1
                group_children = group.get("children", [])
                is_kv_pair = label == "key_value_area" and len(group_children) % 2 == 0
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
                                parse_dict[temp_key] = final_text
                        else:
                            parse_list.append(final_text)

                group_output = {}
                if parse_dict:
                    group_output["key_value_area"] = parse_dict
                if parse_list:
                    group_output["list"] = parse_list

                if page_no > -1:
                    key = str(page_no)
                    if not output.get(key, []):
                        output[key] = [group_output]
                    else:
                        output[key].append(group_output)
                else:
                    print("page number not found: ", ref)
        except Exception as e:
            print("group parsing failed")
            print(e)
        finally:
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

    async def normalise_extraction(self, raw_extraction_data: dict) -> dict:
        groups = []
        pages = {}
        output = {}
        try:
            pages = raw_extraction_data.get("pages", {})
            groups = raw_extraction_data.get("groups", [])
            texts = raw_extraction_data.get("texts", [])
            groups = self.parse_groups(groups, texts)
            section_headers = self.parse_section_headers(texts)
            for key, values in pages.items():
                skip_key = True
                str_key = str(key)
                page_output = {}
                page_output["meta"] = values
                if str_key in section_headers:
                    skip_key = False
                    page_output["section_headers"] = section_headers.get(str_key, [])
                if str_key in groups:
                    skip_key = False
                    page_output["groups"] = groups.get(str_key, [])
                if not skip_key:
                    output[str_key] = page_output
        except Exception as e:
            print("Failed to normalise output")
            print(e)
        return {"output": output}
