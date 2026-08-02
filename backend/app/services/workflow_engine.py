from sqlalchemy.orm import Session
from app.models.workflow import Workflow


def create_workflow(db: Session, workflow_data):

    workflow = Workflow(
        name=workflow_data.name,
        description=workflow_data.description
    )

    db.add(workflow)
    db.commit()
    db.refresh(workflow)

    return workflow


def get_workflows(db: Session):

    return db.query(Workflow).all()


def get_workflow_by_id(db: Session, workflow_id: int):

    return db.query(Workflow).filter(
        Workflow.id == workflow_id
    ).first()


def update_workflow(db: Session, workflow_id: int, workflow_data):

    workflow = get_workflow_by_id(db, workflow_id)

    if not workflow:
        return None

    if workflow_data.name is not None:
        workflow.name = workflow_data.name

    if workflow_data.description is not None:
        workflow.description = workflow_data.description

    if workflow_data.status is not None:
        workflow.status = workflow_data.status

    if workflow_data.is_active is not None:
        workflow.is_active = workflow_data.is_active

    db.commit()
    db.refresh(workflow)

    return workflow


def delete_workflow(db: Session, workflow_id: int):

    workflow = get_workflow_by_id(db, workflow_id)

    if not workflow:
        return None

    db.delete(workflow)
    db.commit()

    return workflow
