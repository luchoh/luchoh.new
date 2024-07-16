from fastapi import APIRouter
from app.api.endpoints import images, galleries, auth, upload

api_router = APIRouter()
api_router.include_router(images.router, prefix="/images", tags=["images"])
api_router.include_router(galleries.router, prefix="/galleries", tags=["galleries"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
