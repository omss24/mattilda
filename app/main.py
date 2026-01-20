"""FastAPI application entry point.

This module configures the FastAPI app, registers routes,
middleware, and exception handlers for domain exceptions.
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.health import router as health_router
from app.api.v1.invoices import router as invoices_router
from app.api.v1.payments import router as payments_router
from app.api.v1.schools import router as schools_router
from app.api.v1.students import router as students_router
from app.core.exceptions import (
    BusinessRuleError,
    DomainException,
    EntityNotFoundError,
    ValidationError,
)
from app.core.logging import LoggingMiddleware
from app.core.metrics import get_requests_total

app = FastAPI(title="Mattilda Backend Challenge API")

app.add_middleware(LoggingMiddleware)


# --- Exception Handlers ---
# Convert domain exceptions to structured JSON responses


@app.exception_handler(EntityNotFoundError)
async def entity_not_found_handler(request: Request, exc: EntityNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"error": {"code": "NOT_FOUND", "message": str(exc)}},
    )


@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"error": {"code": "VALIDATION_ERROR", "message": str(exc)}},
    )


@app.exception_handler(BusinessRuleError)
async def business_rule_error_handler(request: Request, exc: BusinessRuleError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"error": {"code": "BUSINESS_RULE_VIOLATION", "message": str(exc)}},
    )


@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"error": {"code": "DOMAIN_ERROR", "message": str(exc)}},
    )


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
