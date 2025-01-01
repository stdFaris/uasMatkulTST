# src/services/booking.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Optional
from ..models.customer import BookingStatus, BookingType
from ..models.booking import Booking
from ..models.partner import Partner, PartnerSchedule, PartnerAvailability
from .notification import notification_service
from .matching import PartnerMatchingService

class BookingService:
    def __init__(self, db: Session):
        self.db = db

    async def create_booking(self, customer_id: int, booking_data: dict) -> Booking:
        # Validate minimum booking time (90 minutes from now)
        current_time = datetime.utcnow()
        minimum_booking_time = current_time + timedelta(minutes=90)
        
        if booking_data["start_datetime"] < minimum_booking_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Booking must be made at least 90 minutes in advance. Earliest available time: {minimum_booking_time.strftime('%Y-%m-%d %H:%M')}"
            )

        # Use matching service if no partner specified
        if not booking_data.get("partner_id"):
            matching_service = PartnerMatchingService(self.db)
            partners = matching_service.find_best_partners(booking_data)
            if not partners:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No available partners found"
                )
            booking_data["partner_id"] = partners[0].id

        # Validate booking time
        if not self._is_valid_booking_time(booking_data["start_datetime"], booking_data["partner_id"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid booking time or partner not available"
            )

        # Create booking with pending status
        booking = Booking(
            customer_id=customer_id,
            status=BookingStatus.PENDING,
            end_datetime=self._calculate_end_datetime(
                booking_data["start_datetime"],
                booking_data["booking_type"],
                booking_data.get("duration_hours")
            ),
            total_price=self._calculate_price(
                booking_data["partner_id"],
                booking_data["booking_type"],
                booking_data.get("duration_hours")
            ),
            **booking_data
        )
        
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        
        # Schedule notifications
        reminder_time = booking.start_datetime - timedelta(minutes=30)
        notification_service.schedule_reminder(booking.id, reminder_time)
        
        return booking

    def reschedule_booking(self, booking_id: int, new_datetime: datetime) -> Booking:
        """Reschedule a booking to a new time."""
        # Validate minimum booking time (90 minutes from now)
        current_time = datetime.utcnow()
        minimum_booking_time = current_time + timedelta(minutes=90)
        
        if new_datetime < minimum_booking_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Booking must be rescheduled at least 90 minutes in advance. Earliest available time: {minimum_booking_time.strftime('%Y-%m-%d %H:%M')}"
            )

        booking = self.db.query(Booking).get(booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
            
        if not self._is_valid_booking_time(new_datetime, booking.partner_id):
            raise HTTPException(status_code=400, detail="Invalid new booking time")
            
        # Calculate new end time
        duration = booking.end_datetime - booking.start_datetime
        new_end_datetime = new_datetime + duration
        
        # Update booking
        booking.start_datetime = new_datetime
        booking.end_datetime = new_end_datetime
        booking.status = BookingStatus.PENDING  # Require reconfirmation
        
        self.db.commit()
        
        # Reschedule reminder
        reminder_time = new_datetime - timedelta(minutes=30)
        notification_service.reschedule_reminder(booking.id, reminder_time)
        
        return booking

    def _is_valid_booking_time(self, start_datetime: datetime, partner_id: int) -> bool:
        # Validate minimum 90-minute advance booking
        current_time = datetime.utcnow()
        minimum_booking_time = current_time + timedelta(minutes=90)
        
        if start_datetime < minimum_booking_time:
            return False

        # Check if booking is during partner's schedule
        day_of_week = start_datetime.weekday()
        partner = self.db.query(Partner).get(partner_id)
        
        if not partner:
            return False
            
        schedule = self.db.query(PartnerSchedule).filter(
            PartnerSchedule.partner_id == partner_id,
            PartnerSchedule.day_of_week == day_of_week,
            PartnerSchedule.is_available == True
        ).first()
        
        if not schedule:
            return False
            
        booking_time = start_datetime.time()
        return schedule.start_time <= booking_time <= schedule.end_time
    
    
    def _validate_partner(self, partner_id: int) -> Partner:
        partner = self.db.query(Partner).filter(
            Partner.id == partner_id,
            Partner.is_active == True,
            Partner.is_verified == True
        ).first()
        
        if not partner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Partner not found or not available"
            )
        return partner

    def _is_valid_booking_time(self, start_datetime: datetime, partner: Partner) -> bool:
        # Check if booking is during partner's schedule
        day_of_week = start_datetime.weekday()
        schedule = self.db.query(PartnerSchedule).filter(
            PartnerSchedule.partner_id == partner.id,
            PartnerSchedule.day_of_week == day_of_week,
            PartnerSchedule.is_available == True
        ).first()
        
        if not schedule:
            return False
            
        booking_time = start_datetime.time()
        return schedule.start_time <= booking_time <= schedule.end_time
            
    
    def _calculate_end_datetime(
        self,
        start_datetime: datetime,
        booking_type: BookingType,
        duration_hours: Optional[int] = None
    ) -> datetime:
        if booking_type == BookingType.HOURLY:
            return start_datetime + timedelta(hours=duration_hours)
        elif booking_type == BookingType.DAILY:
            return start_datetime + timedelta(days=1)
        else:  # MONTHLY
            next_month = start_datetime.replace(day=1) + timedelta(days=32)
            return next_month.replace(day=1) - timedelta(days=1)
    
    def _calculate_price(
        self,
        partner_id: int,
        booking_type: BookingType,
        duration_hours: Optional[int] = None
    ) -> float:
        partner = self.db.query(Partner).get(partner_id)
        
        if booking_type == BookingType.HOURLY:
            return partner.hourly_rate * duration_hours
        elif booking_type == BookingType.DAILY:
            return partner.daily_rate
        else:  # MONTHLY
            return partner.monthly_rate
    
    def _update_partner_availability(self, booking: Booking):
        if booking.booking_type == BookingType.HOURLY:
            availability = PartnerAvailability(
                partner_id=booking.partner_id,
                date=booking.start_datetime.date(),
                booking_type=BookingType.HOURLY,
                time_slot_start=booking.start_datetime.time(),
                time_slot_end=booking.end_datetime.time(),
                is_booked=True
            )
            self.db.add(availability)
        else:
            # For daily/monthly bookings, block the entire period
            current_date = booking.start_datetime.date()
            while current_date <= booking.end_datetime.date():
                availability = PartnerAvailability(
                    partner_id=booking.partner_id,
                    date=current_date,
                    booking_type=booking.booking_type,
                    is_booked=True
                )
                self.db.add(availability)
                current_date += timedelta(days=1)
        
        self.db.commit()
    
    def update_booking_status(
        self,
        booking_id: int,
        new_status: BookingStatus,
        user_id: int,
        is_partner: bool = False
    ) -> Booking:
        booking = self.db.query(Booking).get(booking_id)
        
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        
        # Verify user permission
        if is_partner and booking.partner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this booking"
            )
        elif not is_partner and booking.customer_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this booking"
            )
        
        # Validate status transition
        valid_transitions = {
            BookingStatus.PENDING: [BookingStatus.CONFIRMED, BookingStatus.CANCELLED],
            BookingStatus.CONFIRMED: [BookingStatus.IN_PROGRESS, BookingStatus.CANCELLED],
            BookingStatus.IN_PROGRESS: [BookingStatus.COMPLETED, BookingStatus.TERMINATED],
            BookingStatus.COMPLETED: [],
            BookingStatus.CANCELLED: [],
            BookingStatus.TERMINATED: []
        }
        
        if new_status not in valid_transitions[booking.status]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot transition from {booking.status} to {new_status}"
            )
        
        booking.status = new_status
        booking.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(booking)
        
        return booking

