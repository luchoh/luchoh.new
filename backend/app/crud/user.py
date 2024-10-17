# Project: luchoh.com refactoring
# File: backend/app/crud/user.py

"""CRUD operations for User model."""

from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.security import get_password_hash, verify_password


class CRUDUser:
    """CRUD operations for User model."""

    def get(self, db: Session, user_id: int):
        """Retrieve a user by ID."""
        return db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, db: Session, username: str):
        """Retrieve a user by username."""
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str):
        """Retrieve a user by email."""
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, user_in: UserCreate):
        """Create a new user."""
        db_user = User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            is_active=user_in.is_active,
            is_superuser=user_in.is_superuser,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def authenticate(self, db: Session, username_or_email: str, password: str):
        """Authenticate a user by username/email and password."""
        db_user = self.get_by_username(db, username=username_or_email)
        if not db_user:
            db_user = self.get_by_email(db, email=username_or_email)
        if not db_user:
            return None
        if not verify_password(password, db_user.hashed_password):
            return None
        return db_user

    def is_active(self, db_user: User) -> bool:
        """Check if a user is active."""
        return db_user.is_active

    def is_superuser(self, db_user: User) -> bool:
        """Check if a user is a superuser."""
        return db_user.is_superuser


user = CRUDUser()
