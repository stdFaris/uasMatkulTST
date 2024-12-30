# src/schemas/booking.py
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from ..models.customer import BookingStatus, BookingType

class BookingBase(BaseModel):
    partner_id: int
    booking_type: BookingType
    start_datetime: datetime
    duration_hours: Optional[int] = None
    notes: Optional[str] = None

class BookingCreate(BookingBase):
    @validator('duration_hours')
    def validate_duration(cls, v, values):
        if values.get('booking_type') == BookingType.HOURLY and not v:
            raise ValueError('Duration hours is required for hourly bookings')
        return v

class BookingUpdate(BaseModel):
    notes: Optional[str] = None

class BookingStatusUpdate(BaseModel):
    status: BookingStatus

class BookingResponse(BookingBase):
    id: int
    customer_id: int
    status: BookingStatus
    end_datetime: datetime
    total_price: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BookingDetailResponse(BookingResponse):
    customer: dict
    partner: dict
    review: Optional[dict]

    class Config:
        from_attributes = True
