import logging
import time
from datetime import datetime, timezone

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.metrics import increment_requests

logger = logging.getLogger("app.request")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):  # type: ignore[override]
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        increment_requests()

        logger.info(
            "timestamp=%s method=%s path=%s status_code=%s response_time_ms=%.2f",
            datetime.now(timezone.utc).isoformat(),
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response
