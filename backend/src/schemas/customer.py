# src/schemas/customer.py
from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime
from ..models.customer import UserRole, BookingStatus

class CustomerBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: constr(regex=r'^\+?[1-9]\d{1,14}$')

class CustomerCreate(CustomerBase):
    password: str

class CustomerUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[constr(regex=r'^\+?[1-9]\d{1,14}$')] = None
    password: Optional[str] = None
    profile_image: Optional[str] = None
    is_active: Optional[bool] = None

class CustomerResponse(CustomerBase):
    id: int
    is_active: bool
    role: UserRole
    profile_image: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    booking_id: int
    customer_id: int
    partner_id: int
    created_at: datetime

    class Config:
        from_attributes = True
