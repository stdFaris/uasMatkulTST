# src/schemas/matching_result.py
from pydantic import BaseModel
from typing import List
from .partner import PartnerResponse

class MatchingResult(BaseModel):
    partners: List[PartnerResponse]
    matching_score: float