from sqlalchemy import func, select
from sqlalchemy.orm import Session


def paginate(query, db: Session, limit: int, offset: int) -> dict:
    total = db.scalar(select(func.count()).select_from(query.subquery())) or 0
    items = db.scalars(query.offset(offset).limit(limit)).all()
    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
    }
