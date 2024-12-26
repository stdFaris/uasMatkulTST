from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.database import get_db
from models.user import User, UserRole
from schemas.user import UserCreate, UserLogin, Token, CustomerProfileCreate
from utils.auth import verify_password, create_access_token, get_password_hash
from datetime import timedelta
from config.settings import settings

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup", response_model=Token)
async def signup(user_data: UserCreate, profile_data: CustomerProfileCreate, db: Session = Depends(get_db)):
    if user_data.role != UserRole.CUSTOMER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only customer registration is allowed"
        )
    
    # Check if user exists
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(email=user_data.email, password=hashed_password, role=UserRole.CUSTOMER)
    db.add(db_user)
    db.flush()
    
    # Create customer profile
    db_profile = CustomerProfile(
        user_id=db_user.id,
        location=profile_data.location,
        balance=0.0
    )
    db.add(db_profile)
    db.commit()
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.email, "role": UserRole.CUSTOMER},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}