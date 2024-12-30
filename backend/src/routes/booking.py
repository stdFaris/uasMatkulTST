# src/routes/booking.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..config.database import get_db
from ..services.auth import get_current_user
from ..services.booking import BookingService
from ..schemas.booking import (
    BookingCreate,
    BookingResponse,
    BookingStatusUpdate
)
from ..models.customer import UserRole

router = APIRouter()

@router.post("", response_model=BookingResponse)
async def create_booking(
    booking_data: BookingCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != UserRole.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customers can create bookings"
        )
    
    booking_service = BookingService(db)
    return booking_service.create_booking(current_user.id, booking_data.dict())

@router.put("/{booking_id}/status", response_model=BookingResponse)
async def update_booking_status(
    booking_id: int,
    status_update: BookingStatusUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    booking_service = BookingService(db)
    return booking_service.update_booking_status(
        booking_id,
        status_update.status,
        current_user.id,
        current_user.role == UserRole.PARTNER
    )