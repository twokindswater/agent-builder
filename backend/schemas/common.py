"""
Common response schemas
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any, Generic, TypeVar

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    message: str
    error: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: Dict[str, Any]
    message: str

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

class PaginatedResponse(BaseModel, Generic[T]):
    success: bool
    data: list[T]
    message: str
    total: int
    page: int
    size: int
    pages: int 