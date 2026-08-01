from pydantic import BaseModel


class DecisionResponse(BaseModel):
    id: int
    agent_name: str
    decision: str
    reason: str
    confidence: float

    class Config:
        from_attributes = True
