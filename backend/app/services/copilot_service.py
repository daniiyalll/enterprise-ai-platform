from app.agents.approval_agent import approval_agent
from app.agents.compliance_agent import compliance_agent
from app.agents.document_agent import document_agent

from app.services.decision_engine import (
    categorize,
    get_confidence,
    get_confidence_level,
    POSITIVE_OUTCOMES,
    NEUTRAL_OUTCOMES,
    NEGATIVE_OUTCOMES
)


def explain_result(agent_label, result):
    """Turns a raw agent result into a formal, enterprise-readable explanation, status, and recommended action."""

    outcome = result.get("decision", result.get("status"))
    reason = result.get("reason", "")
    confidence = get_confidence(outcome)
    category = categorize(outcome)

    if category == "positive":
        return {
            "agent": agent_label,
            "status": "Cleared",
            "confidence": confidence,
            "confidence_level": get_confidence_level(confidence),
            "summary": f"{agent_label}: {reason}.",
            "recommended_action": "No action required — this check has been satisfied."
        }

    if category == "neutral":
        return {
            "agent": agent_label,
            "status": "Requires Review",
            "confidence": confidence,
            "confidence_level": get_confidence_level(confidence),
            "summary": f"{agent_label}: {reason}.",
            "recommended_action": "Escalate to a manager for manual sign-off before proceeding."
        }

    if category == "negative":
        return {
            "agent": agent_label,
            "status": "Blocked",
            "confidence": confidence,
            "confidence_level": get_confidence_level(confidence),
            "summary": f"{agent_label}: {reason}.",
            "recommended_action": "Resolve the issue above and resubmit; this will prevent final approval until addressed."
        }

    return {
        "agent": agent_label,
        "status": "Unknown",
        "confidence": confidence,
        "confidence_level": get_confidence_level(confidence),
        "summary": f"{agent_label}: {reason or outcome}.",
        "recommended_action": "Manual review recommended — outcome could not be classified automatically."
    }


class CopilotService:


    def ask(
        self,
        question: str,
        amount: float = None,
        employee_level: str = None,
        department: str = None,
        document_type: str = None,
        has_signature: bool = None,
        has_required_fields: bool = None
    ):

        question_lower = question.lower()

        response = {
            "question": question,
            "agents_used": [],
            "explanations": [],
            "recommendation": None,
            "workflow_guidance": None,
            "details": []
        }

        outcomes = []
        missing_fields = []


        # Approval Agent
        if "approve" in question_lower or "approval" in question_lower:

            if amount is None or employee_level is None:

                missing_fields.append("'amount' and 'employee_level' (for the Approval Agent)")

            else:

                approval_result = approval_agent.analyze(
                    amount,
                    employee_level
                )

                response["agents_used"].append("Approval Agent")
                response["details"].append(approval_result)
                response["explanations"].append(explain_result("Approval Agent", approval_result))
                outcomes.append(approval_result.get("decision", approval_result.get("status")))


        # Compliance Agent
        if "compliance" in question_lower or "policy" in question_lower:

            if amount is None or department is None:

                missing_fields.append("'amount' and 'department' (for the Compliance Agent)")

            else:

                compliance_result = compliance_agent.check(
                    department,
                    amount
                )

                response["agents_used"].append("Compliance Agent")
                response["details"].append(compliance_result)
                response["explanations"].append(explain_result("Compliance Agent", compliance_result))
                outcomes.append(compliance_result.get("decision", compliance_result.get("status")))


        # Document Agent
        if "document" in question_lower or "file" in question_lower:

            if document_type is None or has_signature is None or has_required_fields is None:

                missing_fields.append(
                    "'document_type', 'has_signature' and 'has_required_fields' (for the Document Agent)"
                )

            else:

                document_result = document_agent.validate(
                    document_type,
                    has_signature,
                    has_required_fields
                )

                response["agents_used"].append("Document Agent")
                response["details"].append(document_result)
                response["explanations"].append(explain_result("Document Agent", document_result))
                outcomes.append(document_result.get("decision", document_result.get("status")))


        # No agent matched at all — give real guidance instead of a dead end
        if len(response["agents_used"]) == 0 and len(missing_fields) == 0:

            response["recommendation"] = (
                "The system could not determine which check this question relates to."
            )
            response["workflow_guidance"] = (
                "Reference 'approval', 'compliance', or 'document' in the question, along with "
                "the relevant details. For example: \"Will this be approved?\" with an amount "
                "and employee_level; \"Does this pass compliance?\" with an amount and department; "
                "or \"Is this document valid?\" with document_type, has_signature, and has_required_fields."
            )
            return response

        if len(missing_fields) > 0:

            response["workflow_guidance"] = (
                "A complete answer requires the following additional details: "
                + "; ".join(missing_fields) + "."
            )

        if len(outcomes) > 0:

            has_negative = any(o in NEGATIVE_OUTCOMES for o in outcomes)
            has_neutral = any(o in NEUTRAL_OUTCOMES for o in outcomes)

            if has_negative:
                blocking_actions = [
                    e["recommended_action"] for e in response["explanations"]
                    if e["status"] == "Blocked"
                ]
                response["recommendation"] = (
                    "This request cannot proceed in its current form. "
                    + " ".join(blocking_actions)
                )
            elif has_neutral:
                response["recommendation"] = (
                    "This request does not meet the criteria for automatic clearance "
                    "and requires manual review before it can proceed."
                )
            else:
                response["recommendation"] = (
                    "This request meets all applicable checks and may proceed."
                )

            response["overall_confidence"] = round(
                sum(e["confidence"] for e in response["explanations"]) / len(response["explanations"]),
                2
            )
            response["confidence_level"] = get_confidence_level(response["overall_confidence"])

        return response



copilot_service = CopilotService()
