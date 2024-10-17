# Project: luchoh.com refactoring
# File: backend/app/utils/auth.py

"""Authentication utility functions for the LuchoH Photography API."""

from datetime import datetime, timedelta
from typing import Optional

from jose import jwt

from app.core.config import settings


def generate_password_reset_token(email: str) -> str:
    """
    Generate a password reset token for the given email.

    Args:
        email (str): The email address of the user requesting a password reset.

    Returns:
        str: A JWT token for password reset.
    """
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    """
    Verify the password reset token.

    Args:
        token (str): The password reset token to verify.

    Returns:
        Optional[str]: The email address if the token is valid, None otherwise.
    """
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["sub"]
    except jwt.JWTError:
        return None


def send_reset_password_email(email: str, token: str) -> None:
    """
    Send a password reset email.

    Args:
        email (str): The email address of the user requesting a password reset.
        token (str): The password reset token.

    Note:
        This function is a placeholder. Implement your email sending logic here.
    """
    # Implement your email sending logic here
    # For now, we'll just print the token
    print(f"Password reset token for {email}: {token}")
