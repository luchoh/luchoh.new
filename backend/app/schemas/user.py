from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str | None = None


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
