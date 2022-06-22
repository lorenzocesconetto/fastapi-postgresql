from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.main import app
from tests.utils.user import get_auth_header_from_email, get_superuser_auth_header


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator:
    db = SessionLocal()
    init_db(db)
    yield db
    db.close()


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_auth_header(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    return get_auth_header_from_email(client=client, db=db, email=settings.EMAIL_TEST_USER)
