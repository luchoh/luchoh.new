# Project: luchoh.com refactoring
# File: backend/app/schemas/token.py
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Union[int, str]
    exp: datetime


class TokenData(BaseModel):
    email: Optional[str] = None
