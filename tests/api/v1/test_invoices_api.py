from fastapi.testclient import TestClient


def create_school(client: TestClient, name: str = "Gamma School") -> int:
    response = client.post("/api/v1/schools", json={"name": name})
    assert response.status_code == 201
    return response.json()["id"]


def create_student(client: TestClient, school_id: int) -> int:
    response = client.post(
        "/api/v1/students",
        json={
            "school_id": school_id,
            "first_name": "Luis",
            "last_name": "Perez",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def create_invoice(client: TestClient, school_id: int, student_id: int) -> dict:
    response = client.post(
        "/api/v1/invoices",
        json={
            "school_id": school_id,
            "student_id": student_id,
            "issue_date": "2026-01-01",
            "due_date": "2026-01-10",
            "amount": "1000.00",
            "currency": "MXN",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_create_invoice(client: TestClient) -> None:
    school_id = create_school(client)
    student_id = create_student(client, school_id)
    invoice = create_invoice(client, school_id, student_id)
    assert invoice["student_id"] == student_id


def test_list_invoices(client: TestClient) -> None:
    school_id = create_school(client)
    student_id = create_student(client, school_id)
    create_invoice(client, school_id, student_id)
    response = client.get(f"/api/v1/invoices?student_id={student_id}")
    assert response.status_code == 200
    assert response.json()["total"] >= 1


def test_get_invoice(client: TestClient) -> None:
    school_id = create_school(client)
    student_id = create_student(client, school_id)
    invoice = create_invoice(client, school_id, student_id)
    response = client.get(f"/api/v1/invoices/{invoice['id']}")
    assert response.status_code == 200


def test_update_invoice(client: TestClient) -> None:
    school_id = create_school(client)
    student_id = create_student(client, school_id)
    invoice = create_invoice(client, school_id, student_id)
    response = client.put(
        f"/api/v1/invoices/{invoice['id']}", json={"description": "Tuition"}
    )
    assert response.status_code == 200
    assert response.json()["description"] == "Tuition"


def test_cancel_invoice(client: TestClient) -> None:
    school_id = create_school(client)
    student_id = create_student(client, school_id)
    invoice = create_invoice(client, school_id, student_id)
    response = client.delete(f"/api/v1/invoices/{invoice['id']}")
    assert response.status_code == 200
    assert response.json()["status"] == "cancelled"
