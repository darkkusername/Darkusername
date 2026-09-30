from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import os

def schedule_content(payload: dict[str, Any]) -> dict[str, Any]:
    """Create a safe publishing job record. No provider call is implied."""
    platform = str(payload.get("platform", "")).strip().lower()
    content = str(payload.get("content", "")).strip()
    scheduled_at = str(payload.get("scheduled_at", "")).strip()
    allowed = {"youtube", "instagram", "tiktok"}
    if platform not in allowed:
        return {"status": "invalid", "error": "platform must be youtube, instagram, or tiktok"}
    if not content:
        return {"status": "invalid", "error": "content is required"}
    if scheduled_at:
        try:
            datetime.fromisoformat(scheduled_at.replace("Z", "+00:00"))
        except ValueError:
            return {"status": "invalid", "error": "scheduled_at must be ISO-8601"}
    job = {
        "platform": platform,
        "content": content,
        "scheduled_at": scheduled_at or None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "mode": "dry_run",
        "provider_configured": bool(os.getenv("METRICOOL_API_TOKEN", "").strip()),
        "status": "preview_only",
        "message": "Saved as a preview only. No post was published or scheduled externally."
    }
    return job
