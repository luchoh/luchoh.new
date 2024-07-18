# Project: luchoh.com refactoring
# File: backend/app/main.py
import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.api.api import api_router
from app.core.config import settings
# from app.db.session import engine
# from app.models import base, user, image, gallery

# Create tables
# base.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LuchoH Photography API", openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
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


@app.get("/")
async def root():
    return {"message": "Welcome to LuchoH Photography API"}


@app.get("/admin")
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})
