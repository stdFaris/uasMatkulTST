# src/models/notification.py
from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, Enum, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampModel
from src.schemas.notification import NotificationType

class Notification(Base, TimestampModel):
    __tablename__ = "notifications"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"))
    type: Mapped[NotificationType] = mapped_column(Enum(NotificationType))
    message: Mapped[str] = mapped_column(String)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    scheduled_for: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    customer: Mapped["Customer"] = relationship(back_populates="notifications")
    booking: Mapped["Booking"] = relationship(back_populates="notifications")