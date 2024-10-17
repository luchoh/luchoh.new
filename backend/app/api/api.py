# Project: luchoh.com refactoring
# File: backend/app/api/api.py

"""API router configuration for the LuchoH Photography application."""

from fastapi import APIRouter
from app.api.endpoints import images, tags, auth, upload

api_router = APIRouter()
api_router.include_router(images.router, prefix="/images", tags=["images"])
api_router.include_router(tags.router, prefix="/tags", tags=["tags"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
