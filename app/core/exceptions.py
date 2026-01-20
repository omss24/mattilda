"""Domain exceptions for business logic errors.

These exceptions are caught by FastAPI exception handlers in main.py
and converted to appropriate HTTP responses (400, 404, 422).
"""


class DomainException(Exception):
    """Base exception for all domain/business logic errors."""

    pass


class EntityNotFoundError(DomainException):
    """Raised when a required entity does not exist in the database."""

    def __init__(self, entity: str, entity_id: int | str | None = None):
        self.entity = entity
        self.entity_id = entity_id
        if entity_id:
            super().__init__(f"{entity} with id {entity_id} not found")
        else:
            super().__init__(f"{entity} not found")


class ValidationError(DomainException):
    """Raised when input data fails validation rules."""

    pass


class BusinessRuleError(DomainException):
    """Raised when an operation violates a business rule (e.g., overpayment)."""

    pass
