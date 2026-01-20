"""API authentication utilities.

Currently implements simple API key authentication.
For production, consider JWT/OAuth2 for user-level access control.
"""
import secrets

from fastapi import Header, HTTPException, status

from app.core.config import settings


def verify_api_key(api_key_header: str | None = Header(None, alias="X-API-Key")) -> None:
    """Validate the X-API-Key header against configured API key.
    
    Uses constant-time comparison to prevent timing attacks.
    """
    if not api_key_header or not secrets.compare_digest(api_key_header, settings.api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
