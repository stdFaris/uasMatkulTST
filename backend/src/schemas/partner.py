# src/schemas/partner.py
from pydantic import BaseModel, confloat
from typing import List, Optional
from datetime import datetime
from enum import Enum
from .enums import PartnerRole, BookingType

class PartnerFilter(BaseModel):
    role: Optional[PartnerRole] = None
    min_rating: Optional[float] = None
    min_experience: Optional[int] = None 
    max_hourly_rate: Optional[float] = None
    specialization: Optional[str] = None

class PartnerPricing(BaseModel):
    hourly_rate: confloat(ge=0)
    daily_rate: confloat(ge=0)
    monthly_rate: confloat(ge=0)

class PartnerResponse(BaseModel):
    id: int
    full_name: str
    role: PartnerRole
    experience_years: int
    rating: float
    total_reviews: int
    specializations: List[str]
    pricing: PartnerPricing
    kecamatan: str
    is_available: bool
    available_hours: Optional[List[dict]] = []
    profile_image: Optional[str] = None
    preferred_booking_type: Optional[BookingType] = None
    languages: Optional[List[str]] = []
    profile_description: Optional[str] = None

    class Config:
        from_attributes = True