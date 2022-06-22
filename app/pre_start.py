import logging

from app.db.init_db import init_db
from app.db.session import SessionLocal
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

wait_seconds = 1  # one second between retries
max_tries = 60 * 2  # 120 retries -> two minutes


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        db = SessionLocal()
        # Try to create session to check if DB is awake
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e
    init_db(db)


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")
