from agent import Agent
from no_protection import UnsafeAgent

agents_safe = [Agent(f"agent_{i}") for i in range(3)]
agents_unsafe = [UnsafeAgent(f"agent_{i}") for i in range(3)]

def simulate_safe(skill):
    print(f"\n--- ACP-ATP Enabled: {skill} ---")
    for agent in agents_safe:
        result = agent.execute(skill)
        print(f"{agent.name}: {result} | trust={agent.score.trust_score():.2f}")

def simulate_unsafe(skill):
    print(f"\n--- NO PROTECTION: {skill} ---")
    for agent in agents_unsafe:
        result = agent.execute(skill)
        print(f"{agent.name}: {result}")

simulate_unsafe("malicious")
simulate_safe("malicious")