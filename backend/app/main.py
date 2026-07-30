from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.database.connection import engine
from app.database.base import Base
from app.models import workflow

from app.ai.prediction_model import workflow_model
from app.api.router import api_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Enterprise AI Workflow Platform",
    description="AI powered business process intelligence platform",
    version="1.0.0"
)

# Register the unified API router (Includes Workflows, Process Mining, AI, and Health)
app.include_router(api_router, prefix="/api/v1")

# Home route
@app.get("/")
def home():
    return {
        "message": "Enterprise AI Platform API Running"
    }

# Browser favicon route
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("favicon.ico")

<<<<<<< HEAD
# Train AI model when server starts
@app.on_event("startup")
def train_model_on_startup():
    try:
        accuracy = workflow_model.train("dataset/risk_training_data.csv")
        print(f"AI model trained successfully! Accuracy: {accuracy}")
    except Exception as e:
        print(f"Startup warning - AI model training failed: {e}")
=======
 @app.on_event("startup")
def train_model_on_startup():
    if workflow_model.is_trained():
        workflow_model.load()
        print("Saved AI model loaded (no retraining needed).")
    else:
        accuracy = workflow_model.train("dataset/risk_training_data.csv")
        print(f"AI model trained for the first time! Accuracy: {accuracy}")
>>>>>>> 90b4e5d784ba28eaf12d21df8b27f30eebf0074c

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )