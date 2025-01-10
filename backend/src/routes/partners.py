# src/routes/partners.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from src.schemas.partner import PartnerResponse, PartnerFilter
from src.schemas.matching import MatchRequest, MatchResponse
from src.schemas.schedule import PartnerAvailability
from src.schemas.enums import PartnerRole, BookingType
from src.services.partner_service import PartnerService
from src.database.session import get_db
from src.utils.deps import get_current_customer

router = APIRouter(prefix="/partners", tags=["Partners"])

@router.get("/search", response_model=List[PartnerResponse])
async def search_partners(
    kecamatan: str,
    role: Optional[PartnerRole] = None,
    min_rating: Optional[float] = None,
    min_experience: Optional[int] = None,
    max_hourly_rate: Optional[float] = None,
    specialization: Optional[str] = None,
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
):
    """Search partners with filters"""
    filters = PartnerFilter(
        role=role,
        min_rating=min_rating,
        min_experience=min_experience,
        max_hourly_rate=max_hourly_rate,
        specialization=specialization
    )
    
    try:
        partners = await PartnerService.get_partners(db, kecamatan, filters)
        return partners
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error searching partners"
        )

@router.post("/match", response_model=List[PartnerResponse])
async def match_partners(
    request: MatchRequest,
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
):
    """Get matched partners based on criteria"""
    return await PartnerService.search_partners(db, request)

@router.get("/{partner_id}", response_model=PartnerResponse)
async def get_partner_details(
    partner_id: int,
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
):
    """Get detailed partner information"""
    try:
        return await PartnerService.get_partner_details(db, partner_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{partner_id}/availability", response_model=PartnerAvailability)
async def get_partner_availability(
    partner_id: int,
    start_date: datetime,
    end_date: datetime,
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
):
    """Get partner availability schedule"""
    return await PartnerService.get_partner_availability(
        db,
        partner_id,
        start_date,
        end_date
    )