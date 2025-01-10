# src/services/booking_service.py
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.booking import Booking
from src.models.partner import Partner
from src.schemas.booking import BookingCreate, BookingStatus, BookingResponse
from src.utils.validation import validate_partner_availability
from src.utils.notification import schedule_booking_notifications
from src.utils.scheduler import validate_booking_time
from src.schemas.enums import BookingType
from src.schemas.schedule import ScheduleResponse

class BookingService:
    @staticmethod
    async def create_booking(
        db: Session,
        customer_id: int,
        booking: BookingCreate
    ) -> BookingResponse:
        # Validate partner availability
        is_available, message = validate_partner_availability(
            db,
            booking.partner_id,
            booking.start_datetime,
            booking.end_datetime
        )
        if not is_available:
            raise ValueError(message)

        # Calculate total price based on booking type and duration
        total_price = await BookingService.calculate_total_price(
            db,
            booking.partner_id,
            booking.type,
            booking.start_datetime,
            booking.end_datetime
        )

        # Create booking
        db_booking = Booking(
            customer_id=customer_id,
            partner_id=booking.partner_id,
            type=booking.type,
            start_datetime=booking.start_datetime,
            end_datetime=booking.end_datetime,
            status=BookingStatus.PENDING,
            total_price=total_price,
            notes=booking.notes
        )
        
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        
        # Schedule notifications
        schedule_booking_notifications(db, db_booking)
        
        return BookingResponse.model_validate(db_booking)

    @staticmethod
    async def calculate_total_price(
        db: Session,
        partner_id: int,
        booking_type: BookingType,
        start_datetime: datetime,
        end_datetime: datetime
    ) -> float:
        partner = db.query(Partner).get(partner_id)
        duration = end_datetime - start_datetime
        
        if booking_type == BookingType.HOURLY:
            hours = duration.total_seconds() / 3600
            return hours * partner.pricing['hourly_rate']
        elif booking_type == BookingType.DAILY:
            days = duration.days + (duration.seconds / 86400)
            return days * partner.pricing['daily_rate']
        else:  # MONTHLY
            months = duration.days / 30
            return months * partner.pricing['monthly_rate']

    @staticmethod
    async def get_customer_bookings(
        db: Session,
        customer_id: int
    ) -> List[BookingResponse]:
        bookings = db.query(Booking).filter(
            Booking.customer_id == customer_id
        ).order_by(Booking.start_datetime.desc()).all()
        return [BookingResponse.model_validate(b) for b in bookings]

    @staticmethod
    async def cancel_booking(
        db: Session,
        booking_id: int,
        customer_id: int,
        reason: str
    ) -> BookingResponse:
        booking = db.query(Booking).filter(
            Booking.id == booking_id,
            Booking.customer_id == customer_id
        ).first()
        
        if not booking:
            raise ValueError("Booking not found")
            
        if booking.status != BookingStatus.PENDING:
            raise ValueError("Can only cancel pending bookings")
            
        booking.status = BookingStatus.CANCELLED
        booking.cancellation_reason = reason
        
        db.commit()
        db.refresh(booking)
        return BookingResponse.model_validate(booking)

    @staticmethod
    async def reschedule_booking(
        db: Session,
        booking_id: int,
        customer_id: int,
        new_start_datetime: datetime,
        new_end_datetime: datetime
    ) -> BookingResponse:
        booking = db.query(Booking).filter(
            Booking.id == booking_id,
            Booking.customer_id == customer_id,
            Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED])
        ).first()

        if not booking:
            raise ValueError("Booking not found or cannot be rescheduled")

        # Validate new schedule
        is_available, message = validate_partner_availability(
            db,
            booking.partner_id,
            new_start_datetime,
            new_end_datetime,
            exclude_booking_id=booking_id
        )
        if not is_available:
            raise ValueError(message)

        # Create new booking with reference to original
        new_booking = Booking(
            customer_id=customer_id,
            partner_id=booking.partner_id,
            type=booking.type,
            start_datetime=new_start_datetime,
            end_datetime=new_end_datetime,
            status=BookingStatus.PENDING,
            total_price=booking.total_price,
            notes=booking.notes,
            is_rescheduled=True,
            original_booking_id=booking_id
        )

        # Update old booking status
        booking.status = BookingStatus.CANCELLED
        booking.cancellation_reason = "Rescheduled"

        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)

        # Schedule new notifications
        schedule_booking_notifications(db, new_booking)

        return BookingResponse.model_validate(new_booking)

    @staticmethod
    async def get_schedule_summary(
        db: Session,
        customer_id: int
    ) -> ScheduleResponse:
        current_time = datetime.now()
        
        # Get upcoming bookings
        upcoming = db.query(Booking).filter(
            Booking.customer_id == customer_id,
            Booking.start_datetime > current_time,
            Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED])
        ).order_by(Booking.start_datetime).all()

        # Get past bookings
        past = db.query(Booking).filter(
            Booking.customer_id == customer_id,
            Booking.end_datetime <= current_time,
            Booking.status == BookingStatus.COMPLETED
        ).order_by(Booking.start_datetime.desc()).all()

        # Get cancelled bookings
        cancelled = db.query(Booking).filter(
            Booking.customer_id == customer_id,
            Booking.status == BookingStatus.CANCELLED
        ).order_by(Booking.start_datetime.desc()).all()

        return ScheduleResponse(
            upcoming_bookings=[BookingResponse.model_validate(b) for b in upcoming],
            past_bookings=[BookingResponse.model_validate(b) for b in past],
            cancelled_bookings=[BookingResponse.model_validate(b) for b in cancelled]
        )