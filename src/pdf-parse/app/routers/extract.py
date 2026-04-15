from fastapi import APIRouter, Depends, HTTPException, UploadFile

from app.deps import get_provider
from app.schemas.api_response import ApiResponse
from app.schemas.extract import ExtractionResponse
from app.services.provider import ExtractionProvider

router = APIRouter(prefix="/extract", tags=["extraction"])


@router.post(
    "", response_model=ApiResponse[ExtractionResponse], response_model_exclude_none=True
)
async def extract_pdf(
    file: UploadFile, provider: ExtractionProvider = Depends(get_provider)
):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files supported")

    result = await provider.extract(file)
    return ApiResponse[ExtractionResponse](
        success=True, message="Payload extracted successfully", data=result
    )
