from app.agents.approval_agent import approval_agent
from app.agents.compliance_agent import compliance_agent
from app.agents.document_agent import document_agent

from app.services.decision_service import save_decision


def make_decision(
    db,
    amount,
    employee_level,
    department,
    document_type,
    has_signature,
    has_required_fields
):

    results = []


    # Approval Agent
    approval_result = approval_agent.analyze(
        amount,
        employee_level
    )

    results.append(approval_result)


    # Compliance Agent
    compliance_result = compliance_agent.check(
        department,
        amount
    )

    results.append(compliance_result)


    # Document Agent
    document_result = document_agent.validate(
        document_type,
        has_signature,
        has_required_fields
    )

    results.append(document_result)



    # Save every agent decision
    for result in results:

        save_decision(
            db=db,
            agent_name=result["agent"],
            decision=result.get(
                "decision",
                result.get("status")
            ),
            reason=result["reason"],
            confidence=0.90
        )


    return {
        "message": "Decision evaluation completed",
        "results": results
    }