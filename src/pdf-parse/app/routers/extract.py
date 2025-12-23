from fastapi import APIRouter, HTTPException, UploadFile

from app.services.provider import get_provider

# from app.schemas.extract import ExtractionResponse

router = APIRouter(prefix="/extract", tags=["extraction"])


# TODO: Enable this once the service is sending correct schema
# @router.post("", response_model=ExtractionResponse)
@router.post("")
async def extract_pdf(file: UploadFile):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Only PDF files supported")

    provider = get_provider()
    result = await provider.extract(file)
    return result
