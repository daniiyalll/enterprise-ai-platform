from pydantic import BaseModel
from typing import Optional


class WorkflowCreate(BaseModel):
    name: str
    description: str


class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None


class WorkflowResponse(BaseModel):
    id: int
    name: str
    description: str
    status: str
    is_active: bool

    class Config:
        from_attributes = True
