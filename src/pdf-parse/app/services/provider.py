from fastapi import UploadFile
from abc import ABC, abstractmethod
from app.schemas.extract import ExtractionResponse


class ExtractionProvider(ABC):
    @abstractmethod
    async def extract(self, file: UploadFile) -> ExtractionResponse:
        pass


def get_provider() -> ExtractionProvider:
    from app.services.docling import DoclingExtractionProvider

    return DoclingExtractionProvider()
