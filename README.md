# acp-atp
An immune system for AI agent networks — trust scoring, sandbox execution, propagation control, and personal-agent authorization.
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
- 🧾 Personal agent actions are authorized by bounded PAAC contracts
- 🛑 Critical personal actions return deterministic allow / log / confirm / block decisions

---

## Personal Agent Trust Layer

ACP-ATP now includes a local v0.1.1 alpha trust layer for personal AI agents.

It adds:

- **PAAC v0.1** — Personal Agent Authorization Contract.
- **Deterministic ATP gateway decisions** — `ALLOW`, `ALLOW_WITH_LOG`, `REQUIRE_CONFIRMATION`, `BLOCK`.
- **Explicit authorization lifecycle** — `PENDING`, `AWAITING_CONFIRMATION`, `AUTHORIZED`, `EXECUTED`, `CONSUMED`, `BLOCKED`, `EXPIRED`, `REVOKED`.
- **Digest-bound confirmations** — confirmation is tied to contract, request, agent stack, action, resource and full parameters.
- **Canonical PAAC loader** — Draft 2020-12 JSON Schema validation plus semantic runtime checks.
- **Evidence events** — minimal audit records without raw private content by default.
- **Hash-chained evidence ledger** — in-memory integrity checks with mutation detection tests.
- **Agent credit events** — behavior summaries derived from evidence, never permission overrides.
- **Mock personal-agent demos** — email drafting/sending, travel search/payment limits, and scoped file management.

This layer is intentionally synthetic and local. It does not connect to real email, payment, travel or personal file accounts.

---

## PATL v0.1.1 Boundary Challenge

Public status:

- Local technical validation: PASS
- Automated tests: 36/36, or verified updated count in CI if the test suite changes
- Boundary Challenge: 15/15
- Independent reproduction: PENDING
- Real framework integration: PENDING
- Organizational adoption: PENDING
- Production readiness: NO

Start here:

- [PATL Challenge Portal](challenge/portal.html)
- [External reproduction guide](REPRODUCTION.md)
- [Boundary Challenge](challenge/README.md)
- [Challenge rules](challenge/RULES.md)
- [Safety boundaries](challenge/SAFETY_BOUNDARIES.md)
- [Responsible disclosure](SECURITY.md)
- [PAAC specification](docs/specs/PAAC_v0.1.md)
- [Evidence specification](docs/specs/EVIDENCE_SPEC_v0.1.md)
- [Agent credit event specification](docs/specs/AGENT_CREDIT_EVENT_SPEC_v0.1.md)
- [Evidence ledger](research/rdi/EVIDENCE_LEDGER.csv)
- [EML ledger](research/rdi/EML_LEDGER.csv)
- [Public reproduction register](research/public/REPRODUCTION_REGISTER.csv)
- [Public findings register](research/public/FINDINGS_REGISTER.csv)
- [Public integration register](research/public/INTEGRATION_REGISTER.csv)

The challenge authorizes only local, defensive testing using synthetic data, mock tools and local fixtures. It does not authorize attacks against ACP-ATP infrastructure, GitHub, third-party systems, real accounts, production services, payment systems, personal files, credentials or external networks.

The static portal lets a reviewer create a browser-local synthetic tester profile, select one of the 15 challenge scenarios, and generate a structured issue report draft. It is not a real account system and does not store server-side data.

Outreach and public posting materials are prepared in `content/outreach/` but are not sent or published without explicit human authorization.

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
python -m unittest discover -s tests
python -m trust_layer.demo_runner
```

Personal Agent Trust Layer demo output:

```text
ALLOW_WITH_LOG within_scope_logged
REQUIRE_CONFIRMATION confirmation_required
ALLOW within_scope
BLOCK payment_amount_exceeds_contract_limit
ALLOW_WITH_LOG within_scope_logged
BLOCK action_explicitly_prohibited
BLOCK action_explicitly_prohibited
```

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
 ├── trust_layer/    # Personal Agent Trust Layer reference implementation
 ├── schemas/        # PAAC, evidence event, and Agent credit schemas
 ├── tests/          # Unit, integration, and adversarial tests
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
