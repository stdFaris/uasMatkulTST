# src/schemas/error.py
from pydantic import BaseModel
from typing import Optional, List

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    details: Optional[List[str]] = None