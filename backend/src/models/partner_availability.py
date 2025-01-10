# src/models/partner_availability.py
from datetime import datetime
from sqlalchemy import ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base, TimestampModel

class PartnerAvailability(Base, TimestampModel):
    __tablename__ = "partner_availabilities"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    partner_id: Mapped[int] = mapped_column(ForeignKey("partners.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)

    partner: Mapped["Partner"] = relationship(back_populates="availabilities")