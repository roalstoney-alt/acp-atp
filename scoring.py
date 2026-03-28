class AgentScore:
    def __init__(self):
        self.behavior = 1.0
        self.security = 1.0
        self.propagation = 1.0

    def trust_score(self):
        return 0.4*self.behavior + 0.4*self.security + 0.2*self.propagation

    def penalize(self, reason):
        if reason == "security":
            self.security -= 0.3
        elif reason == "failure":
            self.behavior -= 0.2

        self.security = max(0, self.security)
        self.behavior = max(0, self.behavior)