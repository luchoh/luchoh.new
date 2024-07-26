# Project: luchoh.com refactoring
# File: backend/app/utils/file.py
import os
import uuid
from app.core.config import settings


def generate_file_path(original_filename, prefix=None, suffix=None):
    """
    Generate a unique file path for uploads.

    :param original_filename: The original filename of the uploaded file
    :param prefix: Optional prefix for the filename (e.g., 'thumbnail_')
    :param suffix: Optional suffix for the filename (before the extension)
    :return: A tuple of (relative_path, full_path)
    """
    file_extension = os.path.splitext(original_filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    if prefix:
        unique_filename = f"{prefix}{unique_filename}"
    if suffix:
        name, ext = os.path.splitext(unique_filename)
        unique_filename = f"{name}{suffix}{ext}"

    relative_path = os.path.join("uploads", unique_filename)
    full_path = os.path.join(settings.UPLOAD_DIRECTORY, unique_filename)

    return relative_path, full_path
