# src/models/booking.py
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Text, DateTime, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import BaseModel, TimeStampedModel
from .customer import BookingStatus, BookingType

class Booking(BaseModel, TimeStampedModel):
    __tablename__ = "bookings"
    
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    partner_id = Column(Integer, ForeignKey("partners.id", ondelete="CASCADE"), nullable=False)
    booking_type = Column(Enum(BookingType), nullable=False, index=True)
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING, index=True)
    start_datetime = Column(DateTime, nullable=False, index=True)
    end_datetime = Column(DateTime, nullable=False)
    duration_hours = Column(Integer)
    total_price = Column(Float, nullable=False)
    notes = Column(Text)
    
    # Updated relationships
    customer = relationship("Customer", back_populates="bookings")
    partner = relationship("Partner", back_populates="bookings")
    review = relationship("Review", back_populates="booking", uselist=False, cascade="all, delete-orphan")

class Review(BaseModel, TimeStampedModel):
    __tablename__ = "reviews"
    
    booking_id = Column(Integer, ForeignKey("bookings.id"), unique=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    partner_id = Column(Integer, ForeignKey("partners.id"))
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    
    # Relationships
    booking = relationship("Booking", back_populates="review")
    customer = relationship("Customer", back_populates="reviews")
    partner = relationship("Partner", back_populates="reviews")
