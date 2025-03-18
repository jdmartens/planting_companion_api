from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.models import User, UserCreate, Plant, PlantCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)

    # Initial plant data
    initial_plants = [
        {
            "name": "Tomato",
            "cultivar": "Cherry",
            "quantity": 10,
            "date": "2025-03-13",
            "location": "Garden",
            "days_to_germ": 7,
            "days_to_maturity": 60,
            "notes": "Needs full sun",
            "planting_depth": "1 inch",
            "spacing": "2 feet"
        },
        {
            "name": "Carrot",
            "cultivar": "Nantes",
            "quantity": 20,
            "date": "2025-03-15",
            "location": "Garden",
            "days_to_germ": 10,
            "days_to_maturity": 70,
            "notes": "Needs loose soil",
            "planting_depth": "1/2 inch",
            "spacing": "3 inches"
        }
    ]

    for plant_data in initial_plants:
        plant = session.exec(
            select(Plant).where(Plant.name == plant_data["name"])
        ).first()
        if not plant:
            plant_in = PlantCreate(**plant_data)
            crud.create_plant(session=session, plant_in=plant_in, owner_id=user.id)