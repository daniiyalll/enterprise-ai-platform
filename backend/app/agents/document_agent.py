class DocumentAgent:

    def __init__(self):
        self.name = "Document Agent"


    def validate(
        self,
        document_type,
        has_signature,
        has_required_fields
    ):

        if not has_signature:

            return {
                "agent": self.name,
                "status": "rejected",
                "reason": "Missing document signature"
            }


        if not has_required_fields:

            return {
                "agent": self.name,
                "status": "rejected",
                "reason": "Missing required document fields"
            }


        return {
            "agent": self.name,
            "status": "approved",
            "reason": f"{document_type} document verified successfully"
        }



document_agent = DocumentAgent()