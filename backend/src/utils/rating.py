# src/utils/rating.py
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.models.partner import Partner
from src.config.settings import settings
def update_partner_rating(
    db: Session,
    partner_id: int,
    new_rating: float
) -> None:
    """
    Update partner rating when new review is added
    """
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        raise ValueError("Partner not found")
        
    total_reviews = partner.total_reviews + 1
    current_rating = partner.rating
    
    # Calculate new weighted rating
    new_average = ((current_rating * partner.total_reviews) + new_rating) / total_reviews
    
    partner.rating = round(new_average, 2)
    partner.total_reviews = total_reviews
    db.commit()
