from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class SuccessResponse(BaseModel, Generic[T]):
    status: str = "success"
    message: str
    data: Optional[T] = None
