# src/models/customer.py
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Boolean
from sqlalchemy.types import JSON
from .base import Base, TimestampModel

class Customer(Base, TimestampModel):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    full_name: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String)
    kecamatan: Mapped[str] = mapped_column(String, index=True)
    preferences: Mapped[dict] = mapped_column(JSON, nullable=True, default={})
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    
    bookings: Mapped[List["Booking"]] = relationship(back_populates="customer")
    notifications: Mapped[List["Notification"]] = relationship(back_populates="customer")