import logging
import os

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.db.init_db import init_db
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

wait_seconds = 2  # two seconds between retries
max_tries = 30  # 30 retries -> one minute


def run_alembic_migrations():
    import alembic.config

    alembicArgs = [
        "--raiseerr",
        "upgrade",
        "head",
    ]
    alembic.config.main(argv=alembicArgs)


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    logger.info("Initializing service")
    try:
        db = SessionLocal()
        # Try to create session to check if DB is awake
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e
    if os.environ.get("RUN_MIGRATION") and os.environ["RUN_MIGRATION"].lower() == "false":
        logger.info("Skipping migrations")
    else:
        logger.info("Running migrations")
        run_alembic_migrations()
    logger.info("Initializing database entries")
    init_db(db)
    logger.info("Service finished initializing")
