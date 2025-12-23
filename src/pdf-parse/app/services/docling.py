import io

from docling.datamodel.base_models import DocumentStream
from docling.document_converter import DocumentConverter
from fastapi import UploadFile

# from app.schemas.extract import ExtractionResponse
from app.services.provider import ExtractionProvider


class DoclingExtractionProvider(ExtractionProvider):
    def __init__(self):
        self.converter = DocumentConverter()

    # TODO: replace return type from dict to ExtractionResponse once mapping is fixed
    async def extract(self, file: UploadFile) -> dict:
        content = await file.read()
        stream = DocumentStream(name=file.filename, stream=io.BytesIO(content))
        result = self.converter.convert(stream)
        doc = result.document
        # TODO: fix the mapping to the response object
        # return ExtractionResponse(pages=doc.pages, tables=doc.tables)
        return doc.export_to_dict()
