# Project: luchoh.com refactoring
# File: backend/app/schemas/token.py
from typing import Optional, Union
from pydantic import BaseModel
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Union[int, str]
    exp: datetime


class TokenData(BaseModel):
    email: Optional[str] = None
