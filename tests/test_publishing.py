from src.publishing import schedule_content

def test_schedule_content_is_preview_only():
    result = schedule_content({"platform": "youtube", "content": "A useful AI tutorial"})
    assert result["status"] == "preview_only"
    assert result["mode"] == "dry_run"
    assert "No post was published" in result["message"]

def test_schedule_rejects_unknown_platform():
    result = schedule_content({"platform": "unknown", "content": "test"})
    assert result["status"] == "invalid"

def test_schedule_rejects_bad_date():
    result = schedule_content({"platform": "youtube", "content": "test", "scheduled_at": "tomorrow"})
    assert result["status"] == "invalid"
