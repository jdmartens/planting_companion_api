from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlmodel import Session, select
from datetime import datetime, timezone
import logging

from app.core.db import engine
from app.models import Reminder
from app.core.config import settings

logging.basicConfig(level=settings.LOGGING_LEVEL)
logger = logging.getLogger(__name__)

def check_due_reminders():
    """
    Task to check for reminders that are due and log them.
    """
    with Session(engine) as session:
        now = datetime.now(timezone.utc)
        due_reminders = session.exec(
            select(Reminder).where(Reminder.remind_time <= now)
        ).all()

        if not due_reminders:
            logger.info("No reminders due.")
            return
        for reminder in due_reminders:
           logger.info(
                f"Reminder due: {reminder.reminder_type} for plant {reminder.plant_id} at {reminder.remind_time}"
            )


def start_scheduler():
    """
    Start the APScheduler to run periodic tasks.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        check_due_reminders,
        trigger=IntervalTrigger(minutes=1), 
        id="check_due_reminders",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started!")