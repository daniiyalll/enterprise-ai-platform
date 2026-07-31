from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.database.connection import engine
from app.database.base import Base
from app.models import workflow

from app.ai.prediction_model import workflow_model
from app.api.router import api_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Enterprise AI Workflow Platform",
    description="AI powered business process intelligence platform",
    version="1.0.0"
)


# Register all APIs
app.include_router(
    api_router,
    prefix="/api/v1"
)


@app.get("/")
def home():
    return {
        "message": "Enterprise AI Platform"
    }


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("favicon.ico")


@app.on_event("startup")
def train_model_on_startup():

    if workflow_model.is_trained():

        workflow_model.load()
        print("Saved AI model loaded.")

    else:

        accuracy = workflow_model.train(
            "dataset/risk_training_data.csv"
        )

        print(
            f"AI model trained. Accuracy: {accuracy}"
        )