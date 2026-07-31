class CopilotService:

    def ask(self, question: str):

        question = question.lower()

        if "approve" in question:

            return {
                "answer": "This request should be reviewed by the approval agent.",
                "recommended_action": "Approval Required",
                "confidence": 0.95
            }

        elif "compliance" in question:

            return {
                "answer": "This request should be checked by the compliance agent.",
                "recommended_action": "Run Compliance Check",
                "confidence": 0.94
            }

        elif "document" in question:

            return {
                "answer": "Please validate the uploaded document.",
                "recommended_action": "Run Document Validation",
                "confidence": 0.93
            }

        else:

            return {
                "answer": "I couldn't understand your request.",
                "recommended_action": "Ask another question",
                "confidence": 0.50
            }


copilot_service = CopilotService()