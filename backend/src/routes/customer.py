# src/routes/customer.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..config.database import get_db
from ..services.auth import get_current_user
from ..services.customer import CustomerService
from ..schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    BookingResponse,
    ReviewCreate,
    ReviewResponse
)
from ..models.customer import BookingStatus

router = APIRouter()

@router.post("", response_model=CustomerResponse)
async def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):
    customer_service = CustomerService(db)
    return customer_service.create_customer(customer_data.dict())

@router.put("/me", response_model=CustomerResponse)
async def update_customer(
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    customer_service = CustomerService(db)
    return customer_service.update_customer(current_user.id, customer_data.dict(exclude_unset=True))

@router.get("/me/bookings", response_model=List[BookingResponse])
async def get_customer_bookings(
    status: Optional[BookingStatus] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    customer_service = CustomerService(db)
    return customer_service.get_customer_bookings(current_user.id, status, skip, limit)

@router.post("/bookings/{booking_id}/reviews", response_model=ReviewResponse)
async def create_booking_review(
    booking_id: int,
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    customer_service = CustomerService(db)
    return customer_service.create_review(current_user.id, booking_id, review_data.dict())
