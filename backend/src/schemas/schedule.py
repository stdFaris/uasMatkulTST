# src/schemas/schedule.py
from pydantic import BaseModel
from typing import List
from datetime import datetime
from .booking import BookingResponse

class TimeSlot(BaseModel):
    start_time: datetime
    end_time: datetime
    is_available: bool
    
class PartnerAvailability(BaseModel):
    partner_id: int
    available_slots: List[TimeSlot]
    blocked_slots: List[TimeSlot]

class ScheduleResponse(BaseModel):
    upcoming_bookings: List[BookingResponse]
    past_bookings: List[BookingResponse]
    cancelled_bookings: List[BookingResponse]
