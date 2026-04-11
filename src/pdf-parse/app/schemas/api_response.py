from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
    error: Optional[str] = None

    def model_dump(self, **kwargs):
        return super().model_dump(exclude_none=True, **kwargs)
