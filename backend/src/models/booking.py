# src/models/booking.py
from datetime import datetime
from typing import Optional, List
from sqlalchemy import ForeignKey, Enum, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampModel
from src.schemas.booking import BookingType, BookingStatus

class Booking(Base, TimestampModel):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    cancellation_reason: Mapped[Optional[str]] = mapped_column(nullable=True)
    customer_notes: Mapped[Optional[str]] = mapped_column(nullable=True)
    partner_notes: Mapped[Optional[str]] = mapped_column(nullable=True)
    is_rescheduled: Mapped[bool] = mapped_column(default=False)
    original_booking_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    partner_id: Mapped[int] = mapped_column(ForeignKey("partners.id"))
    type: Mapped[BookingType] = mapped_column(Enum(BookingType))
    start_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    end_datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    status: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus), default=BookingStatus.PENDING)
    total_price: Mapped[float] = mapped_column(Float)
    notes: Mapped[Optional[str]] = mapped_column(nullable=True)

    customer: Mapped["Customer"] = relationship(back_populates="bookings")
    partner: Mapped["Partner"] = relationship(back_populates="bookings")
    notifications: Mapped[List["Notification"]] = relationship(back_populates="booking")
    review: Mapped[Optional["Review"]] = relationship("Review", back_populates="booking", uselist=False)