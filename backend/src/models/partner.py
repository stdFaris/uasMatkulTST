# src/models/partner.py
from sqlalchemy import Column, String, Boolean, Float, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel, TimeStampedModel
from .customer import UserRole

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
    
    # Partner specific fields
    service_areas = relationship("ServiceArea", back_populates="partner")
    schedule = relationship("PartnerSchedule", back_populates="partner")
    rating = Column(Float, default=0)
    total_reviews = Column(Integer, default=0)
    bio = Column(Text)
    specializations = Column(Text)  # Comma-separated list of specializations
    
    # Relationships
    bookings = relationship("Booking", back_populates="partner")
    reviews = relationship("Review", back_populates="partner")

class ServiceArea(BaseModel):
    __tablename__ = "service_areas"
    
    partner_id = Column(Integer, ForeignKey("partners.id"), nullable=False)
    province_id = Column(Integer, ForeignKey("provinces.id"), nullable=False)
    regency_id = Column(Integer, ForeignKey("regencies.id"), nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False)
    
    partner = relationship("Partner", back_populates="service_areas")
    province = relationship("Province")
    regency = relationship("Regency")
    district = relationship("District")