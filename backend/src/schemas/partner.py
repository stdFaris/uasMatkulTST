# src/schemas/partner.py
from pydantic import BaseModel, EmailStr, validator, Field
from typing import List, Optional
from datetime import datetime
from ..models.customer import UserRole

class PartnerBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: str
    bio: Optional[str] = None
    specializations: Optional[str] = None

class PartnerCreate(PartnerBase):
    password: str

class PartnerUpdate(PartnerBase):
    password: Optional[str] = None
    profile_image: Optional[str] = None
    is_active: Optional[bool] = None

class PartnerResponse(PartnerBase):
    id: int
    is_active: bool
    is_verified: bool
    role: UserRole
    profile_image: Optional[str]
    rating: float
    total_reviews: int
    created_at: datetime
    
    class Config:
        from_attributes = True