# src/models/partner.py
from sqlalchemy import Column, String, Boolean, Float, Integer, ForeignKey, Text, Time, Date, Enum
import enum
from sqlalchemy.orm import relationship
from .base import BaseModel, TimeStampedModel
from .customer import UserRole, BookingType
from .location import Province, District, Regency  # Import location models

class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"

class Partner(BaseModel, TimeStampedModel):
    __tablename__ = "partners"
    
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String, default=UserRole.PARTNER)
    profile_image = Column(String)
    gender = Column(Enum(Gender), nullable=False)
    rating = Column(Float, default=0)
    total_reviews = Column(Integer, default=0)
    bio = Column(Text)
    specializations = Column(Text)
    hourly_rate = Column(Float, nullable=False, default=50.0)
    daily_rate = Column(Float, nullable=False, default=300.0)
    monthly_rate = Column(Float, nullable=False, default=8000.0)
    
    service_areas = relationship("ServiceArea", back_populates="partner", cascade="all, delete-orphan")
    schedules = relationship("PartnerSchedule", back_populates="partner", cascade="all, delete-orphan")
    availability = relationship("PartnerAvailability", back_populates="partner", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="partner", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="partner", cascade="all, delete-orphan")

class ServiceArea(BaseModel):
    __tablename__ = "service_areas"
    
    partner_id = Column(Integer, ForeignKey("partners.id", ondelete="CASCADE"), nullable=False)
    province_id = Column(Integer, ForeignKey("provinces.id", ondelete="CASCADE"), nullable=False)
    regency_id = Column(Integer, ForeignKey("regencies.id", ondelete="CASCADE"), nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id", ondelete="CASCADE"), nullable=False)
    
    partner = relationship("Partner", back_populates="service_areas")
    province = relationship("Province")
    regency = relationship("Regency")
    district = relationship("District")

class PartnerSchedule(BaseModel):
    __tablename__ = "partner_schedules"
    
    partner_id = Column(Integer, ForeignKey("partners.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 0 = Monday, 6 = Sunday
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    is_available = Column(Boolean, default=True)
    
    partner = relationship("Partner", back_populates="schedules")

class PartnerAvailability(BaseModel):
    __tablename__ = "partner_availability"
    
    partner_id = Column(Integer, ForeignKey("partners.id"), nullable=False)
    date = Column(Date, nullable=False)
    booking_type = Column(Enum(BookingType), nullable=False)
    time_slot_start = Column(Time)  # Only for hourly bookings
    time_slot_end = Column(Time)    # Only for hourly bookings
    is_booked = Column(Boolean, default=False)
    
    partner = relationship("Partner", back_populates="availability")
