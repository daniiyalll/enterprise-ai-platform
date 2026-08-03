from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.services.decision_engine import make_decision
from app.services.decision_service import get_decision_history
from app.database.session import get_db
from app.schemas.decision import DecisionResponse
from app.core.permissions import require_manager


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
    current_user=Depends(require_manager)
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


@router.get("/history", response_model=list[DecisionResponse])
def history(
    db: Session = Depends(get_db),
    current_user=Depends(require_manager)
):

    return get_decision_history(db)