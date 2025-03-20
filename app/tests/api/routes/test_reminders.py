import uuid
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.plant import create_random_plant
from app.tests.utils.reminder import create_random_reminder


def test_create_reminder(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    plant = create_random_plant(db)
    data = {
        "plant_id": str(plant.id),
        "reminder_type": "water",
        "remind_time": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
        "notes": "Water the plant",
    }
    response = client.post(
        f"{settings.API_V1_STR}/reminders/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["reminder_type"] == data["reminder_type"]
    assert content["plant_id"] == data["plant_id"]
    assert "id" in content


def test_read_reminder(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    reminder = create_random_reminder(db)
    response = client.get(
        f"{settings.API_V1_STR}/reminders/{reminder.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["reminder_type"] == reminder.reminder_type
    assert content["plant_id"] == str(reminder.plant_id)
    assert content["id"] == str(reminder.id)


def test_read_reminder_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/reminders/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Reminder not found"


def test_update_reminder(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    reminder = create_random_reminder(db)
    data = {"reminder_type": "fertilization", "notes": "Fertilize the plant"}
    response = client.put(
        f"{settings.API_V1_STR}/reminders/{reminder.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["reminder_type"] == data["reminder_type"]
    assert content["notes"] == data["notes"]
    assert content["id"] == str(reminder.id)


def test_update_reminder_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"reminder_type": "fertilization", "notes": "Fertilize the plant"}
    response = client.put(
        f"{settings.API_V1_STR}/reminders/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Reminder not found"


def test_delete_reminder(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    reminder = create_random_reminder(db)
    response = client.delete(
        f"{settings.API_V1_STR}/reminders/{reminder.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Reminder deleted successfully"


def test_delete_reminder_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/reminders/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Reminder not found"