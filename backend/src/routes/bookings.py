# src/routes/bookings.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from src.schemas.booking import BookingCreate, BookingResponse, BookingCancel
from src.schemas.schedule import ScheduleResponse
from src.services.booking_service import BookingService
from src.database.session import get_db
from src.utils.deps import get_current_customer

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingResponse)
async def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
):
    """Create a new booking"""
    try:
        return await BookingService.create_booking(db, current_customer.id, booking)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[BookingResponse])
async def get_bookings(
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
):
    """Get all customer bookings"""
    return await BookingService.get_customer_bookings(db, current_customer.id)

@router.post("/{booking_id}/cancel", response_model=BookingResponse)
async def cancel_booking(
    booking_id: int,
    cancellation: BookingCancel,
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
):
    """Cancel a booking"""
    try:
        return await BookingService.cancel_booking(
            db,
            booking_id,
            current_customer.id,
            cancellation.reason
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{booking_id}/reschedule", response_model=BookingResponse)
async def reschedule_booking(
    booking_id: int,
    new_start_datetime: datetime,
    new_end_datetime: datetime,
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
):
    """Reschedule a booking"""
    try:
        return await BookingService.reschedule_booking(
            db,
            booking_id,
            current_customer.id,
            new_start_datetime,
            new_end_datetime
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/schedule", response_model=ScheduleResponse)
async def get_schedule(
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
):
    """Get customer schedule summary"""
    return await BookingService.get_schedule_summary(db, current_customer.id)