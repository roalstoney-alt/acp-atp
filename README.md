# acp-atp
An immune system for AI agent networks — trust scoring, sandbox execution, and propagation control.
<img width="1024" height="1536" alt="ChatGPT Image Mar 28, 2026, 11_15_54 PM" src="https://github.com/user-attachments/assets/eceaf76d-85ff-4193-abc6-7190d8d0b171" />

# ACP-ATP  
### Adaptive Credit & Trust Protocol  
#### An Immune System for AI Agent Networks

---

## 🧠 Why This Exists

AI agents are starting to:

- Share skills  
- Execute code autonomously  
- Learn from each other  

But one fundamental problem remains unsolved:

> **What stops malicious capabilities from spreading across agent networks?**

---

## ⚠️ The Problem

When AI agents share skills:

- Capability = Executable Code  
- Code = Attack Surface  

This creates a new systemic risk:

### **Unbounded Capability Propagation**

- One compromised skill → spreads across agents  
- Agents auto-execute → no human checkpoint  
- Failure scales faster than detection  

---

## 🛡️ The Solution: ACP-ATP

> **ACP-ATP introduces a Trust & Propagation Control Layer for AI systems**

It ensures:

- ❌ No capability is trusted by default  
- 🔒 Execution is isolated  
- 📉 Risk propagation is constrained  
- ⚖️ Trust is continuously computed


---

## 🧬 Architecture Overview

GPT / LLM (Decision Engine)
↓
Structured Action (JSON)
↓
ACP-ATP Layer
├── Trust Scoring (C_b, C_s, C_p)
├── Permission Validation
├── Risk Assessment
├── Propagation Control
└── Circuit Breaker
↓
Sandbox Execution
↓
Execution Logs → Trust Score Update

---


---

## 🔑 Core Concepts

### 1. Skill Capsule

All capabilities are packaged as:

- Immutable  
- Verifiable  
- Permission-scoped  
- Non-executable without ACP-ATP  

---

### 2. Multi-Dimensional Trust

Each agent is evaluated by:

- **Behavior Score (C_b)** — performance  
- **Security Score (C_s)** — safety compliance  
- **Propagation Score (C_p)** — network trust  


T = w1C_b + w2C_s + w3*C_p


---

### 3. Zero-Trust Execution

- No direct execution  
- All actions go through ACP-ATP  
- Mandatory sandbox isolation  

---

### 4. Controlled Propagation

- Rate-limited capability spread  
- Tiered agent network  
- No uncontrolled scaling  

---

### 5. Circuit Breaker

- Detect anomalies  
- Freeze propagation  
- Isolate affected agents  

---

## 🚀 Demo (Minimal Working Example)

This repo includes a minimal prototype demonstrating:

- ✅ Trust-based execution blocking  
- ✅ Sandbox execution  
- ✅ Security penalty system  

Run:

```bash
python main.py

Example output:
--- NO PROTECTION: malicious ---
agent_0: Executed: malicious
agent_1: Executed: malicious
agent_2: Executed: malicious

--- ACP-ATP Enabled: malicious ---
agent_0: Blocked: High risk skill | trust=0.88
agent_1: Blocked: High risk skill | trust=0.88
agent_2: Blocked: High risk skill | trust=0.88


📁 Project Structure

acp-atp/
 ├── agent.py        # Agent execution logic
 ├── scoring.py      # Trust scoring engine
 ├── sandbox.py      # Execution isolation
 ├── registry.py     # Skill definitions
 ├── main.py         # Demo entry point
 └── whitepaper.md   # Full protocol design

🧪 What This Demo Proves

Even in a minimal setup, ACP-ATP can:

Prevent execution of high-risk capabilities
Penalize unsafe behavior
Reduce trust dynamically
Limit propagation potential
🌍 Why This Matters

AI systems are evolving into networks — not tools.

Without a control layer:

One malicious capability can infect thousands of agents
Autonomous systems amplify risk faster than humans can react
ACP-ATP introduces:

An immune system for AI ecosystems

🧠 Key Insight

ACP-ATP does not prevent harmful intelligence —
it prevents harmful intelligence from scaling.

📌 Roadmap
Phase 1 (Current)
 Trust scoring system
 Sandbox execution
 Minimal agent model
Phase 2
 Propagation control
 Circuit breaker system
 Multi-agent simulation
Phase 3
 Decentralized trust network
 On-chain reputation (optional)
 WASM / microVM sandbox
🤝 Contributing

This is an early-stage protocol design.

We welcome:

Security researchers
AI engineers
Distributed systems experts
📄 Whitepaper

See: whitepaper.md

🚀 Vision

We believe:

The future of AI is not just about intelligence —
but about controlled, trustworthy evolution

⭐ If this resonates
Star the repo
Share the idea
Join the discussion
📬 Contact

Open an issue or start a discussion.

🧩 Final Thought

When AI agents can share skills,
the most important question is not
"how fast they learn"
but
"what prevents bad ideas from spreading?"
