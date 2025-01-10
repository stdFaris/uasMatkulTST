# src/routes/notifications.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.schemas.notification import NotificationResponse
from src.services.notification_service import NotificationService
from src.database.session import get_db
from src.utils.deps import get_current_customer

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    unread_only: bool = False,
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
):
    """Get customer notifications"""
    return await NotificationService.get_customer_notifications(
        db,
        current_customer.id,
        unread_only
    )

@router.post("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_customer = Depends(get_current_customer)
):
    """Mark notification as read"""
    try:
        return await NotificationService.mark_notification_read(
            db,
            notification_id,
            current_customer.id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))