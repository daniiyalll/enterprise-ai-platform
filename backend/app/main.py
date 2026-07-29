from app.database.connection import engine
from app.database.base import Base
from app.models import workflow
from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api import workflows
from app.api import process_mining


app = FastAPI(
    title="Enterprise AI Workflow Platform",
    description="AI powered business process intelligence platform",
    version="1.0.0"
)


# Workflow API routes
app.include_router(
    workflows.router,
    tags=["Workflows"]
)

# Process Mining API routes
app.include_router(
    process_mining.router,
    prefix="/process-mining",
    tags=["Process Mining"]
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


 
     
