from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.services.decision_engine import make_decision
from app.services.decision_service import get_decision_history
from app.database.session import get_db
from app.schemas.decision import DecisionHistoryResponse
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
        request.has_required_fields,
        username=current_user.username
    )


@router.get("/history", response_model=DecisionHistoryResponse)
def history(
    agent_name: Optional[str] = Query(None, description="Filter by agent, e.g. 'Compliance Agent'"),
    decision: Optional[str] = Query(None, description="Filter by outcome, e.g. 'approved', 'rejected'"),
    username: Optional[str] = Query(None, description="Filter by the user who triggered the decision"),
    date_from: Optional[datetime] = Query(None, description="Only decisions on/after this timestamp"),
    date_to: Optional[datetime] = Query(None, description="Only decisions on/before this timestamp"),
    page: int = Query(1, ge=1, description="Page number, starting at 1"),
    page_size: int = Query(20, ge=1, le=200, description="Results per page (max 200)"),
    db: Session = Depends(get_db),
    current_user=Depends(require_manager)
):

    return get_decision_history(
        db,
        agent_name=agent_name,
        decision=decision,
        username=username,
        date_from=date_from,
        date_to=date_to,
        page=page,
        page_size=page_size
    )
