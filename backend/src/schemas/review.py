# src/schemas/review.py
from pydantic import BaseModel, confloat, constr
from typing import Optional
from datetime import datetime

class ReviewCreate(BaseModel):
    booking_id: int
    rating: confloat(ge=1, le=5)
    comment: Optional[constr(max_length=500)]

class ReviewResponse(BaseModel):
    id: int
    booking_id: int
    rating: float
    comment: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
