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