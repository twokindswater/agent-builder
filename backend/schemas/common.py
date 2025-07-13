"""
Common schemas used across the application
"""

from typing import TypeVar, Generic, Optional, Dict, Any
from pydantic import BaseModel

DataT = TypeVar("DataT")
T = TypeVar("T")

class APIResponse(BaseModel, Generic[DataT]):
    """API 공통 응답 스키마"""
    success: bool
    data: Optional[DataT] = None
    error: Optional[str] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: Dict[str, Any]
    message: str

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int 