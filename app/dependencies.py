# app/dependencies.py
from fastapi import Header, HTTPException, status
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY", "tarh-dev-key-123")


def get_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> str:
    """
    Simple API key check using the X-API-Key header.
    """
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return x_api_key
