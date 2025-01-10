# src/services/matching_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from src.models.partner import Partner
from src.models.booking import Booking
from src.schemas.booking import BookingStatus
from src.schemas.matching import MatchRequest, MatchResponse
from src.schemas.partner import PartnerResponse
from src.schemas.schedule import TimeSlot
from src.utils.matching import calculate_matching_score

class MatchingService:
    @staticmethod
    async def find_matches(
        db: Session,
        request: MatchRequest,
        customer_preferences: Optional[dict] = None
    ) -> List[PartnerResponse]:
        # Base query for partners
        query = db.query(Partner).filter(
            Partner.kecamatan == request.kecamatan,
            Partner.role == request.role,
            Partner.is_active == True
        )
        
        # Apply filters from request
        if request.filters:
            if request.filters.min_rating:
                query = query.filter(Partner.rating >= request.filters.min_rating)
            if request.filters.min_experience:
                query = query.filter(Partner.experience_years >= request.filters.min_experience)
            if request.filters.max_hourly_rate:
                query = query.filter(Partner.pricing['hourly_rate'] <= request.filters.max_hourly_rate)
            if request.filters.specialization:
                query = query.filter(Partner.specializations.contains([request.filters.specialization]))
        
        # Get available partners
        available_partners = []
        partners = query.all()
        
        for partner in partners:
            # Check availability for requested time
            is_available = await ScheduleService.check_partner_availability(
                db,
                partner.id,
                request.start_datetime,
                request.start_datetime + timedelta(hours=1)  # Check initial hour
            )
            
            if is_available:
                score = calculate_matching_score(partner, request, customer_preferences or {})
                available_partners.append((partner, score))
        
        # Sort by matching score
        available_partners.sort(key=lambda x: x[1], reverse=True)
        
        # Convert to response objects
        return [
            PartnerResponse(
                **PartnerResponse.model_validate(p[0]).model_dump(),
                matching_score=score
            )
            for p, score in available_partners
        ]