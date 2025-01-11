# src/services/customer_service.py
from math import ceil
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone
from typing import List, Optional
from src.models.customer import Customer
from src.models.booking import Booking
from src.models.notification import Notification
from src.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse, CustomerPreferences
from src.utils.auth import get_password_hash
from src.schemas.dashboard import CustomerDashboard
from src.schemas.booking import BookingStatus, BookingResponse
from src.schemas.enums import BookingType, PartnerRole
from src.schemas.matching import MatchRequest, MatchSortCriteria
from src.schemas.partner import PartnerFilter
from src.schemas.notification import NotificationResponse
from datetime import datetime
from .partner_service import PartnerService
from src.schemas.dashboard import DashboardStats

class CustomerService:
    @staticmethod
    async def create_customer(
        db: Session,
        customer: CustomerCreate
    ) -> CustomerResponse:
        db_customer = Customer(
            email=customer.email,
            hashed_password=get_password_hash(customer.password),
            full_name=customer.full_name,
            phone=customer.phone,
            kecamatan=customer.kecamatan
        )
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return CustomerResponse.model_validate(db_customer)

    async def get_customer(
        db: Session,
        customer_id: int
    ) -> CustomerResponse:
        """Get customer by ID"""
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise ValueError("Customer not found")
        return CustomerResponse.model_validate(customer)

    @staticmethod
    async def update_customer(
        db: Session,
        customer_id: int,
        customer_update: CustomerUpdate
    ) -> CustomerResponse:
        db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
        update_data = customer_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_customer, field, value)
            
        db.commit()
        db.refresh(db_customer)
        return CustomerResponse.model_validate(db_customer)

    @staticmethod
    async def update_preferences(
        db: Session,
        customer_id: int,
        preferences: CustomerPreferences
    ) -> CustomerResponse:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise ValueError("Customer not found")

        # Update preferences
        customer.preferences = preferences.model_dump()
        db.commit()
        db.refresh(customer)
        return CustomerResponse.model_validate(customer)
    
    @staticmethod
    async def get_dashboard(
        db: Session,
        customer_id: int,
        role_filter: Optional[List[PartnerRole]] = None
    ) -> CustomerDashboard:
        # Get customer and preferences
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise ValueError("Customer not found")
        
        preferences = customer.preferences or {}
        
        # Get active bookings
        active_bookings = db.query(Booking).filter(
            Booking.customer_id == customer_id,
            Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED]),
            Booking.start_datetime > datetime.now(timezone.utc)
        ).order_by(Booking.start_datetime).all()
        
        # Use provided role filter or fall back to preferences/default
        selected_roles = role_filter or \
            preferences.get('preferred_partner_roles') or \
            [PartnerRole.PEMBANTU, PartnerRole.TUKANG_KEBUN, PartnerRole.TUKANG_PIJAT]
        
        # Calculate partners per role (total 5 partners divided by number of roles)
        partners_per_role = max(1, ceil(5 / len(selected_roles)))
        
        # Create match requests and get recommended partners for each selected role
        all_recommended_partners = []
        for role in selected_roles:
            match_request = MatchRequest(
                start_datetime=datetime.now(),
                kecamatan=customer.kecamatan,
                role=role,
                booking_type=preferences.get('preferred_booking_type', BookingType.HOURLY),
                filters=PartnerFilter(
                    role=role,
                    min_rating=preferences.get('min_rating', 0),
                    min_experience=0,
                    max_hourly_rate=preferences.get('max_price_per_hour'),
                    specialization=None,
                    kecamatan=customer.kecamatan
                ),
                sort_by=MatchSortCriteria.RATING
            )
            
            # Get recommended partners for this role
            role_partners = await PartnerService.search_partners(
                db,
                match_request,
                preferences
            )
            all_recommended_partners.extend(role_partners[:partners_per_role])

        if len(all_recommended_partners) < 5:
            remaining_needed = 5 - len(all_recommended_partners)
            additional_per_role = ceil(remaining_needed / len(selected_roles))
            
            for role in selected_roles:
                if len(all_recommended_partners) >= 5:
                    break
                    
                match_request.filters.min_rating = 0  # Relax rating requirement
                match_request.filters.max_hourly_rate = None  # Relax price requirement
                
                additional_partners = await PartnerService.search_partners(
                    db,
                    match_request,
                    preferences
                )
                
                # Add partners we haven't already included
                existing_ids = {p.id for p in all_recommended_partners}
                new_partners = [p for p in additional_partners if p.id not in existing_ids]
                all_recommended_partners.extend(new_partners[:additional_per_role])
        
        # Sort combined results by rating and limit to 5
        all_recommended_partners.sort(key=lambda x: x.rating, reverse=True)
        recommended_partners = all_recommended_partners[:5]
        
        # Get recent notifications
        recent_notifications = db.query(Notification).filter(
            Notification.customer_id == customer_id
        ).order_by(Notification.created_at.desc()).limit(5).all()
        
        # Calculate stats
        completed_bookings = db.query(Booking).filter(
            Booking.customer_id == customer_id,
            Booking.status == BookingStatus.COMPLETED
        ).count()
        
        cancelled_bookings = db.query(Booking).filter(
            Booking.customer_id == customer_id,
            Booking.status == BookingStatus.CANCELLED
        ).count()
        
        total_spent = db.query(func.sum(Booking.total_price)).filter(
            Booking.customer_id == customer_id,
            Booking.status == BookingStatus.COMPLETED
        ).scalar() or 0
        
        stats = DashboardStats(
            total_bookings=len(active_bookings) + completed_bookings + cancelled_bookings,
            active_bookings=len(active_bookings),
            completed_bookings=completed_bookings,
            cancelled_bookings=cancelled_bookings,
            total_spent=float(total_spent)
        )
        
        # Prepare and return dashboard response
        return CustomerDashboard(
            customer=CustomerResponse.model_validate(customer),
            upcoming_bookings=[BookingResponse.model_validate(b) for b in active_bookings[:3]],
            recommended_partners=recommended_partners,
            stats=stats,
            active_bookings=len(active_bookings),
            recent_notifications=[NotificationResponse.model_validate(n) for n in recent_notifications]
        )