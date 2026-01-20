from fastapi.testclient import TestClient


def create_school(client: TestClient, name: str = "Delta School") -> int:
    response = client.post("/api/v1/schools", json={"name": name})
    assert response.status_code == 201
    return response.json()["id"]


def create_student(client: TestClient, school_id: int) -> int:
    response = client.post(
        "/api/v1/students",
        json={
            "school_id": school_id,
            "first_name": "Mia",
            "last_name": "Torres",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def create_invoice(client: TestClient, school_id: int, student_id: int) -> int:
    response = client.post(
        "/api/v1/invoices",
        json={
            "school_id": school_id,
            "student_id": student_id,
            "issue_date": "2026-01-01",
            "due_date": "2026-01-10",
            "amount": "500.00",
            "currency": "MXN",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def create_payment(client: TestClient, invoice_id: int) -> dict:
    response = client.post(
        "/api/v1/payments",
        json={
            "invoice_id": invoice_id,
            "paid_at": "2026-01-05T10:00:00",
            "amount": "200.00",
            "method": "transfer",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_create_payment(client: TestClient) -> None:
    school_id = create_school(client)
    student_id = create_student(client, school_id)
    invoice_id = create_invoice(client, school_id, student_id)
    payment = create_payment(client, invoice_id)
    assert payment["invoice_id"] == invoice_id


def test_list_payments(client: TestClient) -> None:
    school_id = create_school(client)
    student_id = create_student(client, school_id)
    invoice_id = create_invoice(client, school_id, student_id)
    create_payment(client, invoice_id)
    response = client.get(f"/api/v1/payments?invoice_id={invoice_id}")
    assert response.status_code == 200
    assert response.json()["total"] >= 1


def test_get_payment(client: TestClient) -> None:
    school_id = create_school(client)
    student_id = create_student(client, school_id)
    invoice_id = create_invoice(client, school_id, student_id)
    payment = create_payment(client, invoice_id)
    response = client.get(f"/api/v1/payments/{payment['id']}")
    assert response.status_code == 200
