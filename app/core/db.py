"""Database session and connection management."""
from sqlalchemy import create_engine
from typing import Generator

from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.core.config import settings

engine = create_engine(settings.database_url, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
	"""FastAPI dependency that provides a database session.
	
	Yields a session and ensures it's closed after the request.
	"""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
