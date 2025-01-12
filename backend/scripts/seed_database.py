from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from src.models.partner import Partner
from src.models.partner_availability import PartnerAvailability
from src.schemas.partner import PartnerRole
from src.models.base import Base
from src.config.settings import settings

# Import the dummy data generator functions
from dummy_data import generate_partner_data, generate_partner_availability

def seed_database():
    # Create database engine using settings
    engine = create_engine(settings.DATABASE_URL)
    
    # Create all tables (if they don't exist)
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    session = Session(engine)
    
    try:
        # Check if partners already exist
        existing_partners = session.query(Partner).count()
        if existing_partners > 0:
            print(f"Database already contains {existing_partners} partners. Skipping seeding.")
            return
        
        # Generate dummy partner data
        partner_data = generate_partner_data(100)
        
        print("Starting to seed partners...")
        # Insert partners
        for i, data in enumerate(partner_data, 1):
            partner = Partner(
                full_name=data['full_name'],
                role=PartnerRole[data['role']],
                experience_years=data['experience_years'],
                rating=data['rating'],
                total_reviews=data['total_reviews'],
                specializations=data['specializations'],
                pricing=data['pricing'],
                kecamatan=data['kecamatan'],
                is_available=data['is_available']
            )
            session.add(partner)
            session.flush()  # To get the partner ID
            
            # Generate and insert availability for each partner
            availabilities = generate_partner_availability(partner.id)
            for avail in availabilities:
                availability = PartnerAvailability(
                    partner_id=avail['partner_id'],
                    start_time=avail['start_time'],
                    end_time=avail['end_time'],
                    is_blocked=avail['is_blocked']
                )
                session.add(availability)
            
            if i % 10 == 0:  # Progress update every 10 partners
                print(f"Processed {i} partners...")
        
        # Commit all changes
        session.commit()
        print("Successfully seeded the database!")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()