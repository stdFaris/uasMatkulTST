from typing import List, Dict
from sqlalchemy import String, Float, Boolean, JSON, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampModel
from src.schemas.partner import PartnerRole

class Partner(Base, TimestampModel):
    __tablename__ = "partners"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String)
    role: Mapped[PartnerRole] = mapped_column(Enum(PartnerRole))
    experience_years: Mapped[int] = mapped_column()
    rating: Mapped[float] = mapped_column(Float, default=5.0)
    total_reviews: Mapped[int] = mapped_column(default=0)
    specializations: Mapped[Dict] = mapped_column(JSON)
    pricing: Mapped[Dict] = mapped_column(JSON)
    kecamatan: Mapped[str] = mapped_column(String, index=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    # Gunakan string untuk reference
    availabilities: Mapped[List["PartnerAvailability"]] = relationship(back_populates="partner")
    bookings: Mapped[List["Booking"]] = relationship("Booking", back_populates="partner")