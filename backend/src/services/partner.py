# src/services/partner.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from ..models.partner import Partner, ServiceArea, PartnerSchedule
from ..models.customer import BookingStatus
from ..models.booking import Booking
from ..utils.auth import get_password_hash

class PartnerService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_partner(self, partner_data: dict) -> Partner:
        # Check if email already exists
        if self.db.query(Partner).filter(Partner.email == partner_data["email"]).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        partner_data["hashed_password"] = get_password_hash(partner_data.pop("password"))
        
        # Validate gender
        if "gender" not in partner_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Gender is required"
            )
        
        # Create partner
        partner = Partner(**partner_data)
        self.db.add(partner)
        self.db.commit()
        self.db.refresh(partner)
        
        return partner

    
    def update_partner(self, partner_id: int, partner_data: dict) -> Partner:
        partner = self.db.query(Partner).get(partner_id)
        
        if not partner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Partner not found"
            )
        
        # Handle password update
        if "password" in partner_data:
            partner_data["hashed_password"] = get_password_hash(partner_data.pop("password"))
        
        # Update partner fields
        for key, value in partner_data.items():
            setattr(partner, key, value)
        
        self.db.commit()
        self.db.refresh(partner)
        
        return partner
    
    def add_service_area(self, partner_id: int, area_data: dict) -> ServiceArea:
        service_area = ServiceArea(partner_id=partner_id, **area_data)
        self.db.add(service_area)
        self.db.commit()
        self.db.refresh(service_area)
        return service_area
    
    def update_schedule(self, partner_id: int, schedule_data: List[dict]) -> List[PartnerSchedule]:
        # Delete existing schedule
        self.db.query(PartnerSchedule).filter(
            PartnerSchedule.partner_id == partner_id
        ).delete()
        
        # Create new schedule
        schedules = [PartnerSchedule(partner_id=partner_id, **data) for data in schedule_data]
        self.db.add_all(schedules)
        self.db.commit()
        
        return schedules
    
    def get_partner_bookings(
        self,
        partner_id: int,
        status: Optional[BookingStatus] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Booking]:
        query = self.db.query(Booking).filter(Booking.partner_id == partner_id)
        
        if status:
            query = query.filter(Booking.status == status)
        
        return query.order_by(Booking.created_at.desc()).offset(skip).limit(limit).all()
