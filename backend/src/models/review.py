# src/models/review.py
from typing import Optional
from sqlalchemy import ForeignKey, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampModel

class Review(Base, TimestampModel):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"), unique=True)
    rating: Mapped[float] = mapped_column(Float)
    comment: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    booking: Mapped["Booking"] = relationship(back_populates="review")