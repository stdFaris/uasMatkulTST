# src/services/review_service.py
from sqlalchemy.orm import Session
from src.models.review import Review
from src.models.booking import Booking
from src.schemas.booking import BookingStatus
from src.schemas.review import ReviewCreate, ReviewResponse
from src.utils.rating import update_partner_rating
from typing import Optional

class ReviewService:
    @staticmethod
    async def create_review(
        db: Session,
        customer_id: int,
        review: ReviewCreate
    ) -> ReviewResponse:
        # Verify booking exists and belongs to customer
        booking = db.query(Booking).filter(
            Booking.id == review.booking_id,
            Booking.customer_id == customer_id,
            Booking.status == BookingStatus.COMPLETED
        ).first()
        
        if not booking:
            raise ValueError("Invalid booking or booking not completed")
            
        # Check if review already exists
        existing_review = db.query(Review).filter(
            Review.booking_id == review.booking_id
        ).first()
        
        if existing_review:
            raise ValueError("Review already exists for this booking")
            
        # Create review
        db_review = Review(
            booking_id=review.booking_id,
            rating=review.rating,
            comment=review.comment
        )
        
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        
        # Update partner rating
        await update_partner_rating(db, booking.partner_id, review.rating)
        
        return ReviewResponse.model_validate(db_review)

    @staticmethod
    async def get_booking_review(
        db: Session,
        booking_id: int,
        customer_id: int
    ) -> Optional[ReviewResponse]:
        review = db.query(Review).join(Booking).filter(
            Review.booking_id == booking_id,
            Booking.customer_id == customer_id
        ).first()
        
        if review:
            return ReviewResponse.model_validate(review)
        return None