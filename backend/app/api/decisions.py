from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.services.decision_engine import make_decision
from app.database.session import get_db
from app.core.dependencies import get_current_user


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
def evaluate(
    request: DecisionRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return make_decision(
        db,
        request.amount,
        request.employee_level,
        request.department,
        request.document_type,
        request.has_signature,
        request.has_required_fields
    )
