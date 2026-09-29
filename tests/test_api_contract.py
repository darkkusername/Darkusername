from fastapi.testclient import TestClient
from src.main import app
client=TestClient(app)
def test_health():
    r=client.get("/health")
    assert r.status_code==200 and r.json()["status"]=="ok"
def test_status_is_international():
    body=client.get("/api/v1/agent/status").json()
    assert body["market"]=="international" and body["language"]=="en"
    assert body["algeria_as_trend_criterion"] is False
