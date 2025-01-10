# src/schemas/base.py
from pydantic import BaseModel
from typing import Generic, List, Optional, TypeVar
from datetime import datetime

T = TypeVar("T")

class PageResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int = 1
    per_page: int = 10

class Response(BaseModel, Generic[T]):
    status: str = "success"
    message: Optional[str] = None
    data: Optional[T] = None
    errors: Optional[List[str]] = None