# src/models/customer.py
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Float, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .base import BaseModel, TimeStampedModel

class UserRole(str, enum.Enum):
    CUSTOMER = "customer"
    PARTNER = "partner"
    ADMIN = "admin"

class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    TERMINATED = "terminated"

class BookingType(str, enum.Enum):
    HOURLY = "hourly"
    DAILY = "daily"
    MONTHLY = "monthly"

class Customer(BaseModel, TimeStampedModel):
    __tablename__ = "customers"
    
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True, nullable=False)
    phone = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    role = Column(String, default=UserRole.CUSTOMER)
    profile_image = Column(String)
    
    # Updated relationships with cascade
    bookings = relationship("Booking", back_populates="customer", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="customer", cascade="all, delete-orphan")
