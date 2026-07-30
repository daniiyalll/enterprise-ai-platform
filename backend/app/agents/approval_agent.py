class ApprovalAgent:

    def __init__(self):
        self.name = "Approval Agent"


    def analyze(self, amount, employee_level):

        if amount <= 10000 and employee_level != "intern":

            return {
                "agent": self.name,
                "decision": "approved",
                "reason": "Request meets approval policy"
            }


        return {
            "agent": self.name,
            "decision": "review_required",
            "reason": "Needs human approval"
        }



approval_agent = ApprovalAgent()