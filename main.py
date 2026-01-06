from pydantic import BaseModel, Field
from typing import Generic, TypeVar
from datetime import datetime

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    data: T
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.now)
    message: str = "Success"
