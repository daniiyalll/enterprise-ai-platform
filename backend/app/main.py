from app.database.connection import engine
from app.database.base import Base
from app.models import workflow
from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.ai.prediction_model import workflow_model

from app.api import workflows
from app.api import process_mining
from app.api import ai
from app.api import auth
from app.api import agents
from app.api import decisions


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

# AI Prediction API routes
app.include_router(
    ai.router,
    tags=["AI Prediction"]
)

# Authentication API routes
app.include_router(
    auth.router,
    tags=["Authentication"]
)

# AI Agents API routes
app.include_router(
    agents.router,
    tags=["AI Agents"]
)

# Decision Engine API routes
app.include_router(
    decisions.router,
    tags=["Decision Engine"]
)

# Home route
@app.get("/")
def home():
    return {
        "message": "Enterprise AI Platform"
    }


# Browser favicon route
@app.get("/favicon.ico")
def favicon():
    return FileResponse("favicon.ico")


@app.on_event("startup")
def train_model_on_startup():
    if workflow_model.is_trained():
        workflow_model.load()
        print("Saved AI model loaded (no retraining needed).")
    else:
        accuracy = workflow_model.train("dataset/risk_training_data.csv")
        print(f"AI model trained for the first time! Accuracy: {accuracy}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
