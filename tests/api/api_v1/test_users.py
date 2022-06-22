from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from tests.utils import random_email, random_lower_string


def test_get_users_superuser_me(client: TestClient, superuser_token_headers: dict[str, str]):
    response = client.get(
        f"{settings.API_STR}{settings.API_V1_STR}/users/me", headers=superuser_token_headers
    )
    assert response.status_code == 200
    current_user = response.json()
    assert current_user
    assert current_user["is_active"]
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


def test_get_users_normal_user_me(client: TestClient, normal_user_token_headers: dict[str, str]):
    response = client.get(
        f"{settings.API_STR}{settings.API_V1_STR}/users/me", headers=normal_user_token_headers
    )
    assert response.status_code == 200
    current_user = response.json()
    assert current_user
    assert current_user["is_active"]
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER


def test_superuser_create_user_new_email(
    client: TestClient, superuser_token_headers: dict, db: Session
):
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password, "is_superuser": True, "is_active": False}
    response = client.post(
        f"{settings.API_STR}{settings.API_V1_STR}/users",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= response.status_code < 300

    user = crud.user.get_by_email(db, email=email)
    assert user
    assert user.email == email
    assert user.is_superuser
    assert user.is_active is False


def test_create_user_new_email(client: TestClient, db: Session):
    email = random_email()
    password = random_lower_string()
    data = {"email": email, "password": password, "is_superuser": True, "is_active": False}
    response = client.post(
        f"{settings.API_STR}{settings.API_V1_STR}/users/open",
        json=data,
    )
    assert 200 <= response.status_code < 300

    user = crud.user.get_by_email(db, email=email)
    assert user
    assert user.email == email
    assert user.is_superuser is False
    assert user.is_active


def test_get_existing_user(client: TestClient, superuser_token_headers: dict, db: Session):
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    user_id = user.id
    response = client.get(
        f"{settings.API_STR}{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert 200 <= response.status_code < 300
    api_user = response.json()
    existing_user = crud.user.get_by_email(db, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_create_user_existing_username(
    client: TestClient, superuser_token_headers: dict, db: Session
):
    username = random_email()  # username = email
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud.user.create(db, obj_in=user_in)
    data = {"email": username, "password": password}
    response = client.post(
        f"{settings.API_STR}{settings.API_V1_STR}/users",
        headers=superuser_token_headers,
        json=data,
    )
    created_user = response.json()
    assert response.status_code == 400
    assert "_id" not in created_user


def test_retrieve_users(client: TestClient, superuser_token_headers: dict, db: Session):
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    crud.user.create(db, obj_in=user_in)

    username2 = random_email()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, password=password2)
    crud.user.create(db, obj_in=user_in2)

    response = client.get(
        f"{settings.API_STR}{settings.API_V1_STR}/users", headers=superuser_token_headers
    )
    all_users = response.json()

    assert len(all_users) > 1
    for item in all_users:
        assert "email" in item
