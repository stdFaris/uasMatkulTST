# src/services/schedule_service.py
from sqlalchemy.orm import Session
from typing import List, Tuple
from datetime import datetime, timedelta
from src.models.booking import Booking
from src.schemas.booking import BookingStatus
from src.schemas.schedule import TimeSlot
from src.schemas.booking import BookingType

class ScheduleService:
    @staticmethod
    async def get_available_slots(
        db: Session,
        partner_id: int,
        start_date: datetime,
        end_date: datetime,
        booking_type: BookingType
    ) -> List[TimeSlot]:
        # Get existing bookings
        existing_bookings = db.query(Booking).filter(
            Booking.partner_id == partner_id,
            Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED]),
            Booking.start_datetime < end_date,
            Booking.end_datetime > start_date
        ).all()
        
        # Generate all possible slots
        all_slots = []
        current = start_date
        
        while current < end_date:
            # Only consider slots during business hours (8 AM - 8 PM)
            if 1 == 1:
                if booking_type == BookingType.HOURLY:
                    slot_end = current + timedelta(hours=1)
                elif booking_type == BookingType.DAILY:
                    slot_end = (current + timedelta(days=1)).replace(hour=20, minute=0)
                else:  # MONTHLY
                    slot_end = (current + timedelta(days=30)).replace(hour=20, minute=0)
                
                is_available = True
                
                # Check for conflicts with existing bookings
                for booking in existing_bookings:
                    if (booking.start_datetime <= current < booking.end_datetime or
                        booking.start_datetime < slot_end <= booking.end_datetime):
                        is_available = False
                        break
                
                # Add buffer time after each booking
                if is_available and booking_type == BookingType.HOURLY:
                    buffer_end = slot_end + timedelta(hours=1)
                    for booking in existing_bookings:
                        if (booking.start_datetime <= buffer_end <= booking.end_datetime):
                            is_available = False
                            break
                
                if is_available:
                    all_slots.append(TimeSlot(
                        start_time=current,
                        end_time=slot_end,
                        is_available=True
                    ))
            
            # Increment based on booking type
            if booking_type == BookingType.HOURLY:
                current += timedelta(hours=1)
            elif booking_type == BookingType.DAILY:
                current += timedelta(days=1)
            else:  # MONTHLY
                current += timedelta(days=30)
        
        return all_slots

    @staticmethod
    async def check_partner_availability(
        db: Session,
        partner_id: int,
        start_time: datetime,
        end_time: datetime
    ) -> bool:
        # Check if there are any overlapping bookings
        start_time = start_time.astimezone()
        end_time = end_time.astimezone()
        overlapping = db.query(Booking).filter(
            Booking.partner_id == partner_id,
            Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED]),
            Booking.start_datetime < end_time,
            Booking.end_datetime > start_time
        ).first()
            
        # Check buffer time
        buffer_end = end_time + timedelta(hours=1)
        buffer_conflict = db.query(Booking).filter(
            Booking.partner_id == partner_id,
            Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED]),
            Booking.start_datetime <= buffer_end,
            Booking.end_datetime > end_time
        ).first()
        
        return not (overlapping or buffer_conflict)

    @staticmethod
    async def validate_booking_duration(
        booking_type: BookingType,
        start_time: datetime,
        end_time: datetime
    ) -> Tuple[bool, str]:
        duration = end_time - start_time
        
        if booking_type == BookingType.HOURLY:
            if duration.total_seconds() > 21600:  # 6 hours
                return False, "Hourly bookings cannot exceed 6 hours"
        elif booking_type == BookingType.DAILY:
            if duration.days > 7:
                return False, "Daily bookings cannot exceed 7 days"
        # Monthly bookings don't have a maximum duration limit
        
        return True, ""