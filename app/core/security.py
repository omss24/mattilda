from fastapi import Header, HTTPException, status

from app.core.config import settings


def verify_api_key(api_key_header: str | None = Header(None, alias="X-API-Key")) -> None:
    if not api_key_header or api_key_header != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
