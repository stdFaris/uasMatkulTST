# src/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from src.schemas.auth import UserAuth, Token, RefreshToken
from src.schemas.customer import CustomerBase
from src.services.auth_service import AuthService
from src.database.session import get_db
from src.utils.deps import get_current_customer
from src.models.customer import Customer

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
async def login(
    auth_data: UserAuth,
    db: Session = Depends(get_db)
):
    """Login endpoint for customers"""
    customer = await AuthService.authenticate_customer(db, auth_data.email, auth_data.password)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    return await AuthService.create_tokens(customer)

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: RefreshToken,
    db: Session = Depends(get_db)
):
    """Refresh access token"""
    try:
        return await AuthService.refresh_token(db, refresh_token.refresh_token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

@router.get("/me", response_model=CustomerBase)
async def get_current_user_info(
    current_customer: Customer = Depends(get_current_customer),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user's information
    """
    return current_customer