# backend/src/seed/seed_data.py
from datetime import datetime, time, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..models.location import Province, Regency, District, Village
from ..models.customer import Customer, UserRole, BookingStatus, BookingType
from ..models.partner import Partner, ServiceArea, PartnerSchedule, Gender
from ..models.booking import Booking, Review

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_database(db: Session):
    # Seed locations
    provinces = [
        Province(name="DKI Jakarta", code="31"),
        Province(name="Jawa Barat", code="32")
    ]
    db.add_all(provinces)
    db.commit()

    regencies = [
        Regency(name="Jakarta Selatan", code="3171", province_id=1),
        Regency(name="Jakarta Pusat", code="3172", province_id=1),
        Regency(name="Bandung", code="3273", province_id=2)
    ]
    db.add_all(regencies)
    db.commit()

    districts = [
        District(name="Kebayoran Baru", code="3171010", regency_id=1),
        District(name="Menteng", code="3172010", regency_id=2),
        District(name="Coblong", code="3273010", regency_id=3)
    ]
    db.add_all(districts)
    db.commit()

    # Seed customers
    customers = [
        Customer(
            email="john@example.com",
            hashed_password=pwd_context.hash("password123"),
            full_name="John Doe",
            phone="+6281234567890",
            is_active=True,
            role=UserRole.CUSTOMER
        ),
        Customer(
            email="jane@example.com", 
            hashed_password=pwd_context.hash("password123"),
            full_name="Jane Smith",
            phone="+6281234567891",
            is_active=True,
            role=UserRole.CUSTOMER
        )
    ]
    db.add_all(customers)
    db.commit()

    # Seed partners
    partners = [
        Partner(
            email="partner1@example.com",
            hashed_password=pwd_context.hash("password123"),
            full_name="Alice Wilson",
            phone="+6281234567892",
            is_active=True,
            is_verified=True,
            role=UserRole.PARTNER,
            gender=Gender.FEMALE,
            rating=4.5,
            total_reviews=10,
            bio="Professional caregiver with 5 years experience",
            specializations="Elderly care, Special needs care"
        ),
        Partner(
            email="partner2@example.com",
            hashed_password=pwd_context.hash("password123"),
            full_name="Bob Brown",
            phone="+6281234567893",
            is_active=True,
            is_verified=True,
            role=UserRole.PARTNER,
            gender=Gender.MALE,
            rating=4.8,
            total_reviews=15,
            bio="Experienced in elderly care",
            specializations="Elderly care, Physiotherapy assistance"
        )
    ]
    db.add_all(partners)
    db.commit()

    # Seed service areas
    service_areas = [
        ServiceArea(partner_id=1, province_id=1, regency_id=1, district_id=1),
        ServiceArea(partner_id=2, province_id=1, regency_id=2, district_id=2)
    ]
    db.add_all(service_areas)
    db.commit()

    # Seed schedules
    schedules = []
    for partner_id in [1, 2]:
        for day in range(7):  # Monday to Sunday
            schedules.append(
                PartnerSchedule(
                    partner_id=partner_id,
                    day_of_week=day,
                    start_time=time(8, 0),  # 8 AM
                    end_time=time(17, 0),   # 5 PM
                    is_available=True
                )
            )
    db.add_all(schedules)
    db.commit()

    # Seed bookings and reviews
    bookings = [
        Booking(
            customer_id=1,
            partner_id=1,
            booking_type=BookingType.HOURLY,
            status=BookingStatus.COMPLETED,
            start_datetime=datetime.utcnow() - timedelta(days=7),
            end_datetime=datetime.utcnow() - timedelta(days=7, hours=-4),
            duration_hours=4,
            total_price=200.0,
            notes="Please bring medical equipment"
        ),
        Booking(
            customer_id=2,
            partner_id=2,
            booking_type=BookingType.DAILY,
            status=BookingStatus.CONFIRMED,
            start_datetime=datetime.utcnow() + timedelta(days=1),
            end_datetime=datetime.utcnow() + timedelta(days=2),
            total_price=300.0
        )
    ]
    db.add_all(bookings)
    db.commit()

    reviews = [
        Review(
            booking_id=1,
            customer_id=1,
            partner_id=1,
            rating=5,
            comment="Excellent service and very professional"
        )
    ]
    db.add_all(reviews)
    db.commit()