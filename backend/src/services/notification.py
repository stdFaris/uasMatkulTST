# src/services/notification.py
from datetime import datetime, timedelta
import resend
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from ..config.settings import Settings
from ..config.database import SQLALCHEMY_DATABASE_URL, SessionLocal
from ..models.customer import BookingStatus
from ..models.booking import Booking
from sqlalchemy.orm import Session

settings = Settings()
resend.api_key = settings.RESEND_API_KEY

class NotificationService:
    def __init__(self):
        self.scheduler = BackgroundScheduler(timezone=settings.SCHEDULER_TIMEZONE)
        self.scheduler.start()

    async def send_booking_confirmation(self, booking, db: Session):
        try:
            await resend.Emails.send({
                "from": settings.FROM_EMAIL,
                "to": booking.customer.email,
                "subject": "Booking Confirmed - SantaiRumah",
                "html": self._get_confirmation_email_template(booking)
            })
        except Exception as e:
            print(f"Error sending confirmation email: {e}")

    def schedule_reminder(self, booking_id: int, reminder_time: datetime):
        """Schedule a reminder notification."""
        self.scheduler.add_job(
            self.send_reminder,
            trigger=DateTrigger(run_date=reminder_time),
            args=[booking_id],
            id=f'reminder_{booking_id}'
        )

    def reschedule_reminder(self, booking_id: int, new_reminder_time: datetime):
        """Reschedule an existing reminder."""
        job_id = f'reminder_{booking_id}'
        self.scheduler.remove_job(job_id)
        self.schedule_reminder(booking_id, new_reminder_time)

    async def send_reminder(self, booking_id: int):
        """Send reminder notification."""
        db = SessionLocal()
        try:
            booking = db.query(Booking).filter(
                Booking.id == booking_id,
                Booking.status == BookingStatus.CONFIRMED
            ).first()
            
            if booking:
                await resend.Emails.send({
                    "from": settings.FROM_EMAIL,
                    "to": [booking.customer.email, booking.partner.email],
                    "subject": "Upcoming Service Reminder - SantaiRumah",
                    "html": self._get_reminder_email_template(booking)
                })
        finally:
            db.close()
    
    def _format_location(self, booking: Booking) -> str:
        """Format location details from service area."""
        service_area = booking.partner.service_areas[0] if booking.partner.service_areas else None
        if service_area:
            return f"{service_area.district.name}, {service_area.regency.name}"
        return "Location not specified"

    def _get_confirmation_email_template(self, booking):
        return f"""
        <h2>Your booking has been confirmed!</h2>
        <p>Booking details:</p>
        <ul>
            <li>Service Date: {booking.start_datetime.strftime('%Y-%m-%d')}</li>
            <li>Start Time: {booking.start_datetime.strftime('%H:%M')}</li>
            <li>Duration: {booking.duration_hours} hours</li>
            <li>Total Price: ${booking.total_price:.2f}</li>
        </ul>
        <p>Your service provider will arrive at the scheduled time.</p>
        """

    def _get_reminder_email_template(self, booking):
        return f"""
        <h2>Your service starts in 30 minutes!</h2>
        <p>Booking details:</p>
        <ul>
            <li>Start Time: {booking.start_datetime.strftime('%H:%M')}</li>
            <li>Duration: {booking.duration_hours} hours</li>
            <li>Customer: {booking.customer.full_name}</li>
            <li>Service Provider: {booking.partner.full_name}</li>
            <li>Location: {self._format_location(booking)}</li>
        </ul>
        """

notification_service = NotificationService()
