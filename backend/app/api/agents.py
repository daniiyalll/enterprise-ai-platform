from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.agents.approval_agent import approval_agent
from app.agents.compliance_agent import compliance_agent
from app.agents.document_agent import document_agent
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/agents",
    tags=["AI Agents"]
)


class ComplianceRequest(BaseModel):
    department: str
    amount: float


@router.post("/compliance")
def compliance_check(
    request: ComplianceRequest,
    current_user = Depends(get_current_user)
):

    result = compliance_agent.check(
        request.department,
        request.amount
    )

    return result



class ApprovalRequest(BaseModel):
    amount: float
    employee_level: str


@router.post("/approval")
def approval_check(
    request: ApprovalRequest,
    current_user = Depends(get_current_user)
):

    result = approval_agent.analyze(
        request.amount,
        request.employee_level
    )

    return result



class DocumentRequest(BaseModel):
    document_type: str
    has_signature: bool
    has_required_fields: bool


@router.post("/document")
def document_check(
    request: DocumentRequest,
    current_user = Depends(get_current_user)
):

    result = document_agent.validate(
        request.document_type,
        request.has_signature,
        request.has_required_fields
    )

    return result
