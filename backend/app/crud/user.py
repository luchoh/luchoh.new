# Project: luchoh.com refactoring
# File: backend/app/crud/user.py
from sqlalchemy.orm import Session

from app.auth.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate


class CRUDUser:
    def get(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, user_in: UserCreate):
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
        db_user = self.get_by_username(db, username=username_or_email)
        if not db_user:
            db_user = self.get_by_email(db, email=username_or_email)
        if not db_user:
            return None
        if not verify_password(password, db_user.hashed_password):
            return None
        return db_user

    def is_active(self, user_obj: User) -> bool:
        return user_obj.is_active

    def is_superuser(self, user_obj: User) -> bool:
        return user_obj.is_superuser


user = CRUDUser()
