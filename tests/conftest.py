from datetime import date, datetime
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.core.db import Base, get_db
from app.core.config import settings
from app.main import app
from app.models.invoice import Invoice
from app.models.payment import Payment
from app.models.school import School
from app.models.student import Student


def create_test_session() -> Session:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(engine)
    return Session(engine)


@pytest.fixture()
def db_session() -> Session:
    session = create_test_session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session: Session) -> TestClient:
    def override_get_db() -> Session:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        test_client.headers.update({"X-API-Key": settings.api_key})
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def school(db_session: Session) -> School:
    school = School(name="Mattilda Academy")
    db_session.add(school)
    db_session.flush()
    return school


@pytest.fixture()
def student(db_session: Session, school: School) -> Student:
    student = Student(
        school_id=school.id,
        first_name="Ana",
        last_name="Lopez",
    )
    db_session.add(student)
    db_session.flush()
    return student


@pytest.fixture()
def invoice(db_session: Session, school: School, student: Student) -> Invoice:
    invoice = Invoice(
        school_id=school.id,
        student_id=student.id,
        issue_date=date(2026, 1, 1),
        due_date=date(2026, 1, 10),
        amount=Decimal("1000.00"),
        currency="MXN",
    )
    db_session.add(invoice)
    db_session.flush()
    return invoice


@pytest.fixture()
def payments(db_session: Session, invoice: Invoice) -> list[Payment]:
    payment_1 = Payment(
        invoice_id=invoice.id,
        paid_at=datetime(2026, 1, 5, 10, 0, 0),
        amount=Decimal("200.00"),
        method="transfer",
    )
    payment_2 = Payment(
        invoice_id=invoice.id,
        paid_at=datetime(2026, 1, 6, 12, 0, 0),
        amount=Decimal("300.00"),
        method="card",
    )
    db_session.add_all([payment_1, payment_2])
    db_session.commit()
    return [payment_1, payment_2]
