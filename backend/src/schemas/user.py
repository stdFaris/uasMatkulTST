from pydantic import BaseModel, EmailStr
from typing import Optional
from models.user import UserRole, ServiceType

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: UserRole

class CustomerProfileCreate(BaseModel):
    location: str

class PartnerProfileCreate(BaseModel):
    location: str
    service_type: ServiceType
    hourly_rate: float
    working_hours_start: str
    working_hours_end: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None