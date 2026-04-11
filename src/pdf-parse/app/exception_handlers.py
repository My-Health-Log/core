from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas.api_response import ApiResponse


def api_exception_handler(__request__, exception):
    message = "Internal server error"
    status_code = 500
    error_details = str(exception)

    if isinstance(exception, RequestValidationError):
        status_code = 422
        message = "Validation Error"
        error_details = str(exception.errors())
    elif isinstance(exception, HTTPException):
        status_code = exception.status_code
        message = exception.detail
        error_details = None

    return JSONResponse(
        status_code=status_code,
        content=ApiResponse(
            success=False, message=message, error=error_details
        ).model_dump(),
    )
