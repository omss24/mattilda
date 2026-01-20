from sqlalchemy import text

from app.core.cache import get_redis_client
from app.core.db import SessionLocal
from app.core.metrics import get_requests_total


def get_health_status() -> dict:
    database_status = "ok"
    redis_status = "ok"

    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
    except Exception:
        database_status = "error"

    try:
        get_redis_client().ping()
    except Exception:
        redis_status = "error"

    return {
        "status": "ok",
        "database": database_status,
        "redis": redis_status,
        "requests_total": get_requests_total(),
    }
