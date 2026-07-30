from fastapi import APIRouter
from pydantic import BaseModel

from app.services.decision_engine import make_decision


router = APIRouter(
    prefix="/decisions",
    tags=["Decision Engine"]
)


class DecisionRequest(BaseModel):
    amount: float
    employee_level: str
    department: str
    document_type: str
    has_signature: bool
    has_required_fields: bool


@router.post("/evaluate")
def evaluate(request: DecisionRequest):

    return make_decision(
        request.amount,
        request.employee_level,
        request.department,
        request.document_type,
        request.has_signature,
        request.has_required_fields
    )
