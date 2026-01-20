from fastapi.testclient import TestClient


def create_school(client: TestClient, name: str = "Alpha School") -> dict:
    response = client.post("/api/v1/schools", json={"name": name})
    assert response.status_code == 201
    return response.json()


def test_create_school(client: TestClient) -> None:
    school = create_school(client)
    assert school["name"] == "Alpha School"


def test_list_schools(client: TestClient) -> None:
    create_school(client)
    response = client.get("/api/v1/schools")
    assert response.status_code == 200
    assert response.json()["total"] >= 1


def test_get_school(client: TestClient) -> None:
    school = create_school(client)
    response = client.get(f"/api/v1/schools/{school['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == school["name"]


def test_update_school(client: TestClient) -> None:
    school = create_school(client)
    response = client.put(
        f"/api/v1/schools/{school['id']}", json={"address": "Main St"}
    )
    assert response.status_code == 200
    assert response.json()["address"] == "Main St"


def test_delete_school(client: TestClient) -> None:
    school = create_school(client)
    delete_resp = client.delete(f"/api/v1/schools/{school['id']}")
    assert delete_resp.status_code == 204

    missing_resp = client.get(f"/api/v1/schools/{school['id']}")
    assert missing_resp.status_code == 404
