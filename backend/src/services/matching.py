# src/services/matching.py
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..models.partner import Partner, PartnerSchedule, ServiceArea
from ..models.booking import Booking, Review
from datetime import datetime, timedelta
from typing import List, Optional

class PartnerMatchingService:
    def __init__(self, db: Session):
        self.db = db
    
    def find_best_partners(self, booking_data: dict, limit: int = 5) -> List[Partner]:
        """Find best matching partners based on multiple criteria."""
        query = self.db.query(Partner).filter(
            Partner.is_active == True,
            Partner.is_verified == True
        )
        
        # Filter by service area
        query = query.join(Partner.service_areas).filter(
            ServiceArea.district_id == booking_data.get('district_id')
        )
        
        # Filter by availability
        day_of_week = booking_data['start_datetime'].weekday()
        start_time = booking_data['start_datetime'].time()
        
        query = query.join(Partner.schedules).filter(
            PartnerSchedule.day_of_week == day_of_week,
            PartnerSchedule.start_time <= start_time,
            PartnerSchedule.end_time >= start_time,
            PartnerSchedule.is_available == True
        )
        
        # Calculate partner scores
        query = query.add_columns(
            (Partner.rating * 0.4 +  # 40% weight for rating
             Partner.total_reviews * 0.3 +  # 30% weight for experience
             func.random() * 0.3  # 30% weight for randomization
            ).label('score')
        ).order_by('score DESC')
        
        return query.limit(limit).all()
