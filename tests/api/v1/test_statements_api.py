from fastapi.testclient import TestClient


def create_school(client: TestClient, name: str = "Statement School") -> int:
    response = client.post("/api/v1/schools", json={"name": name})
    assert response.status_code == 201
    return response.json()["id"]


def create_student(client: TestClient, school_id: int) -> int:
    response = client.post(
        "/api/v1/students",
        json={
            "school_id": school_id,
            "first_name": "Lia",
            "last_name": "Ortega",
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
            "amount": "1000.00",
            "currency": "MXN",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def create_payment(client: TestClient, invoice_id: int) -> None:
    response = client.post(
        "/api/v1/payments",
        json={
            "invoice_id": invoice_id,
            "paid_at": "2026-01-05T10:00:00",
            "amount": "400.00",
            "method": "transfer",
        },
    )
    assert response.status_code == 201


def test_school_statement(client: TestClient) -> None:
    school_id = create_school(client)
    student_id = create_student(client, school_id)
    invoice_id = create_invoice(client, school_id, student_id)
    create_payment(client, invoice_id)

    school_statement = client.get(f"/api/v1/schools/{school_id}/statement")
    assert school_statement.status_code == 200
    assert school_statement.json()["total_invoiced"] == "1000.00"
    assert school_statement.json()["total_paid"] == "400.00"


def test_student_statement(client: TestClient) -> None:
    school_id = create_school(client)
    student_id = create_student(client, school_id)
    invoice_id = create_invoice(client, school_id, student_id)
    create_payment(client, invoice_id)

    student_statement = client.get(f"/api/v1/students/{student_id}/statement")
    assert student_statement.status_code == 200
    assert student_statement.json()["total_invoiced"] == "1000.00"
    assert student_statement.json()["total_paid"] == "400.00"
