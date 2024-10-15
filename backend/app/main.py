# Project: luchoh.com refactoring
# File: backend/app/main.py
"""
Main application module for the luchoh.com backend.

This module initializes the FastAPI application, sets up routes,
and configures CORS and static file serving.
"""

import logging
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.api import api_router
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LuchoH Photography API", openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

print("BACKEND_CORS_ORIGINS:", settings.BACKEND_CORS_ORIGINS_LIST)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS_LIST:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS_LIST,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Set up templates
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

# Set up static files
static_dir = os.path.join(current_dir, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

uploads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../uploads")
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")


@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {"message": "Welcome to LuchoH Photography API"}


@app.get("/api/config")
async def get_config():
    """
    Endpoint to retrieve the default tag configuration.

    Returns:
        JSONResponse: A JSON response containing the DEFAULT_TAG configuration.
    """
    return JSONResponse({"DEFAULT_TAG": settings.DEFAULT_TAG})


@app.get("/admin")
async def admin(request: Request):
    """
    Admin page endpoint.

    Args:
        request (Request): The incoming request object.

    Returns:
        TemplateResponse: Renders the admin.html template with request and settings context.
    """
    return templates.TemplateResponse(
        "admin.html", {"request": request, "settings": settings}
    )
