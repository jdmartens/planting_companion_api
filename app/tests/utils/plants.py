from sqlmodel import Session
from app.models import Plant, PlantCreate
import random
import string
from datetime import date


def random_string(length: int = 10) -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def create_random_plant(db: Session) -> Plant:
    plant_in = PlantCreate(
        name=random_string(),
        cultivar=random_string(),
        quantity=random.randint(1, 100),
        date=date.today(),
        location=random_string(),
        days_to_germ=random.randint(1, 30),
        days_to_maturity=random.randint(30, 120),
        notes=random_string(),
        planting_depth=f"{random.randint(1, 3)} inch",
        spacing=f"{random.randint(1, 3)} feet",
    )
    plant = Plant.from_orm(plant_in)
    db.add(plant)
    db.commit()
    db.refresh(plant)
    return plant