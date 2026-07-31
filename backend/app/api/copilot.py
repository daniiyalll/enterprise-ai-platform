from fastapi import APIRouter
from pydantic import BaseModel

from app.services.copilot_service import copilot_service

router = APIRouter(
    prefix="/copilot",
    tags=["AI Copilot"]
)

class CopilotRequest(BaseModel):
    question: str

@router.post("/ask")
def ask_copilot(request: CopilotRequest):
    return copilot_service.ask(request.question)