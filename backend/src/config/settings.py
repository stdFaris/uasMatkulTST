# src/config/settings.py
from pydantic_settings import BaseSettings
from datetime import timedelta
from typing import Dict, ClassVar

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str
    
    # JWT Settings
    JWT_SECRET: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE: int = 30
    REFRESH_TOKEN_EXPIRE: int = 7
    
    # Business Rules
    MAX_HOURLY_DURATION: int = 6
    MAX_DAILY_DURATION: int = 7
    BREAK_DURATION: int = 1
    NOTIFICATION_REMINDER: int = 30
    
    MINIMUM_CANCELLATION_NOTICE: int = 2
    MAXIMUM_ACTIVE_BOOKINGS: int = 3
    RATING_COOLDOWN: int = 24
    MAX_FAILED_LOGIN_ATTEMPTS: int = 5
    ACCOUNT_LOCKOUT_DURATION: int = 30
    PASSWORD_RESET_TIMEOUT: int = 15
    
    MATCHING_SCORE_WEIGHTS: Dict[str, float] = {
        "rating": 0.3,
        "experience": 0.2,
        "availability": 0.3,
        "reviews": 0.2
    }
    
    NOTIFICATION_TYPES: ClassVar[Dict[str, Dict[str, str]]] = {
        "BOOKING_REMINDER": {
            "title": "Upcoming Booking Reminder",
            "template": "Your booking with {partner_name} starts in 30 minutes"
        },
        "BOOKING_CONFIRMATION": {
            "title": "Booking Confirmed",
            "template": "Your booking with {partner_name} has been confirmed"
        },
        "SCHEDULE_CHANGE": {
            "title": "Schedule Change",
            "template": "Your booking schedule has been updated"
        },
        "PARTNER_UNAVAILABLE": {
            "title": "Partner Unavailable",
            "template": "Your partner is no longer available for the scheduled time"
        }
    }
    
    class Config:
        env_file = ".env"

settings = Settings()