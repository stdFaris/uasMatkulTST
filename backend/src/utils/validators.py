# src/utils/validators.py
import re
from typing import Optional
from datetime import datetime, time
from fastapi import HTTPException, status
from ..models.partner import Gender

class Validators:
    @staticmethod
    def validate_gender(gender: str) -> bool:
        """Validate gender value."""
        if gender not in [g.value for g in Gender]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid gender. Must be one of: {', '.join([g.value for g in Gender])}"
            )
        return True
    
    @staticmethod
    def validate_phone_number(phone: str) -> bool:
        """Validate phone number format."""
        pattern = r'^\+?[1-9]\d{1,14}$'
        if not re.match(pattern, phone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid phone number format"
            )
        return True

    @staticmethod
    def validate_password(password: str) -> bool:
        """
        Validate password strength:
        - Minimum 8 characters
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one number
        - Contains at least one special character
        """
        if len(password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long"
            )

        patterns = [
            (r'[A-Z]', "Password must contain at least one uppercase letter"),
            (r'[a-z]', "Password must contain at least one lowercase letter"),
            (r'[0-9]', "Password must contain at least one number"),
            (r'[!@#$%^&*(),.?":{}|<>]', "Password must contain at least one special character")
        ]

        for pattern, message in patterns:
            if not re.search(pattern, password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=message
                )

        return True

    @staticmethod
    def validate_booking_time(
        start_time: time,
        end_time: time,
        buffer_hours: Optional[int] = None
    ) -> bool:
        """Validate booking time constraints."""
        # Convert to datetime for easier comparison
        now = datetime.now().time()
        
        if start_time <= now:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Booking start time must be in the future"
            )

        if end_time <= start_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End time must be after start time"
            )

        if buffer_hours:
            # Calculate buffer end time
            buffer_end = datetime.combine(datetime.today(), end_time)
            buffer_end = buffer_end.time()
            
            if buffer_end <= end_time:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Must have {buffer_hours} hours buffer after booking"
                )

        return True
