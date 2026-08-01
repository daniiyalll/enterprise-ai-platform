from app.agents.approval_agent import approval_agent
from app.agents.compliance_agent import compliance_agent
from app.agents.document_agent import document_agent

from app.services.decision_service import save_decision


def get_confidence(outcome):

    positive = ["approved", "passed"]
    neutral = ["review_required"]
    negative = ["rejected", "failed"]

    if outcome in positive:
        return 0.95

    if outcome in neutral:
        return 0.60

    if outcome in negative:
        return 0.30

    return 0.50


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


    confidences = []


    # Save every agent decision with real confidence
    for result in results:

        outcome = result.get("decision", result.get("status"))

        confidence = get_confidence(outcome)
        confidences.append(confidence)

        save_decision(
            db=db,
            agent_name=result["agent"],
            decision=outcome,
            reason=result["reason"],
            confidence=confidence
        )


    overall_confidence = round(
        sum(confidences) / len(confidences),
        2
    )


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
        "overall_confidence": overall_confidence,
        "results": results
    }
