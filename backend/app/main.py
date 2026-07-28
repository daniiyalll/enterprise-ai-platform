from app.database.connection import engine
from app.database.base import Base
from app.models import workflow
from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api import workflows


app = FastAPI(
    title="Enterprise AI Workflow Platform",
    description="AI powered business process intelligence platform",
    version="1.0.0"
)


# Workflow API routes
app.include_router(
    workflows.router,
    prefix="/workflows",
    tags=["Workflows"]
)


# Home route
@app.get("/")
def home():
    return {
        "message": "Enterprise AI Platform API Running"
    }


# Browser favicon route
@app.get("/favicon.ico")
def favicon():
    return FileResponse("favicon.ico")