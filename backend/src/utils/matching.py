# src/utils/matching.py
from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.partner import Partner
from src.schemas.partner import PartnerFilter
from datetime import datetime
from src.schemas.matching import MatchRequest
from src.schemas.booking import BookingStatus
from sqlalchemy import cast, Float, String
from sqlalchemy.sql import expression
from src.config.settings import settings

def match_partners(
    db: Session,
    kecamatan: str,
    filters: Optional[PartnerFilter],
    current_time: datetime
) -> List[Partner]:
    query = db.query(Partner).filter(Partner.kecamatan == kecamatan)
    
    if filters:
        if filters.role:
            query = query.filter(Partner.role == filters.role)
        if filters.min_rating:
            query = query.filter(Partner.rating >= filters.min_rating)
        if filters.min_experience:
            query = query.filter(Partner.experience_years >= filters.min_experience)
        if filters.max_hourly_rate:
            query = query.filter(Partner.pricing['hourly_rate'].astext.cast(Float) <= filters.max_hourly_rate)
        if filters.specialization:
            query = query.filter(Partner.specializations.any(filters.specialization))
    
    return query.all()

def calculate_matching_score(
    partner: Partner,
    request: MatchRequest,
    customer_preferences: dict
) -> float:
    score = 0.0
    weights = settings.MATCHING_SCORE_WEIGHTS
    
    # Rating score
    score += (partner.rating / 5.0) * weights["rating"]
    
    # Experience score
    max_experience = 20  # Assume 20 years is maximum
    score += (min(partner.experience_years, max_experience) / max_experience) * weights["experience"]
    
    # Availability score
    availability_score = calculate_availability_score(partner, request.start_datetime)
    score += availability_score * weights["availability"]
    
    # Reviews score
    reviews_weight = calculate_reviews_weight(partner.total_reviews)
    score += reviews_weight * weights["reviews"]
    
    return score

def calculate_availability_score(partner: Partner, start_datetime: datetime) -> float:
    """Calculate availability score based on partner's schedule"""
    # Ensure both datetimes are timezone-aware
    start_datetime = start_datetime.astimezone()
    
    has_conflicts = any(
        booking for booking in partner.bookings
        if booking.status != BookingStatus.CANCELLED and
        booking.start_datetime.astimezone().date() == start_datetime.date()
    )
    
    if has_conflicts:
        return 0.0
    
    # Check if partner has nearby bookings (within 2 hours)
    nearby_bookings = [
        booking for booking in partner.bookings
        if booking.status != BookingStatus.CANCELLED and
        abs((booking.start_datetime.astimezone() - start_datetime).total_seconds()) <= 7200
    ]
    
    if nearby_bookings:
        return 0.5
        
    return 1.0

def calculate_reviews_weight(total_reviews: int) -> float:
    """Calculate weight based on number of reviews"""
    if total_reviews == 0:
        return 0.5
    elif total_reviews < 10:
        return 0.7
    elif total_reviews < 50:
        return 0.9
    else:
        return 1.0
