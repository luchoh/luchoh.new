import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.api.api import api_router
# from app.db.session import engine
# from app.models import base, user, image, gallery

# Create tables
# base.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LuchoH Photography API")

app.include_router(api_router)

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
