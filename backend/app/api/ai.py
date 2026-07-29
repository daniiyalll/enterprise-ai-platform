from fastapi import APIRouter
from pydantic import BaseModel
from app.ai.prediction_model import workflow_model

router = APIRouter(
    prefix="/ai",
    tags=["AI Prediction"]
)


class PredictionRequest(BaseModel):
    features: list[float]


@router.post("/predict")
def predict_risk(request: PredictionRequest):
    return workflow_model.predict(request.features)
