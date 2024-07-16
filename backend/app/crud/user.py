from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.security import get_password_hash


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


user = CRUDUser()
