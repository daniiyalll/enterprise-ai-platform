from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DecisionResponse(BaseModel):
    id: int
    agent_name: str
    decision: str
    reason: str
    confidence: float
    username: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DecisionHistoryResponse(BaseModel):
    total: int
    page: int
    page_size: int
    results: list[DecisionResponse]
