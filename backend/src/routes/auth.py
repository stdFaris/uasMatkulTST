# src/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from ..config.database import get_db
from ..config.settings import Settings
from ..schemas.auth import Token, LoginRequest
from ..services.auth import verify_password, create_access_token
from ..models.customer import Customer
from ..models.partner import Partner

settings = Settings()
router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Try to find user in both customer and partner tables
    user = db.query(Customer).filter(Customer.email == form_data.username).first()
    is_partner = False
    
    if not user:
        user = db.query(Partner).filter(Partner.email == form_data.username).first()
        is_partner = True
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "role": "partner" if is_partner else "customer"
        },
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}