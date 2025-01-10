# src/services/partner_service.py
from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.partner import Partner
from src.schemas.partner import PartnerResponse, PartnerFilter
from src.schemas.matching import MatchRequest
from src.schemas.booking import BookingStatus
from src.utils.matching import match_partners, calculate_matching_score
from datetime import datetime
from src.models.partner_availability import PartnerAvailability as PartnerAvailabilityModels
from src.schemas.schedule import PartnerAvailability as PartnerAvailabilitySchemas

class PartnerService:
    @staticmethod
    async def get_partners(
        db: Session,
        kecamatan: str,
        filters: Optional[PartnerFilter] = None
    ) -> List[PartnerResponse]:
        try:
            partners = match_partners(db, kecamatan, filters, datetime.now())
            return [PartnerResponse.model_validate(p) for p in partners]
        except Exception as e:
            logger.error(f"Error in get_partners: {str(e)}")
            raise

    @staticmethod
    async def get_partner_details(
        db: Session,
        partner_id: int
    ) -> PartnerResponse:
        partner = db.query(Partner).filter(Partner.id == partner_id).first()
        if not partner:
            raise ValueError("Partner not found")
        return PartnerResponse.model_validate(partner)

    @staticmethod
    async def search_partners(
        db: Session,
        request: MatchRequest,
        customer_preferences: Optional[dict] = None
    ) -> List[PartnerResponse]:
        # Get initial matches based on basic criteria
        partners = match_partners(
            db,
            request.kecamatan,
            request.filters,
            request.start_datetime
        )
        
        # Calculate matching scores and sort
        scored_partners = []
        for partner in partners:
            score = calculate_matching_score(
                partner,
                request,
                customer_preferences or {}
            )
            scored_partners.append((partner, score))
            
        # Sort by score descending
        scored_partners.sort(key=lambda x: x[1], reverse=True)
        
        # Return partner responses with scores
        return [
            PartnerResponse(
                **PartnerResponse.model_validate(p[0]).model_dump(),
                matching_score=p[1]
            )
            for p in scored_partners
        ]

    @staticmethod
    async def get_partner_availability(
        db: Session,
        partner_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> PartnerAvailabilitySchemas:
        # Get all bookings in the date range
        bookings = db.query(Booking).filter(
            Booking.partner_id == partner_id,
            Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED]),
            Booking.start_datetime <= end_date,
            Booking.end_datetime >= start_date
        ).all()

        # Get blocked time slots
        blocked_slots = db.query(PartnerAvailabilityModels).filter(
            PartnerAvailabilityModels.partner_id == partner_id,
            PartnerAvailabilityModels.start_time <= end_date,
            PartnerAvailabilityModels.end_time >= start_date,
            PartnerAvailabilityModels.is_blocked == True
        ).all()

        # Calculate available slots
        available_slots = []
        current = start_date
        while current < end_date:
            if 8 <= current.hour < 20:  # Business hours check
                slot_end = current + timedelta(hours=1)
                is_available = not any(
                    (b.start_datetime <= current < b.end_datetime) or
                    (b.start_datetime < slot_end <= b.end_datetime)
                    for b in bookings
                )
                if is_available:
                    available_slots.append(TimeSlot(
                        start_time=current,
                        end_time=slot_end,
                        is_available=True
                    ))
            current += timedelta(hours=1)

        return PartnerAvailabilitySchemas(
            partner_id=partner_id,
            available_slots=available_slots,
            blocked_slots=[TimeSlot(
                start_time=slot.start_time,
                end_time=slot.end_time,
                is_available=False
            ) for slot in blocked_slots]
        )