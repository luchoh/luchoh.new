# Project: luchoh.com refactoring
# File: backend/app/schemas/msg.py

"""Pydantic model for message responses."""

from pydantic import BaseModel


class Msg(BaseModel):
    """
    Pydantic model for a simple message response.

    Attributes:
        msg (str): The message content.
    """
    msg: str
