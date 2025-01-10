# src/schemas/dashboard.py
from pydantic import BaseModel
from typing import List
from .customer import CustomerResponse
from .partner import PartnerResponse
from .booking import BookingResponse
from .notification import NotificationResponse

class DashboardStats(BaseModel):
    total_bookings: int
    active_bookings: int
    completed_bookings: int
    cancelled_bookings: int
    total_spent: float

class CustomerDashboard(BaseModel):
    customer: CustomerResponse
    upcoming_bookings: List[BookingResponse]
    recommended_partners: List[PartnerResponse]
    stats: DashboardStats
    active_bookings: int  # Ditambahkan sesuai error
    recent_notifications: List[NotificationResponse]  # Ditambahkan sesuai error

    class Config:
        from_attributes = True