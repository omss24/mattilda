"""Database query pagination utilities."""
from sqlalchemy import func, select
from sqlalchemy.orm import Session


def paginate(query, db: Session, limit: int, offset: int) -> dict:
    """Apply offset-based pagination to a SQLAlchemy query.
    
    Returns a dict with:
    - items: The paginated results
    - total: Total count of all matching records
    - limit/offset: The pagination parameters used
    
    Note: For large datasets, consider cursor-based pagination
    to avoid performance issues with high offset values.
    """
    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    items = db.scalars(query.offset(offset).limit(limit)).all()
    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
    }
