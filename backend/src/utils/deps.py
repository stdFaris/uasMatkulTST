# src/utils/deps.py
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from src.models.customer import Customer
from src.database.session import get_db
from src.config.settings import settings
from src.schemas.booking import BookingStatus

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_customer(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Customer:
    """
    Dependency to get the current authenticated customer from the JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        customer_id: str = payload.get("sub")
        if customer_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    customer = db.query(Customer).filter(
        Customer.id == int(customer_id),
        Customer.is_active == True
    ).first()
    
    if customer is None:
        raise credentials_exception
        
    # Update last login time
    customer.last_login = datetime.now()
    db.commit()
    
    return customer

async def get_current_active_customer(
    current_customer: Customer = Depends(get_current_customer)
) -> Customer:
    """
    Dependency to ensure the customer is active
    """
    if not current_customer.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive customer"
        )
    return current_customer

async def check_booking_limits(
    db: Session = Depends(get_db),
    current_customer: Customer = Depends(get_current_customer)
) -> None:
    """
    Dependency to check if customer has reached maximum active bookings
    """
    active_bookings = db.query(Booking).filter(
        Booking.customer_id == current_customer.id,
        Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED])
    ).count()
    
    if active_bookings >= settings.MAXIMUM_ACTIVE_BOOKINGS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maximum active bookings ({settings.MAXIMUM_ACTIVE_BOOKINGS}) reached"
        )
