# Project: luchoh.com refactoring
# File: backend/app/utils/slugify.py
import re

from unidecode import unidecode


def generate_slug(title: str) -> str:
    """
    Generate a URL-friendly slug from a title.
    """
    # Convert to ASCII
    slug = unidecode(title)
    # Convert to lowercase
    slug = slug.lower()
    # Remove non-word characters (everything except numbers and letters)
    slug = re.sub(r"[^\w\s-]", "", slug)
    # Replace all spaces and repeated dashes with single dashes
    slug = re.sub(r"[-\s]+", "-", slug).strip("-")
    return slug
