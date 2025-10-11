from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "message" in resp.json()
