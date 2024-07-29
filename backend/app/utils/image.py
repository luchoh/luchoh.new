# Project: luchoh.com refactoring
# File: backend/app/utils/image.py

from app.utils.slugify import generate_slug
from app import models, schemas

from fastapi import Request

def get_full_url(request: Request, path: str) -> str:
    base_url = f"{request.base_url}"
    return f"{base_url}{path}"

def generate_image_response(image: models.Image, request: Request) -> dict:
    image_dict = image.__dict__.copy()
    image_dict["file_path"] = get_full_url(request, image.file_path)
    if image.thumbnail_url:
        image_dict["thumbnail_url"] = get_full_url(request, image.thumbnail_url)
    image_dict["tags"] = [schemas.Tag.from_orm(tag) for tag in image.tags]
    image_dict["slug"] = generate_slug(image.title)
    return image_dict