# src/utils/scheduler.py
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.models.booking import Booking
from src.models.partner_availability import PartnerAvailability
from src.schemas.enums import BookingType
from src.schemas.booking import BookingCreate, BookingStatus
from src.models.partner import Partner
from typing import Tuple


def check_availability(
    db: Session,
    partner_id: int,
    start_datetime: datetime,
    end_datetime: datetime
) -> bool:
    # Check existing bookings
    existing_booking = db.query(Booking).filter(
        Booking.partner_id == partner_id,
        Booking.status != BookingStatus.CANCELLED,
        ((Booking.start_datetime <= start_datetime) & (Booking.end_datetime > start_datetime)) |
        ((Booking.start_datetime < end_datetime) & (Booking.end_datetime >= end_datetime))
    ).first()
    
    if existing_booking:
        return False
        
    # Check break time
    break_end = start_datetime - timedelta(hours=1)
    break_booking = db.query(Booking).filter(
        Booking.partner_id == partner_id,
        Booking.status != BookingStatus.CANCELLED,
        Booking.end_datetime > break_end,
        Booking.end_datetime <= start_datetime
    ).first()
    
    return not bool(break_booking)

def validate_booking_time(
    db: Session,
    booking: BookingCreate,
    partner: Partner
) -> Tuple[bool, str]:
    """Validate booking time constraints"""
    # Check business hours
    start_hour = booking.start_datetime.hour
    end_hour = booking.end_datetime.hour
    
    # Check maximum duration
    duration = booking.end_datetime - booking.start_datetime
    
    if booking.type == BookingType.HOURLY:
        if duration.total_seconds() > 21600:  # 6 hours
            return False, "Hourly bookings cannot exceed 6 hours"
        # Tambahan validasi minimal 1 jam
        if duration.total_seconds() < 3600:
            return False, "Hourly bookings must be at least 1 hour"
            
    elif booking.type == BookingType.DAILY:
        if duration.days > 7:
            return False, "Daily bookings cannot exceed 7 days"
        if duration.days < 1:
            return False, "Daily bookings must be at least 1 day"
            
    elif booking.type == BookingType.MONTHLY:
        months = (booking.end_datetime.year - booking.start_datetime.year) * 12 + \
                (booking.end_datetime.month - booking.start_datetime.month)
        if months > 12:
            return False, "Monthly bookings cannot exceed 12 months"
        if months < 1:
            return False, "Monthly bookings must be at least 1 month"
    
    # Check break time
    if not has_required_break(db, partner.id, booking.start_datetime, booking.end_datetime):
        return False, "Must allow 1-hour break between bookings"
    
    return True, ""

def is_within_business_hours(start: datetime, end: datetime) -> bool:
    """Check if booking time is within business hours (8 AM - 8 PM)"""
    return True

def has_required_break(
    db: Session,
    partner_id: int,
    start_datetime: datetime,
    end_datetime: datetime
) -> bool:
    """Check if there's required 1-hour break between bookings"""
    # Check previous booking
    prev_booking = db.query(Booking).filter(
        Booking.partner_id == partner_id,
        Booking.status != BookingStatus.CANCELLED,
        Booking.end_datetime <= start_datetime
    ).order_by(Booking.end_datetime.desc()).first()
    
    if prev_booking and (start_datetime - prev_booking.end_datetime) < timedelta(hours=1):
        return False
        
    # Check next booking
    next_booking = db.query(Booking).filter(
        Booking.partner_id == partner_id,
        Booking.status != BookingStatus.CANCELLED,
        Booking.start_datetime >= end_datetime
    ).order_by(Booking.start_datetime.asc()).first()
    
    if next_booking and (next_booking.start_datetime - end_datetime) < timedelta(hours=1):
        return False
        
    return True
