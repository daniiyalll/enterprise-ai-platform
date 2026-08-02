from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.workflow import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowResponse
)

from app.services.workflow_engine import (
    create_workflow,
    get_workflows,
    get_workflow_by_id,
    update_workflow,
    delete_workflow
)

from app.core.permissions import (
    require_employee,
    require_manager,
    require_admin
)


router = APIRouter(
    prefix="/workflows",
    tags=["Workflows"]
)



# Manager + Admin only
@router.post(
    "/",
    response_model=WorkflowResponse
)
def create(
    workflow: WorkflowCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_manager)
):

    return create_workflow(
        db,
        workflow
    )



# Everyone logged in
@router.get(
    "/",
    response_model=list[WorkflowResponse]
)
def read_all(
    db: Session = Depends(get_db),
    current_user = Depends(require_employee)
):

    return get_workflows(db)



# Everyone logged in
@router.get(
    "/{workflow_id}",
    response_model=WorkflowResponse
)
def read_one(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_employee)
):

    workflow = get_workflow_by_id(
        db,
        workflow_id
    )


    if not workflow:

        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )


    return workflow



# Manager + Admin only
@router.put(
    "/{workflow_id}",
    response_model=WorkflowResponse
)
def update(
    workflow_id: int,
    workflow: WorkflowUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_manager)
):

    updated = update_workflow(
        db,
        workflow_id,
        workflow
    )


    if not updated:

        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )


    return updated



# Admin only
@router.delete(
    "/{workflow_id}"
)
def delete(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):

    deleted = delete_workflow(
        db,
        workflow_id
    )


    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )


    return {
        "message": f"Workflow {workflow_id} deleted successfully"
    }