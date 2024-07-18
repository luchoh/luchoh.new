# Project: luchoh.com refactoring
# File: backend/app/schemas/token.py
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: EmailStr | None = None
