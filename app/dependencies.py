# app/dependencies.py

from fastapi import Header, HTTPException, status


# ⚠️ For now this is hardcoded. Later we can move it to env/.env.
API_KEY = "tarh-dev-key-123"


def get_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> str:
    """
    Simple API key check using the X-API-Key header.

    - If header missing or incorrect → 401 Unauthorized
    - If correct → returns the API key (not actually used, just for validation)
    """
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return x_api_key
