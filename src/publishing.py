from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import os
from .db import save_business_record

ALLOWED_PLATFORMS={"youtube","instagram","tiktok"}

def _parse_iso(value:str)->bool:
    try:
        datetime.fromisoformat(value.replace("Z","+00:00"))
        return True
    except ValueError:
        return False

def schedule_content(payload:dict[str,Any])->dict[str,Any]:
    """Persist a publishing job and never imply an external post occurred without provider confirmation."""
    platform=str(payload.get("platform","")).strip().lower()
    content=str(payload.get("content","")).strip()
    scheduled_at=str(payload.get("scheduled_at","")).strip()
    requested_mode=str(payload.get("mode","preview")).strip().lower()
    mode="dry_run" if requested_mode in {"preview","dry_run"} else requested_mode
    if platform not in ALLOWED_PLATFORMS:
        return {"status":"invalid","error":"platform must be youtube, instagram, or tiktok"}
    if not content:
        return {"status":"invalid","error":"content is required"}
    if scheduled_at and not _parse_iso(scheduled_at):
        return {"status":"invalid","error":"scheduled_at must be ISO-8601"}
    if mode not in {"dry_run","execute"}:
        return {"status":"invalid","error":"mode must be preview/dry_run or execute"}

    provider_configured=bool(os.getenv("METRICOOL_API_TOKEN","").strip())
    job={
        "platform":platform,
        "content":content,
        "scheduled_at":scheduled_at or None,
        "created_at":datetime.now(timezone.utc).isoformat(),
        "mode":mode,
        "provider_configured":provider_configured,
        "status":"preview_only" if mode=="dry_run" else "provider_not_implemented",
    }
    if mode=="execute":
        job["message"]="No external publication was performed: provider execution is not implemented yet."
    else:
        job["message"]="Publishing job persisted as preview. No post was published or scheduled externally."

    record=save_business_record("publishing_jobs",job)
    job["record_id"]=record["id"]
    return job
