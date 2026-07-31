from app.agents.approval_agent import approval_agent
from app.agents.compliance_agent import compliance_agent
from app.agents.document_agent import document_agent


class CopilotService:


    def ask(self, question: str):

        question = question.lower()

        response = {
            "question": question,
            "agents_used": [],
            "recommendation": None,
            "details": []
        }


        # Approval Agent
        if "approve" in question or "approval" in question:

            approval_result = approval_agent.analyze(
                amount=5000,
                employee_level="manager"
            )

            response["agents_used"].append("Approval Agent")
            response["details"].append(
                approval_result
            )


        # Compliance Agent
        if "compliance" in question or "policy" in question:

            compliance_result = compliance_agent.check(
                department="general",
                amount=5000
            )

            response["agents_used"].append("Compliance Agent")
            response["details"].append(
                compliance_result
            )


        # Document Agent
        if "document" in question or "file" in question:

            document_result = document_agent.validate(
                document_type="contract",
                has_signature=True,
                has_required_fields=True
            )

            response["agents_used"].append("Document Agent")
            response["details"].append(
                document_result
            )


        if len(response["agents_used"]) == 0:

            response["recommendation"] = (
                "No suitable agent found for this request."
            )

        else:

            response["recommendation"] = (
                "Request processed by AI agents."
            )


        return response



copilot_service = CopilotService()