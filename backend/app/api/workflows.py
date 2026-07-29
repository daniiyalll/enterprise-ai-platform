from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.workflow import WorkflowCreate, WorkflowResponse
from app.services.workflow_engine import (
    create_workflow,
    get_workflows
)


router = APIRouter(
    prefix="/workflows",
    tags=["Workflows"]
)


@router.post("/", response_model=WorkflowResponse)
def create(
    workflow: WorkflowCreate,
    db: Session = Depends(get_db)
):

    return create_workflow(db, workflow)


@router.get("/", response_model=list[WorkflowResponse])
def read_all(
    db: Session = Depends(get_db)
):

    return get_workflows(db)
