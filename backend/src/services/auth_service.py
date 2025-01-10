# src/services/auth_service.py
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.models.customer import Customer
from src.schemas.auth import UserAuth, Token, RefreshToken
from src.utils.auth import verify_password, create_access_token, decode_token
from typing import Optional
from src.config.settings import settings

class AuthService:
    @staticmethod
    async def authenticate_customer(
        db: Session,
        email: str,
        password: str
    ) -> Optional[Customer]:
        customer = db.query(Customer).filter(Customer.email == email).first()
        if not customer or not verify_password(password, customer.hashed_password):
            return None
        return customer

    @staticmethod
    async def create_tokens(customer: Customer) -> Token:
        access_token = create_access_token(
            data={"sub": str(customer.id), "type": "access"},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
        )
        refresh_token = create_access_token(
            data={"sub": str(customer.id), "type": "refresh"},
            expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE)
        )
        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        )

    @staticmethod
    async def refresh_token(
        db: Session,
        refresh_token: str
    ) -> Token:
        try:
            payload = decode_token(refresh_token)
            if payload.get("type") != "refresh":
                raise ValueError("Invalid token type")
                
            customer_id = int(payload.get("sub"))
            customer = db.query(Customer).filter(Customer.id == customer_id).first()
            
            if not customer:
                raise ValueError("Customer not found")
                
            return await AuthService.create_tokens(customer)
        except Exception as e:
            raise ValueError(f"Invalid refresh token: {str(e)}")