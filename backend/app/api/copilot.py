from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional

from app.services.copilot_service import copilot_service
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/copilot",
    tags=["AI Copilot"]
)


class CopilotRequest(BaseModel):
    question: str
    amount: Optional[float] = None
    employee_level: Optional[str] = None
    department: Optional[str] = None
    document_type: Optional[str] = None
    has_signature: Optional[bool] = None
    has_required_fields: Optional[bool] = None


@router.post("/ask")
def ask_copilot(
    request: CopilotRequest,
    current_user = Depends(get_current_user)
):

    return copilot_service.ask(
        request.question,
        request.amount,
        request.employee_level,
        request.department,
        request.document_type,
        request.has_signature,
        request.has_required_fields
    )
