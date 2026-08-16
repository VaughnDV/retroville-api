"""Wait until PostgreSQL accepts connections. Used by Compose, not the production image."""

from __future__ import annotations

import logging
import os
import time

import psycopg

check_timeout = float(os.getenv("POSTGRES_CHECK_TIMEOUT", "30"))
check_interval = float(os.getenv("POSTGRES_CHECK_INTERVAL", "1"))
database_url = os.getenv("DATABASE_URL", "postgres://postgres:@postgres:5432/postgres")

logger = logging.getLogger("wait_for_postgres")
logging.basicConfig(level=logging.INFO)


def ready() -> bool:
    deadline = time.time() + check_timeout
    while time.time() < deadline:
        try:
            with psycopg.connect(database_url, connect_timeout=3) as conn:
                conn.execute("SELECT 1")
            logger.info("Postgres is ready")
            return True
        except Exception as exc:
            logger.info("Postgres is not ready (%s); retrying", exc)
            time.sleep(check_interval)
    logger.error("Could not connect to Postgres within %s seconds", check_timeout)
    return False


if __name__ == "__main__":
    raise SystemExit(0 if ready() else 1)
