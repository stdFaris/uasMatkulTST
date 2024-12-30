# src/services/booking.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Optional, List
from ..models.customer import Booking, BookingStatus, BookingType
from ..models.partner import Partner, PartnerSchedule, PartnerAvailability

class BookingService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_booking(self, customer_id: int, booking_data: dict) -> Booking:
        try:
            # Validate partner exists and is active
            partner = self.db.query(Partner).filter(
                Partner.id == booking_data["partner_id"],
                Partner.is_active == True,
                Partner.is_verified == True
            ).first()
            
            if not partner:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Partner not found or not available"
                )
            
            # Add transaction handling
            with self.db.begin():
                booking = Booking(
                    customer_id=customer_id,
                    end_datetime=self._calculate_end_datetime(
                        booking_data["start_datetime"],
                        booking_data["booking_type"],
                        booking_data.get("duration_hours")
                    ),
                    total_price=self._calculate_price(
                        partner,
                        booking_data["booking_type"],
                        booking_data.get("duration_hours")
                    ),
                    **booking_data
                )
                
                self.db.add(booking)
                self.db.flush()
                
                # Update partner availability
                self._update_partner_availability(booking)
                
                return booking
                
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error occurred"
            ) from e
            
    
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
        partner: Partner,
        booking_type: BookingType,
        duration_hours: Optional[int] = None
    ) -> float:
        # Implement your pricing logic here
        base_rates = {
            BookingType.HOURLY: 50.0,  # per hour
            BookingType.DAILY: 300.0,  # per day
            BookingType.MONTHLY: 8000.0  # per month
        }
        
        if booking_type == BookingType.HOURLY:
            return base_rates[booking_type] * duration_hours
        return base_rates[booking_type]
    
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
