# Project: luchoh.com refactoring
# File: backend/app/models/user.py

"""SQLAlchemy model for User."""

from sqlalchemy import Boolean, Column, Integer, String
from app.db.base_class import Base

# pylint: disable=too-few-public-methods

class User(Base):
    """
    SQLAlchemy model for the User table.

    Attributes:
        id (int): Primary key for the user.
        username (str): Unique username for the user.
        email (str): Unique email address for the user.
        hashed_password (str): Hashed password for the user.
        is_active (bool): Flag indicating if the user account is active.
        is_superuser (bool): Flag indicating if the user has superuser privileges.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
