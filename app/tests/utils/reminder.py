from datetime import datetime, timedelta, timezone
from sqlmodel import Session
from app.models import Reminder, ReminderCreate
from app.tests.utils.plant import create_random_plant
import random
import string


def random_string(length: int = 10) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def create_random_reminder(db: Session) -> Reminder:
    plant = create_random_plant(db)
    reminder_in = ReminderCreate(
        plant_id=plant.id,
        reminder_type="water",
        remind_time=datetime.now(timezone.utc) + timedelta(days=7),
        notes=random_string(),
    )
    reminder = Reminder.from_orm(reminder_in)
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder