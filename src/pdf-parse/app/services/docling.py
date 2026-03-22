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

    async def normalise_extraction(self, rawFile: dict) -> dict:
        print(rawFile)
        return {}
