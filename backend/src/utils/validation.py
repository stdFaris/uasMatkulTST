# src/utils/validation.py
from datetime import datetime, timedelta
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from src.models.partner import Partner
from src.models.booking import Booking
from src.schemas.booking import BookingStatus
from src.config.settings import settings
from .scheduler import has_required_break  

def validate_partner_availability(
    db: Session,
    partner_id: int,
    start_datetime: datetime,
    end_datetime: datetime,
    exclude_booking_id: Optional[int] = None
) -> Tuple[bool, str]:
    """
    Comprehensive validation for partner availability
    """
    # Check if partner exists and is available
    partner = db.query(Partner).filter(
        Partner.id == partner_id,
        Partner.is_available == True
    ).first()
    
    if not partner:
        return False, "Partner not found or unavailable"
    # Check existing bookings
    query = db.query(Booking).filter(
        Booking.partner_id == partner_id,
        Booking.status.in_([BookingStatus.CONFIRMED, BookingStatus.PENDING]),
        ~((Booking.end_datetime <= start_datetime) | 
          (Booking.start_datetime >= end_datetime))
    )
    
    if exclude_booking_id:
        query = query.filter(Booking.id != exclude_booking_id)
    
    if query.first():
        return False, "Time slot already booked"
    
    # Check break time
    if not has_required_break(db, partner_id, start_datetime, end_datetime):
        return False, "Must allow 1-hour break between bookings"
    
    return True, ""
