from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.deps import get_provider
from app.services.provider import ExtractionProvider

# from app.schemas.extract import ExtractionResponse

router = APIRouter(prefix="/extract", tags=["extraction"])


# TODO: Enable this once the service is sending correct schema
# @router.post("", response_model=ExtractionResponse)
@router.post("")
async def extract_pdf(
    file: UploadFile, provider: ExtractionProvider = Depends(get_provider)
):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files supported")

    result = await provider.extract(file)
    return result
