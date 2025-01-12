# src/utils/notification.py
from datetime import datetime, timedelta
from fastapi_utils.tasks import repeat_every
from src.config.settings import settings
from sqlalchemy.orm import Session
from src.models.booking import Booking
from src.schemas.notification import NotificationType, NotificationCreate
from src.models.notification import Notification

@repeat_every(seconds=60)
def check_upcoming_bookings():
    # Implementation for checking and sending notifications
    reminder_time = datetime.utcnow() + timedelta(minutes=settings.NOTIFICATION_REMINDER)
    # Query and notify users about upcoming bookings
    pass

def generate_notification_message(type: NotificationType, booking: Booking) -> str:
    """
    Generate notification message based on type and booking details with WIB timezone (+7)
    """
    # Convert UTC string to datetime and add 7 hours
    start_time = start_time = booking.start_datetime + timedelta(hours=7)
    
    messages = {
        NotificationType.BOOKING_REMINDER: (
            f"Reminder: You have an upcoming appointment with {booking.partner.full_name} "
            f"at {start_time.strftime('%H:%M')} WIB on "
            f"{start_time.strftime('%Y-%m-%d')}"
        ),
        NotificationType.SCHEDULE_CHANGE: (
            f"Your appointment with {booking.partner.full_name} has been rescheduled to "
            f"{start_time.strftime('%Y-%m-%d %H:%M')} WIB"
        ),
        NotificationType.BOOKING_CONFIRMATION: (
            f"Your appointment with {booking.partner.full_name} has been confirmed for "
            f"{start_time.strftime('%Y-%m-%d')} at "
            f"{start_time.strftime('%H:%M')} WIB"
        ),
        NotificationType.PARTNER_UNAVAILABLE: (
            f"Unfortunately, {booking.partner.full_name} is no longer available for your "
            f"appointment on {start_time.strftime('%Y-%m-%d %H:%M')} WIB"
        )
    }
    return messages.get(type, "Notification about your booking")

def create_notification(
    db: Session,
    customer_id: int,
    type: NotificationType,
    booking_id: int,
    scheduled_for: datetime
) -> Notification:
    """
    Create a new notification in the database.
    
    Args:
        db: Database session
        customer_id: ID of the customer to notify
        type: Type of notification from NotificationType enum
        booking_id: ID of the related booking
        scheduled_for: When the notification should be sent
        
    Returns:
        Notification: The created notification object
    """
    try:
        # Get the booking to generate the message
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking:
            raise ValueError(f"Booking with id {booking_id} not found")
            
        # Generate message based on notification type and booking details
        message = generate_notification_message(type, booking)
        
        # Create notification object
        notification = Notification(
            customer_id=customer_id,
            booking_id=booking_id,
            type=type,
            message=message,
            scheduled_for=scheduled_for,
            is_read=False
        )
        
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        return notification
        
    except Exception as e:
        db.rollback()
        raise Exception(f"Failed to create notification: {str(e)}")

def schedule_booking_notifications(
    db: Session,
    booking: Booking
) -> None:
    """Schedule all necessary notifications for a booking"""
    # Reminder 30 minutes before
    reminder_time = booking.start_datetime - timedelta(minutes=30)
    create_notification(
        db,
        customer_id=booking.customer_id,
        type=NotificationType.BOOKING_REMINDER,
        booking_id=booking.id,
        scheduled_for=reminder_time
    )
    
    # Booking confirmation
    create_notification(
        db,
        customer_id=booking.customer_id,
        type=NotificationType.BOOKING_CONFIRMATION,
        booking_id=booking.id,
        scheduled_for=datetime.now()
    )