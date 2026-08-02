from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.database.connection import engine
from app.database.base import Base

# Import models so SQLAlchemy knows about tables
from app.models import workflow
from app.models import user
from app.models import decision

from app.ai.prediction_model import workflow_model

from app.api.router import api_router
from app.api import dashboard


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Enterprise AI Workflow Platform",
    description="AI powered business process intelligence platform",
    version="1.0.0"
)


# Register all API routes
app.include_router(
    api_router,
    prefix="/api/v1"
)


# Home route
@app.get("/")
def home():
    return {
        "message": "Enterprise AI Platform"
    }


# Favicon route
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("favicon.ico")


# Train / Load AI model
@app.on_event("startup")
def train_model_on_startup():

    try:
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

    except Exception as e:

        print(
            f"AI model startup warning: {e}"
        )

# Dashboard API routes
app.include_router(
    dashboard.router,
    tags=["Dashboard"]
)


# Run application
if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
