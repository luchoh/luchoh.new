# Project: luchoh.com refactoring
# File: backend/app/api/endpoints/upload.py

"""Endpoints for handling file uploads in the LuchoH Photography API."""

import os
import shutil

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException

from app.api import deps
from app.models.user import User
from app import crud
from app.core.config import settings
from app.utils.file import generate_file_path

router = APIRouter()

# Use an absolute path for UPLOAD_DIRECTORY
UPLOAD_DIRECTORY = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "uploads")
)
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}


def is_file_extension_allowed(filename):
    """Check if the file extension is allowed."""
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS


@router.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Upload a file to the server.

    This endpoint allows authenticated users to upload files to the server.
    It checks for proper permissions and file type before saving the file.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    if not is_file_extension_allowed(file.filename):
        raise HTTPException(status_code=400, detail="File extension not allowed")

    # Ensure the upload directory exists
    os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)

    relative_file_path, file_location = generate_file_path(file.filename)

    try:
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not upload file: {str(e)}") from e

    file_size = os.path.getsize(file_location)

    return {
        "message": "File uploaded successfully",
        "original_filename": file.filename,
        "saved_filename": os.path.basename(file_location),
        "file_path": relative_file_path,
        "file_size": file_size,
    }
