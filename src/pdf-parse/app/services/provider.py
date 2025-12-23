from abc import ABC, abstractmethod

from fastapi import UploadFile

# from app.schemas.extract import ExtractionResponse


class ExtractionProvider(ABC):
    @abstractmethod
    # TODO: replace return type from dict to ExtractionResponse once mapping is fixed
    # async def extract(self, file: UploadFile) -> ExtractionResponse:
    async def extract(self, file: UploadFile) -> dict:
        pass


def get_provider() -> ExtractionProvider:
    from app.services.docling import DoclingExtractionProvider

    return DoclingExtractionProvider()
