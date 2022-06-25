from typing import Any

from fastapi import APIRouter, Depends
from pydantic import EmailStr

from app import schemas
from app.api import deps
from app.core.celery_app import celery_app
from app.mail import send_test_email

router = APIRouter(prefix="/utils", tags=["utils"])


@router.post(
    "/test-celery",
    response_model=schemas.Msg,
    status_code=201,
    dependencies=[Depends(deps.get_current_active_superuser)],
)
def test_celery(
    msg: schemas.Msg,
) -> Any:
    """Test Celery worker."""
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post(
    "/test-email",
    response_model=schemas.Msg,
    status_code=201,
    dependencies=[Depends(deps.get_current_active_superuser)],
)
def test_email(
    email_to: EmailStr,
) -> Any:
    """Test email sending."""
    send_test_email(email_to=email_to)
    return {"msg": "Test email was sent."}
