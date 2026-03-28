from scoring import AgentScore
from sandbox import run_in_sandbox
from registry import SKILLS

class Agent:
    def __init__(self, name):
        self.name = name
        self.score = AgentScore()

    def execute(self, skill_name):
        skill = SKILLS.get(skill_name)

        if not skill:
            return "Skill not found"

        # ACP-ATP检查
        if self.score.trust_score() < 0.5:
            return "Blocked: Low trust score"

        if skill["risk"] == "high":
            self.score.penalize("security")
            return "Blocked: High risk skill"

        # 沙盒执行
        output, error = run_in_sandbox(skill["code"])

        if error:
            self.score.penalize("failure")
            return f"Error: {error}"

        return output