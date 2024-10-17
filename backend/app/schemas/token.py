# Project: luchoh.com refactoring
# File: backend/app/schemas/token.py

"""Pydantic models for token-related schemas."""

from typing import Optional, Union
from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    """Schema for access token response."""
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """Schema for token payload."""
    sub: Union[int, str]
    exp: datetime


class TokenData(BaseModel):
    """Schema for token data."""
    email: Optional[str] = None
