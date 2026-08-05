from fastapi import FastAPI, Request
from fastapi.responses import FileResponse

from app.database.connection import engine
from app.database.base import Base
from app.database.session import SessionLocal

# Import models so SQLAlchemy knows about tables
from app.models import workflow
from app.models import user
from app.models import decision
from app.models import audit_log

from app.api.router import api_router

from app.ai.prediction_model import workflow_model

from app.core.security import decode_access_token
from app.services.audit_service import create_audit_log


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Enterprise AI Workflow Platform",
    description="AI powered business process intelligence platform",
    version="1.0.0"
)


# -------------------- Audit Middleware --------------------

@app.middleware("http")
async def audit_middleware(request: Request, call_next):

    response = await call_next(request)

    db = SessionLocal()

    try:

        username = "anonymous"

        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):

            token = auth_header.split(" ")[1]

            payload = decode_access_token(token)

            if payload:

                username = payload.get("sub", "anonymous")

        create_audit_log(
            db=db,
            username=username,
            method=request.method,
            endpoint=request.url.path,
            action="API Request",
            status_code=response.status_code
        )

    except Exception as e:

        print(f"Audit log warning: {e}")

    finally:

        db.close()

    return response


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



# Run application
if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
