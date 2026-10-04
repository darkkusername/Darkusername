import os
import secrets
from fastapi import Header, HTTPException

def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    expected = os.getenv("API_KEY", "").strip()
    required = os.getenv("REQUIRE_API_KEY", "false").strip().lower() in {"1","true","yes","on"}
    if not required and not expected:
        return
    if not expected:
        raise HTTPException(status_code=503, detail="API_KEY is required but not configured")
    if not x_api_key or not secrets.compare_digest(x_api_key, expected):
        raise HTTPException(status_code=401, detail="Invalid API key")
