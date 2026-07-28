from fastapi import APIRouter


router = APIRouter()


workflows = []


@router.post("/")
def create_workflow(workflow: dict):

    workflows.append(workflow)

    return {
        "message": "Workflow created successfully",
        "workflow": workflow
    }



@router.get("/")
def get_workflows():

    return {
        "total": len(workflows),
        "workflows": workflows
    }



@router.get("/{workflow_id}")
def get_workflow(workflow_id: int):

    if workflow_id >= len(workflows):
        return {
            "error": "Workflow not found"
        }

    return workflows[workflow_id]