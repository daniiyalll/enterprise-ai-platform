from app.agents.approval_agent import approval_agent
from app.agents.compliance_agent import compliance_agent
from app.agents.document_agent import document_agent


def make_decision(
    amount,
    employee_level,
    department,
    document_type,
    has_signature,
    has_required_fields
):

    approval_result = approval_agent.analyze(
        amount,
        employee_level
    )

    compliance_result = compliance_agent.check(
        department,
        amount
    )

    document_result = document_agent.validate(
        document_type,
        has_signature,
        has_required_fields
    )

    results = [approval_result, compliance_result, document_result]

    hard_reject = any(
        r.get("status") in ["failed", "rejected"]
        for r in results
    )

    needs_review = any(
        r.get("decision") == "review_required"
        for r in results
    )

    if hard_reject:
        final_decision = "rejected"
    elif needs_review:
        final_decision = "needs_review"
    else:
        final_decision = "approved"

    return {
        "final_decision": final_decision,
        "approval_agent": approval_result,
        "compliance_agent": compliance_result,
        "document_agent": document_result
    }
