# Project: luchoh.com refactoring
# File: backend/app/utils/image.py

"""Utility functions for image handling in the LuchoH Photography API."""

from fastapi import Request

from app.utils.slugify import generate_slug
from app import models, schemas


def get_full_url(request: Request, path: str) -> str:
    """
    Generate a full URL for a given path.

    Args:
        request (Request): The FastAPI request object.
        path (str): The relative path to convert to a full URL.

    Returns:
        str: The full URL.
    """
    base_url = f"{request.base_url}"
    return f"{base_url}{path}"


def generate_image_response(image: models.Image, request: Request) -> dict:
    """
    Generate a response dictionary for an image.

    Args:
        image (models.Image): The image model instance.
        request (Request): The FastAPI request object.

    Returns:
        dict: A dictionary containing the image data with full URLs.
    """
    image_dict = image.__dict__.copy()
    image_dict["file_path"] = get_full_url(request, image.file_path)
    if image.thumbnail_url:
        image_dict["thumbnail_url"] = get_full_url(request, image.thumbnail_url)
    image_dict["tags"] = [schemas.Tag.from_orm(tag) for tag in image.tags]
    image_dict["slug"] = generate_slug(image.title)
    return image_dict
