# Project: luchoh.com refactoring
# File: backend/app/db/session.py

"""Database session management for the LuchoH Photography API."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """
    Dependency function to get a database session.

    Yields:
        Session: A SQLAlchemy database session.

    Note:
        This function should be used as a dependency in FastAPI route functions.
        It ensures that the database session is properly closed after each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
