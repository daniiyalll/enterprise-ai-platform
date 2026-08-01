from app.agents.approval_agent import approval_agent
from app.agents.compliance_agent import compliance_agent
from app.agents.document_agent import document_agent


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
            "recommendation": None,
            "details": []
        }


        # Approval Agent
        if "approve" in question_lower or "approval" in question_lower:

            if amount is None or employee_level is None:

                response["details"].append({
                    "agent": "Approval Agent",
                    "error": "Please provide 'amount' and 'employee_level' for a real answer."
                })

            else:

                approval_result = approval_agent.analyze(
                    amount,
                    employee_level
                )

                response["agents_used"].append("Approval Agent")
                response["details"].append(approval_result)


        # Compliance Agent
        if "compliance" in question_lower or "policy" in question_lower:

            if amount is None or department is None:

                response["details"].append({
                    "agent": "Compliance Agent",
                    "error": "Please provide 'amount' and 'department' for a real answer."
                })

            else:

                compliance_result = compliance_agent.check(
                    department,
                    amount
                )

                response["agents_used"].append("Compliance Agent")
                response["details"].append(compliance_result)


        # Document Agent
        if "document" in question_lower or "file" in question_lower:

            if document_type is None or has_signature is None or has_required_fields is None:

                response["details"].append({
                    "agent": "Document Agent",
                    "error": "Please provide 'document_type', 'has_signature' and 'has_required_fields' for a real answer."
                })

            else:

                document_result = document_agent.validate(
                    document_type,
                    has_signature,
                    has_required_fields
                )

                response["agents_used"].append("Document Agent")
                response["details"].append(document_result)


        if len(response["agents_used"]) == 0:

            response["recommendation"] = (
                "No suitable agent found for this request, or required data was missing."
            )

        else:

            response["recommendation"] = (
                "Request processed by AI agents using the provided data."
            )


        return response



copilot_service = CopilotService()
