# Project: luchoh.com refactoring
# File: backend/app/crud/user.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.security import get_password_hash, verify_password

class CRUDUser:
    def get(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, user: UserCreate):
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=get_password_hash(user.password),
            is_active=user.is_active,
            is_superuser=user.is_superuser,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def authenticate(self, db: Session, username_or_email: str, password: str):
        user = self.get_by_username(db, username=username_or_email)
        if not user:
            user = self.get_by_email(db, email=username_or_email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

user = CRUDUser()