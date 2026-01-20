from fastapi import FastAPI

from app.api.v1.health import router as health_router
from app.api.v1.invoices import router as invoices_router
from app.api.v1.payments import router as payments_router
from app.api.v1.schools import router as schools_router
from app.api.v1.students import router as students_router
from app.core.logging import LoggingMiddleware
from app.core.metrics import get_requests_total

app = FastAPI(title="Mattilda Backend Challenge API")

app.add_middleware(LoggingMiddleware)


@app.get("/")
def root() -> dict:
    return {"message": "Mattilda backend challenge API"}


@app.get("/metrics")
def metrics() -> dict:
    return {"requests_total": get_requests_total()}


app.include_router(health_router)
app.include_router(schools_router, prefix="/api/v1")
app.include_router(students_router, prefix="/api/v1")
app.include_router(invoices_router, prefix="/api/v1")
app.include_router(payments_router, prefix="/api/v1")
