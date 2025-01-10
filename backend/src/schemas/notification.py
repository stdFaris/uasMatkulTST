# src/schemas/notification.py
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from .booking import BookingResponse

class NotificationType(str, Enum):
    BOOKING_REMINDER = "booking_reminder"
    SCHEDULE_CHANGE = "schedule_change"
    BOOKING_CONFIRMATION = "booking_confirmation"
    PARTNER_UNAVAILABLE = "partner_unavailable"

class NotificationCreate(BaseModel):
    customer_id: int
    type: NotificationType
    booking_id: int
    scheduled_for: datetime
    
class NotificationResponse(BaseModel):
    id: int
    type: NotificationType
    message: str
    booking: BookingResponse
    created_at: datetime
    is_read: bool

    class Config:
        from_attributes = True
