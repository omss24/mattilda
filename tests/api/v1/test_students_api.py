from fastapi.testclient import TestClient


def create_school(client: TestClient, name: str = "Beta School") -> int:
    response = client.post("/api/v1/schools", json={"name": name})
    assert response.status_code == 201
    return response.json()["id"]


def create_student(client: TestClient, school_id: int) -> dict:
    response = client.post(
        "/api/v1/students",
        json={
            "school_id": school_id,
            "first_name": "Ana",
            "last_name": "Lopez",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_create_student(client: TestClient) -> None:
    school_id = create_school(client)
    student = create_student(client, school_id)
    assert student["school_id"] == school_id


def test_list_students(client: TestClient) -> None:
    school_id = create_school(client)
    create_student(client, school_id)
    response = client.get(f"/api/v1/students?school_id={school_id}")
    assert response.status_code == 200
    assert response.json()["total"] >= 1


def test_get_student(client: TestClient) -> None:
    school_id = create_school(client)
    student = create_student(client, school_id)
    response = client.get(f"/api/v1/students/{student['id']}")
    assert response.status_code == 200


def test_update_student(client: TestClient) -> None:
    school_id = create_school(client)
    student = create_student(client, school_id)
    response = client.put(
        f"/api/v1/students/{student['id']}", json={"last_name": "Garcia"}
    )
    assert response.status_code == 200
    assert response.json()["last_name"] == "Garcia"


def test_delete_student(client: TestClient) -> None:
    school_id = create_school(client)
    student = create_student(client, school_id)
    delete_resp = client.delete(f"/api/v1/students/{student['id']}")
    assert delete_resp.status_code == 204

    missing_resp = client.get(f"/api/v1/students/{student['id']}")
    assert missing_resp.status_code == 404
