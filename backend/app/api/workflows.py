from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate, WorkflowResponse
from app.services.workflow_engine import (
    create_workflow,
    get_workflows,
    get_workflow_by_id,
    update_workflow,
    delete_workflow
)
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/workflows",
    tags=["Workflows"]
)


@router.post("/", response_model=WorkflowResponse)
def create(
    workflow: WorkflowCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return create_workflow(db, workflow)


@router.get("/", response_model=list[WorkflowResponse])
def read_all(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return get_workflows(db)


@router.get("/{workflow_id}", response_model=WorkflowResponse)
def read_one(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    workflow = get_workflow_by_id(db, workflow_id)

    if not workflow:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    return workflow


@router.put("/{workflow_id}", response_model=WorkflowResponse)
def update(
    workflow_id: int,
    workflow: WorkflowUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    updated = update_workflow(db, workflow_id, workflow)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    return updated


@router.delete("/{workflow_id}")
def delete(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    deleted = delete_workflow(db, workflow_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    return {"message": f"Workflow {workflow_id} deleted successfully"}
 
