from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.services.copilot_service import copilot_service
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/copilot",
    tags=["AI Copilot"]
)

class CopilotRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_copilot(
    request: CopilotRequest,
    current_user = Depends(get_current_user)
):
    return copilot_service.ask(request.question)
