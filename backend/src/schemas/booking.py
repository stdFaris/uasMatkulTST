# src/schemas/booking.py
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime, timedelta
from enum import Enum
from .enums import PartnerRole, BookingType
from .partner import PartnerResponse
from src.config.settings import settings

class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed" 
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class BookingCreate(BaseModel):
    partner_id: int
    type: BookingType
    start_datetime: datetime
    end_datetime: datetime
    notes: Optional[str]
    
    @validator('start_datetime')
    def validate_booking_time(cls, v):
        # Convert datetime.now() to UTC for consistent comparison
        current_time = datetime.now().astimezone()
        booking_time = v.astimezone()
        if booking_time < current_time:
            raise ValueError("Cannot book in the past")
        return v

    @validator('end_datetime')
    def validate_booking_duration(cls, v, values):
        if 'start_datetime' not in values:
            return v
        
        start = values['start_datetime'].astimezone()
        end = v.astimezone()
            
        duration = end - start
        if values.get('type') == BookingType.HOURLY:
            if duration.total_seconds() > 21600:  # 6 hours in seconds
                raise ValueError("Hourly bookings cannot exceed 6 hours")
        elif values.get('type') == BookingType.DAILY:
            if duration.days > 7:
                raise ValueError("Daily bookings cannot exceed 7 days")
        
        return v
    
class BookingCancel(BaseModel):
    reason: str
    cancellation_time: datetime

    @validator('cancellation_time')
    def validate_cancellation_notice(cls, v):
        current_time = datetime.now().astimezone()
        cancel_time = v.astimezone()
        min_time = current_time + timedelta(hours=settings.MINIMUM_CANCELLATION_NOTICE)
        
        if cancel_time < min_time:
            raise ValueError(f"Cancellation must be made at least {settings.MINIMUM_CANCELLATION_NOTICE} hours in advance")
        return v

class BookingResponse(BaseModel):
    id: int
    partner_id: int
    type: BookingType
    start_datetime: datetime
    end_datetime: datetime
    status: BookingStatus
    total_price: float
    notes: Optional[str]
    partner: PartnerResponse

    class Config:
        from_attributes = True
