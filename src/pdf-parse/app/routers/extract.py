from fastapi import APIRouter, HTTPException, Request, UploadFile

# from app.schemas.extract import ExtractionResponse

router = APIRouter(prefix="/extract", tags=["extraction"])


# TODO: Enable this once the service is sending correct schema
# @router.post("", response_model=ExtractionResponse)
@router.post("")
async def extract_pdf(file: UploadFile, request: Request):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files supported")

    provider = request.app.state.provider
    result = await provider.extract(file)
    return result
