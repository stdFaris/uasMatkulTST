# src/schemas/partner.py
from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from datetime import datetime, time
from ..models.customer import UserRole
from ..models.partner import Gender

class PartnerBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: str
    gender: Gender
    bio: Optional[str] = None
    specializations: Optional[str] = None

class PartnerCreate(PartnerBase):
    password: str

class PartnerUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    profile_image: Optional[str] = None
    is_active: Optional[bool] = None
    gender: Optional[Gender] = None
    bio: Optional[str] = None
    specializations: Optional[str] = None

class ServiceAreaBase(BaseModel):
    province_id: int
    regency_id: int
    district_id: Optional[int] = None
    village_id: Optional[int] = None
    
class ServiceAreaCreate(ServiceAreaBase):
    pass

class ServiceAreaResponse(ServiceAreaBase):
    id: int
    partner_id: int
    province: dict
    regency: dict
    district: Optional[dict]
    village: Optional[dict]
    created_at: datetime

    class Config:
        from_attributes = True

class ScheduleBase(BaseModel):
    day_of_week: int  # 0-6 (Monday-Sunday)
    start_time: time
    end_time: time
    is_available: bool = True

    @validator('day_of_week')
    def validate_day_of_week(cls, v):
        if not 0 <= v <= 6:
            raise ValueError('day_of_week must be between 0 and 6')
        return v

    @validator('end_time')
    def validate_time_range(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(ScheduleBase):
    id: int
    partner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PartnerResponse(PartnerBase):
    id: int
    is_active: bool
    is_verified: bool
    role: UserRole
    profile_image: Optional[str]
    rating: float
    total_reviews: int
    created_at: datetime
    service_areas: List[ServiceAreaResponse]
    schedules: List[ScheduleResponse]
    
    class Config:
        from_attributes = True