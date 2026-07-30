class ComplianceAgent:

    def __init__(self):
        self.name = "Compliance Agent"


    def check(self, department, amount):

        restricted_departments = [
            "finance",
            "legal"
        ]


        if department.lower() in restricted_departments and amount > 50000:

            return {
                "agent": self.name,
                "status": "failed",
                "reason": "High value request requires compliance review"
            }


        return {
            "agent": self.name,
            "status": "passed",
            "reason": "Request complies with current policies"
        }



compliance_agent = ComplianceAgent()