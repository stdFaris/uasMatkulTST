# src/services/customer.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from ..models.customer import Customer, Review, Booking, BookingStatus
from ..utils.auth import get_password_hash

class CustomerService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_customer(self, customer_data: dict) -> Customer:
        # Check if email already exists
        if self.db.query(Customer).filter(Customer.email == customer_data["email"]).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        customer_data["hashed_password"] = get_password_hash(customer_data.pop("password"))
        
        # Create customer
        customer = Customer(**customer_data)
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        
        return customer
    
    def update_customer(self, customer_id: int, customer_data: dict) -> Customer:
        customer = self.db.query(Customer).get(customer_id)
        
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        
        # Handle password update
        if "password" in customer_data:
            customer_data["hashed_password"] = get_password_hash(customer_data.pop("password"))
        
        # Update customer fields
        for key, value in customer_data.items():
            setattr(customer, key, value)
        
        self.db.commit()
        self.db.refresh(customer)
        
        return customer
    
    def get_customer_bookings(
        self,
        customer_id: int,
        status: Optional[BookingStatus] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Booking]:
        query = self.db.query(Booking).filter(Booking.customer_id == customer_id)
        
        if status:
            query = query.filter(Booking.status == status)
        
        return query.order_by(Booking.created_at.desc()).offset(skip).limit(limit).all()
    
    def create_review(self, customer_id: int, booking_id: int, review_data: dict) -> Review:
        # Verify booking
        booking = self.db.query(Booking).filter(
            Booking.id == booking_id,
            Booking.customer_id == customer_id,
            Booking.status.in_([BookingStatus.COMPLETED, BookingStatus.TERMINATED])
        ).first()
        
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Valid completed booking not found"
            )
        
        # Check if review already exists
        if self.db.query(Review).filter(Review.booking_id == booking_id).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Review already exists"
            )
        
        # Create review
        review = Review(
            booking_id=booking_id,
            customer_id=customer_id,
            partner_id=booking.partner_id,
            **review_data
        )
        
        self.db.add(review)
        
        # Update partner rating if rating provided
        if review.rating:
            partner = booking.partner
            total_reviews = partner.total_reviews + 1
            partner.rating = ((partner.rating * partner.total_reviews) + review.rating) / total_reviews
            partner.total_reviews = total_reviews
        
        self.db.commit()
        self.db.refresh(review)
        
        return review