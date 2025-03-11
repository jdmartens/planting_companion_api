import uuid
from typing import Any, List

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import Plant, PlantCreate, PlantPublic, PlantsPublic, PlantUpdate, Message

router = APIRouter(prefix="/plants", tags=["plants"])


@router.get("/", response_model=PlantsPublic)
def read_plants(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve plants.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Plant)
        count = session.exec(count_statement).one()
        statement = select(Plant).offset(skip).limit(limit)
        plants = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Plant)
            .where(Plant.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Plant)
            .where(Plant.owner_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        plants = session.exec(statement).all()

    return PlantsPublic(data=plants, count=count)


@router.get("/{id}", response_model=PlantPublic)
def read_plant(session: SessionDep, current_user: CurrentUser, id: uuid.UUID) -> Any:
    """
    Get plant by ID.
    """
    plant = session.get(Plant, id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    if not current_user.is_superuser and (plant.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return plant


@router.post("/", response_model=PlantPublic)
def create_plant(
    *, session: SessionDep, current_user: CurrentUser, plant_in: PlantCreate
) -> Any:
    """
    Create new plant.
    """
    plant = Plant.model_validate(plant_in, update={"owner_id": current_user.id})
    session.add(plant)
    session.commit()
    session.refresh(plant)
    return plant


@router.put("/{id}", response_model=PlantPublic)
def update_plant(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    plant_in: PlantUpdate,
) -> Any:
    """
    Update a plant.
    """
    plant = session.get(Plant, id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    if not current_user.is_superuser and (plant.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    update_dict = plant_in.model_dump(exclude_unset=True)
    plant.sqlmodel_update(update_dict)
    session.add(plant)
    session.commit()
    session.refresh(plant)
    return plant


@router.delete("/{id}")
def delete_plant(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete a plant.
    """
    plant = session.get(Plant, id)
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")
    if not current_user.is_superuser and (plant.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(plant)
    session.commit()
    return Message(message="Plant deleted successfully")