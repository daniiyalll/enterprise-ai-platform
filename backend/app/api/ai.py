from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.ai.prediction_model import workflow_model
from app.core.permissions import require_employee


router = APIRouter(
    prefix="/ai",
    tags=["AI Prediction"]
)


class PredictionRequest(BaseModel):
    features: list[float]


@router.post("/predict")
def predict_risk(
    request: PredictionRequest,
    current_user=Depends(require_employee)
):

    return workflow_model.predict(
        request.features
    )