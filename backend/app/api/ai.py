from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.ai.prediction_model import workflow_model
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/ai",
    tags=["AI Prediction"]
)


class PredictionRequest(BaseModel):
    features: list[float]


@router.post("/predict")
def predict_risk(
    request: PredictionRequest,
    current_user = Depends(get_current_user)
):
    return workflow_model.predict(request.features)
