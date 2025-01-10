# src/schemas/customer.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Annotated
from datetime import datetime
from .partner import PartnerRole
from .booking import BookingType

class CustomerBase(BaseModel):
    email: EmailStr
    full_name: Annotated[str, Field(min_length=3, max_length=50)]
    phone: Annotated[str, Field(pattern=r'^\+?[1-9][0-9]{7,14}$')]
    kecamatan: str

class CustomerCreate(CustomerBase):
    password: Annotated[str, Field(min_length=8)]

class CustomerPreferences(BaseModel):
    preferred_partner_roles: List[PartnerRole] = [PartnerRole.PEMBANTU, PartnerRole.TUKANG_KEBUN, PartnerRole.TUKANG_PIJAT]
    preferred_booking_type: Optional[BookingType] = None
    min_rating: Optional[float] = None
    max_price_per_hour: Optional[float] = None
    preferred_languages: Optional[List[str]] = None

class CustomerUpdate(BaseModel):
    full_name: Optional[str]
    phone: Optional[str]
    kecamatan: Optional[str]
    preferences: Optional[CustomerPreferences]

class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
