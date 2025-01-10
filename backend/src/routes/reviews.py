# src/routes/reviews.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from src.schemas.review import ReviewCreate, ReviewResponse
from src.services.review_service import ReviewService
from src.database.session import get_db
from src.utils.deps import get_current_customer

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=ReviewResponse)
async def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
):
    """Create a review for a completed booking"""
    try:
        return await ReviewService.create_review(db, current_customer.id, review)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{booking_id}", response_model=Optional[ReviewResponse])
async def get_booking_review(
    booking_id: int,
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
):
    """Get review for a specific booking"""
    return await ReviewService.get_booking_review(
        db,
        booking_id,
        current_customer.id
    )