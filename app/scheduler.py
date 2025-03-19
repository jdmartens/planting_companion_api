from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlmodel import Session, select
from datetime import datetime, timezone

from app.core.db import engine
from app.models import Reminder
from app.core.config import settings

def check_due_reminders():
    """
    Task to check for reminders that are due and log them.
    """
    with Session(engine) as session:
        now = datetime.now(timezone.utc)
        due_reminders = session.exec(
            select(Reminder).where(Reminder.remind_time <= now)
        ).all()

        for reminder in due_reminders:
            # Log or handle the due reminders
            print(f"Reminder due: {reminder.reminder_type} for plant {reminder.plant_id} at {reminder.remind_time}")


def start_scheduler():
    """
    Start the APScheduler to run periodic tasks.
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        check_due_reminders,
        trigger=IntervalTrigger(hours=1),  # Run every hour
        id="check_due_reminders",
        replace_existing=True,
    )
    scheduler.start()
    print("Scheduler started!")