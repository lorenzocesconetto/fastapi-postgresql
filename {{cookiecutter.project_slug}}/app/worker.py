from app.core.celery_app import celery_app
from app.pre_start import init

init()  # Wait for db + init db


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"
