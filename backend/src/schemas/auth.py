# src/schemas/auth.py
from pydantic import BaseModel, EmailStr, constr

class UserAuth(BaseModel):
    email: EmailStr
    password: constr(min_length=8)

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshToken(BaseModel):
    refresh_token: str