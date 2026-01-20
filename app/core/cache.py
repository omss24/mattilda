"""Redis-based caching for expensive operations.

Used primarily for caching account statements which require
aggregation across multiple tables. Cache is invalidated
when invoices or payments are created/updated.
"""
import json
from typing import Any

import redis
from fastapi import Request

from app.core.config import settings


_redis_client: redis.Redis | None = None


def get_redis_client() -> redis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
    return _redis_client


def build_cache_key(request: Request) -> str:
    method = request.method.upper()
    path = request.url.path
    params = sorted(request.query_params.items())
    if params:
        query_string = "&".join(f"{key}={value}" for key, value in params)
    else:
        query_string = ""
    return f"cache:{method}:{path}:{query_string}"


def cache_get(key: str) -> dict | None:
    try:
        value = get_redis_client().get(key)
        if not value:
            return None
        return json.loads(value)
    except Exception:
        return None


def cache_set(key: str, value: dict, ttl: int = 60) -> None:
    try:
        payload = json.dumps(value, default=str)
        get_redis_client().setex(key, ttl, payload)
    except Exception:
        return None


def cache_invalidate_prefix(prefix: str) -> None:
    try:
        client = get_redis_client()
        for key in client.scan_iter(match=f"{prefix}*"):
            client.delete(key)
    except Exception:
        return None
