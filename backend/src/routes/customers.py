# src/routes/customers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from src.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse, CustomerPreferences
from src.schemas.dashboard import CustomerDashboard
from src.services.customer_service import CustomerService
from src.database.session import get_db
from src.utils.deps import get_current_customer
from fastapi.responses import JSONResponse
from fastapi import Query
from src.schemas.enums import PartnerRole

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/register", response_model=CustomerResponse)
async def register_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    """Register a new customer"""
    try:
        return await CustomerService.create_customer(db, customer)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/profile", response_model=CustomerResponse)
async def get_profile(
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
):
    """Get customer profile"""
    try:
        return await CustomerService.get_customer(db, current_customer.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/profile", response_model=CustomerResponse)
async def update_profile(
    customer_update: CustomerUpdate,
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
):
    """Update customer profile"""
    try:
        return await CustomerService.update_customer(
            db, 
            current_customer.id, 
            customer_update
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/preferences", response_model=CustomerResponse)
async def update_preferences(
    preferences: CustomerPreferences,
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
):
    """Update customer preferences"""
    try:
        return await CustomerService.update_preferences(
            db,
            current_customer.id,
            preferences
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/dashboard", response_model=CustomerDashboard)
async def get_dashboard(
    role_filter: Optional[List[PartnerRole]] = Query(None),
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
):
    try:
        dashboard_data = await CustomerService.get_dashboard(
            db, 
            current_customer.id,
            role_filter
        )
        return dashboard_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )