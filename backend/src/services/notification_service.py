# src/services/notification_service.py
from typing import List
from sqlalchemy.orm import Session
from src.models.notification import Notification
from src.schemas.notification import NotificationResponse

class NotificationService:
    @staticmethod
    async def get_customer_notifications(
        db: Session,
        customer_id: int,
        unread_only: bool = False
    ) -> List[NotificationResponse]:
        query = db.query(Notification).filter(
            Notification.customer_id == customer_id
        )
        
        if unread_only:
            query = query.filter(Notification.is_read == False)
            
        notifications = query.order_by(
            Notification.created_at.desc()
        ).all()
        
        return [NotificationResponse.model_validate(n) for n in notifications]

    @staticmethod
    async def mark_notification_read(
        db: Session,
        notification_id: int,
        customer_id: int
    ) -> NotificationResponse:
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.customer_id == customer_id
        ).first()
        
        if not notification:
            raise ValueError("Notification not found")
            
        notification.is_read = True
        db.commit()
        db.refresh(notification)
        
        return NotificationResponse.model_validate(notification)
