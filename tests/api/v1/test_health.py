from fastapi.testclient import TestClient

from app.main import app


def test_health() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["database"] in {"ok", "error"}
    assert payload["redis"] in {"ok", "error"}
    assert isinstance(payload["requests_total"], int)
