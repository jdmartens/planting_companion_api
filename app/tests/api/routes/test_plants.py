import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.plant import create_random_plant


def test_create_plant(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {
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
    }
    response = client.post(
        f"{settings.API_V1_STR}/plants/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["cultivar"] == data["cultivar"]
    assert "id" in content
    assert "owner_id" in content


def test_read_plant(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    plant = create_random_plant(db)
    response = client.get(
        f"{settings.API_V1_STR}/plants/{plant.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == plant.name
    assert content["cultivar"] == plant.cultivar
    assert content["id"] == str(plant.id)
    assert content["owner_id"] == str(plant.owner_id)


def test_read_plant_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/plants/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Plant not found"


def test_read_plant_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    plant = create_random_plant(db)
    response = client.get(
        f"{settings.API_V1_STR}/plants/{plant.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_plants(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_plant(db)
    create_random_plant(db)
    response = client.get(
        f"{settings.API_V1_STR}/plants/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_plant(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    plant = create_random_plant(db)
    data = {"name": "Updated Tomato", "cultivar": "Updated Cherry"}
    response = client.put(
        f"{settings.API_V1_STR}/plants/{plant.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["cultivar"] == data["cultivar"]
    assert content["id"] == str(plant.id)
    assert content["owner_id"] == str(plant.owner_id)


def test_update_plant_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"name": "Updated Tomato", "cultivar": "Updated Cherry"}
    response = client.put(
        f"{settings.API_V1_STR}/plants/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Plant not found"


def test_update_plant_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    plant = create_random_plant(db)
    data = {"name": "Updated Tomato", "cultivar": "Updated Cherry"}
    response = client.put(
        f"{settings.API_V1_STR}/plants/{plant.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_delete_plant(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    plant = create_random_plant(db)
    response = client.delete(
        f"{settings.API_V1_STR}/plants/{plant.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Plant deleted successfully"


def test_delete_plant_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/plants/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Plant not found"


def test_delete_plant_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    plant = create_random_plant(db)
    response = client.delete(
        f"{settings.API_V1_STR}/plants/{plant.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"