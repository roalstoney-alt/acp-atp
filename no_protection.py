from registry import SKILLS

class UnsafeAgent:
    def __init__(self, name):
        self.name = name

    def execute(self, skill_name):
        skill = SKILLS.get(skill_name)
        if not skill:
            return "Skill not found"

        # ❌ 无任何安全机制
        return f"Executed: {skill_name}"