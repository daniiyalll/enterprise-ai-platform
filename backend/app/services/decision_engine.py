from app.agents.approval_agent import approval_agent
from app.agents.compliance_agent import compliance_agent
from app.agents.document_agent import document_agent

from app.services.decision_service import save_decision


POSITIVE_OUTCOMES = ["approved", "passed"]
NEUTRAL_OUTCOMES = ["review_required"]
NEGATIVE_OUTCOMES = ["rejected", "failed"]


def categorize(outcome):
    """Buckets a raw agent outcome into positive / neutral / negative / unknown."""

    if outcome in POSITIVE_OUTCOMES:
        return "positive"

    if outcome in NEUTRAL_OUTCOMES:
        return "neutral"

    if outcome in NEGATIVE_OUTCOMES:
        return "negative"

    return "unknown"


def get_confidence(outcome):
    """Base confidence for a single agent's own outcome."""

    category = categorize(outcome)

    if category == "positive":
        return 0.95

    if category == "neutral":
        return 0.60

    if category == "negative":
        return 0.30

    return 0.50


def get_agreement_adjustment(categories):
    """
    Adjusts overall confidence based on how much the agents agree with
    each other, not just their individual outcomes.

    - All agents land in the same bucket (full agreement)      -> boost
    - Agents split between positive and negative (hard clash)   -> big penalty
    - Any other mix (e.g. positive + neutral)                   -> smaller penalty
    """

    distinct = set(categories)

    if len(distinct) == 1:
        return 0.05

    if "positive" in distinct and "negative" in distinct:
        return -0.20

    return -0.08


def build_confidence_reasoning(categories, agreement_adjustment, overall_confidence):
    """Produces a formal, auditable explanation for why the confidence score landed where it did."""

    distinct = set(categories)
    positive_count = categories.count("positive")
    neutral_count = categories.count("neutral")
    negative_count = categories.count("negative")

    if len(distinct) == 1:
        basis = (
            f"All {len(categories)} agent checks reached the same conclusion "
            f"({next(iter(distinct))}), so the confidence score has been increased "
            f"by {agreement_adjustment:.2f} to reflect full agreement."
        )
    elif "positive" in distinct and "negative" in distinct:
        basis = (
            f"The agent checks produced conflicting results ({positive_count} positive, "
            f"{neutral_count} neutral, {negative_count} negative), which is a material "
            f"disagreement. The confidence score has been reduced by "
            f"{abs(agreement_adjustment):.2f} to reflect this conflict."
        )
    else:
        basis = (
            f"The agent checks did not fully align ({positive_count} positive, "
            f"{neutral_count} neutral, {negative_count} negative). The confidence score "
            f"has been reduced by {abs(agreement_adjustment):.2f} to reflect the partial disagreement."
        )

    return (
        f"{basis} Overall confidence: {overall_confidence:.2f} "
        f"({round(overall_confidence * 100)}%)."
    )


def build_decision_explanation(final_decision, results):
    """Produces a single, enterprise-readable summary of why the final decision was reached."""

    lines = []

    for result in results:
        outcome = result.get("decision", result.get("status"))
        lines.append(f"{result['agent']} — {outcome.replace('_', ' ')}: {result['reason']}.")

    findings = " ".join(lines)

    if final_decision == "rejected":
        headline = "Request rejected. At least one agent check failed and must be resolved before this can proceed."
    elif final_decision == "needs_review":
        headline = "Request requires manual review. No check failed outright, but one or more items need human sign-off."
    else:
        headline = "Request approved. All agent checks were satisfied with no outstanding issues."

    return f"{headline} {findings}"


def make_decision(
    db,
    amount,
    employee_level,
    department,
    document_type,
    has_signature,
    has_required_fields,
    username=None
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
    categories = []


    # Save every agent decision with real confidence
    for result in results:

        outcome = result.get("decision", result.get("status"))

        confidence = get_confidence(outcome)
        confidences.append(confidence)
        categories.append(categorize(outcome))

        save_decision(
            db=db,
            agent_name=result["agent"],
            decision=outcome,
            reason=result["reason"],
            confidence=confidence,
            username=username
        )


    base_confidence = sum(confidences) / len(confidences)
    adjustment = get_agreement_adjustment(categories)

    overall_confidence = round(
        min(1.0, max(0.0, base_confidence + adjustment)),
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
        "decision_explanation": build_decision_explanation(final_decision, results),
        "overall_confidence": overall_confidence,
        "confidence_reasoning": build_confidence_reasoning(categories, adjustment, overall_confidence),
        "agents_agreed": len(set(categories)) == 1,
        "results": results
    }
