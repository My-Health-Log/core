import io
from docling.datamodel.base_models import DocumentStream, InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from fastapi import UploadFile

# from app.schemas.extract import ExtractionResponse
from app.services.provider import ExtractionProvider


class DoclingExtractionProvider(ExtractionProvider):
    def __init__(self):
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = False
        pipeline_options.do_table_structure = True
        pipeline_options.generate_picture_images = False  # disables image extraction

        self.converter = DocumentConverter(
            allowed_formats=[InputFormat.PDF],
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            },
        )

    # TODO: replace return type from dict to ExtractionResponse once mapping is fixed
    async def extract(self, file: UploadFile) -> dict:
        if file.size is None or file.filename is None:
            raise FileNotFoundError
        if file.size > 50 * 1024 * 1024:
            raise MemoryError
        content = await file.read()
        stream = DocumentStream(name=file.filename or "", stream=io.BytesIO(content))
        result = self.converter.convert(stream)
        doc = result.document
        # TODO: fix the mapping to the response object
        # return ExtractionResponse(pages=doc.pages, tables=doc.tables)
        return doc.export_to_dict()
