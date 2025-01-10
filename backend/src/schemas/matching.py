# src/schemas/matching.py
from pydantic import BaseModel, confloat
from typing import List, Optional
from datetime import datetime
from .partner import PartnerResponse, PartnerFilter
from .enums import BookingType, PartnerRole
from enum import Enum


class MatchSortCriteria(str, Enum):
    RATING = "rating"
    EXPERIENCE = "experience" 
    PRICE = "price"

class MatchRequest(BaseModel):
    start_datetime: datetime
    kecamatan: str
    role: PartnerRole
    booking_type: BookingType
    filters: PartnerFilter
    sort_by: MatchSortCriteria

class MatchResponse(BaseModel):
    recommended_partners: List[PartnerResponse]
    matching_score: float
    availability_confirmed: bool