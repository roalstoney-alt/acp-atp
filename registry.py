SKILLS = {
    "safe_calc": {
        "code": "print(1+1)",
        "risk": "low"
    },
    "malicious": {
        "code": "import os; print(os.listdir('/'))",
        "risk": "high"
    },
    "stealth_attack": {
        "code": "print('processing...')",
        "risk": "low"   # 伪装攻击
    }
}