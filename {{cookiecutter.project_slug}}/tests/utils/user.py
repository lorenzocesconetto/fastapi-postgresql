from fastapi.testclient import TestClient
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.models.user import User
from app.schemas import UserCreate, UserUpdate
from tests.utils import random_email, random_lower_string


def _get_auth_header_from_credentials(
    client: TestClient,
    login_data: dict[str, str],
) -> dict[str, str]:
    response = client.post(settings.API_LOGIN_STR, data=login_data)
    tokens = response.json()
    access_token = tokens["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


def get_auth_header(*, client: TestClient, email: EmailStr, password: str) -> dict[str, str]:
    return _get_auth_header_from_credentials(client, {"username": email, "password": password})


def get_superuser_auth_header(client: TestClient) -> dict[str, str]:
    return get_auth_header(
        client=client, email=settings.FIRST_SUPERUSER, password=settings.FIRST_SUPERUSER_PASSWORD
    )


def create_random_user(db: Session) -> User:
    email = random_email()
    password = random_lower_string()
    user = crud.user.get_by_email(db, email=email)
    if not user:
        user_in_create = UserCreate(email=email, password=password)
        user = crud.user.create(db, obj_in=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        user = crud.user.update(db, db_obj=user, obj_in=user_in_update)
    return user


def get_auth_header_from_email(
    *, client: TestClient, db: Session, email: EmailStr
) -> dict[str, str]:
    """
    Return a valid token for the user with given email.

    If the user doesn't exist it is created first.
    """
    password = random_lower_string()
    user = crud.user.get_by_email(db, email=email)
    if not user:
        user_in_create = UserCreate(email=email, password=password)
        user = crud.user.create(db, obj_in=user_in_create)
    else:
        user_in_update = UserUpdate(password=password)
        user = crud.user.update(db, db_obj=user, obj_in=user_in_update)
    return get_auth_header(client=client, email=email, password=password)
