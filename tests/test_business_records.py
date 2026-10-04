from src.publishing import schedule_content
from src.db import recent_business_records

def test_publishing_preview_is_persisted(tmp_path, monkeypatch):
    import src.db as db
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    result = schedule_content({
        "platform": "youtube",
        "content": "AI agents explained",
        "mode": "preview",
    })
    assert result["status"] == "preview_only"
    assert result["record_id"] >= 1
    rows = recent_business_records("publishing_jobs", 10)
    assert rows[0]["payload"]["platform"] == "youtube"

def test_publishing_execute_never_fakes_external_action(tmp_path, monkeypatch):
    import src.db as db
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    result = schedule_content({
        "platform": "tiktok",
        "content": "AI automation workflow",
        "mode": "execute",
    })
    assert result["status"] == "provider_not_implemented"
    assert "No external publication was performed" in result["message"]
