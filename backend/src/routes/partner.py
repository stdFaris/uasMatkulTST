# src/routes/partner.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..config.database import get_db
from ..services.auth import get_current_user
from ..services.partner import PartnerService
from ..schemas.partner import (
    PartnerCreate,
    PartnerUpdate,
    PartnerResponse,
    ServiceAreaCreate,
    ServiceAreaResponse,
    ScheduleCreate,
    ScheduleResponse,
    BookingResponse
)
from ..models.customer import BookingStatus, UserRole

router = APIRouter()

@router.post("", response_model=PartnerResponse)
async def create_partner(
    partner_data: PartnerCreate,
    db: Session = Depends(get_db)
):
    partner_service = PartnerService(db)
    return partner_service.create_partner(partner_data.dict())

@router.put("/me", response_model=PartnerResponse)
async def update_partner(
    partner_data: PartnerUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != UserRole.PARTNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only partners can update their profiles"
        )
    partner_service = PartnerService(db)
    return partner_service.update_partner(current_user.id, partner_data.dict(exclude_unset=True))

@router.post("/me/service-areas", response_model=ServiceAreaResponse)
async def add_service_area(
    area_data: ServiceAreaCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != UserRole.PARTNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only partners can add service areas"
        )
    partner_service = PartnerService(db)
    return partner_service.add_service_area(current_user.id, area_data.dict())

@router.put("/me/schedule", response_model=List[ScheduleResponse])
async def update_schedule(
    schedule_data: List[ScheduleCreate],
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != UserRole.PARTNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only partners can update their schedule"
        )
    partner_service = PartnerService(db)
    return partner_service.update_schedule(current_user.id, [s.dict() for s in schedule_data])

@router.get("/me/bookings", response_model=List[BookingResponse])
async def get_partner_bookings(
    status: Optional[BookingStatus] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != UserRole.PARTNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only partners can view their bookings"
        )
    partner_service = PartnerService(db)
    return partner_service.get_partner_bookings(current_user.id, status, skip, limit)
