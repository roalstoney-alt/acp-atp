ACP — Adaptive Credit Propagation Protocol
A Trust Layer for Autonomous AI Agent Networks
1. Abstract

ACP (Adaptive Credit Propagation) is a protocol that models AI agent interactions as a dynamic propagation network, where trust, risk, and responsibility are continuously distributed across execution chains.

Unlike traditional evaluation systems that assess agents in isolation, ACP introduces a propagation-based credit model in which each agent’s output affects downstream performance and is influenced by upstream dependencies.

This enables real-time containment of failures, incentivizes reliable behavior, and establishes a self-regulating trust layer for autonomous agent ecosystems.

2. Problem Statement
2.1 Fragmented Trust in AI Systems

Current AI ecosystems lack a fundamental mechanism:

There is no propagation of responsibility.

In multi-agent workflows:

Agent A produces an output
Agent B uses it
Agent C fails

Yet no system identifies or attributes responsibility across the chain.

2.2 Lack of Propagation Awareness

Most evaluation systems assume:

score = f(local performance)

However, in real systems:

output → becomes another agent’s input

Errors are not isolated—they propagate.

2.3 Systemic Risk in Agent Networks

Agent-based systems introduce cascading risks:

Prompt injection attacks
Model degradation (drift)
Tool/API failures

These can lead to:

Cascade failures across entire execution chains.

3. Core Concept
3.1 Execution as a Graph

ACP models agent interactions as a:

Directed Propagation Graph

Where:

Nodes represent execution events
Edges represent dependencies (parent → child)
3.2 Propagation Unit

Each execution trace includes:

parent_id — upstream dependency
propagation_group — chain identifier
propagation_depth — distance from origin

This forms complete execution chains:

A → B → C → D
3.3 Trust is Propagated

Core principle:

Trust is not assigned — it is propagated.

An agent’s reliability is shaped not only by its own performance, but by its position within a network of dependencies.

4. Credit Propagation Model
4.1 Base Score

Each agent starts with a local performance score:

BaseScore = 0.6 × success_rate + 0.4 × acceptance_rate
4.2 Propagation Formula

ACP extends this into a network-aware model:

Score(node) =
    BaseScore(node)
  + α × ParentInfluence
  + β × ChildFeedback

Recommended parameters:

α = 0.3 (upstream influence)
β = 0.2 (downstream feedback)
4.3 Interpretation
Component	Meaning
BaseScore	Intrinsic performance
ParentInfluence	Quality of upstream dependencies
ChildFeedback	Impact on downstream agents
4.4 Key Insight

An agent is not an isolated unit — it is a node in a living system.

5. Incentive Mechanism
5.1 Positive Incentives

Agents are rewarded when they:

Are frequently selected (high acceptance rate)
Appear in high-quality execution chains
Produce stable and reliable outputs

Result:

Higher score → greater visibility → more usage
5.2 Negative Incentives

Agents are penalized when they:

Produce unreliable or incorrect outputs
Contribute to failing chains
Reduce downstream success rates

Result:

Lower score → reduced usage → potential isolation
5.3 Propagation Responsibility (Key Innovation)

ACP introduces a new accountability model:

An agent is responsible not only for its output,
but also for the consequences of that output.

This creates network-level accountability, not just local evaluation.

6. Disaster Scenarios
6.1 Prompt Injection Attack

Propagation pattern:

Malicious Agent → LLM → Tool → User
Risks:
Rapid spread of incorrect or manipulated outputs
No visibility into origin
No accountability chain
ACP Response:
Track full propagation chain
Detect abnormal patterns
Reduce trust and propagation weight
Contain spread
6.2 Model Drift Cascade

Scenario:

Agent A degrades → Agent B degrades → Agent C fails
Risks:
Silent degradation across systems
Root cause becomes invisible
ACP Response:
Downstream failures propagate backward
Root cause agents lose trust score
Enables automatic detection of degraded nodes
6.3 Central Node Failure

Scenario:

Many agents → Core agent → Many dependents

If the core agent fails:

Entire system is affected
High systemic fragility
ACP Response:
Dynamic score decay
Reduced propagation influence
Fallback agent routing
Risk redistribution
7. Containment Mechanisms
7.1 Propagation Depth Limit
max_depth = N

Limits how far influence can spread.

7.2 Propagation Decay
weight = base × (λ ^ depth)

Ensures distant nodes have reduced influence.

7.3 Anomaly Detection

Triggers:

Sudden drop in success rate
Abnormal acceptance patterns

Actions:

Degrade → Flag → Isolate
7.4 Quarantine Mechanism

State transitions:

Normal → Risk → Quarantined

Quarantined agents:

Are excluded from propagation
Cannot influence downstream nodes
7.5 Trust Tiers

Agents are categorized into tiers:

Tier 1 → Tier 2 → Tier 3

Each tier determines:

Propagation weight
Access level
System privileges
8. System Architecture
CLI / API → Execution Logs → Database
                         ↓
                   Scoring Engine
                         ↓
                      API Layer
                         ↓
          Visualization / Graph / Simulation
9. Demonstration Narrative (30s Viral Demo)

ACP can be demonstrated visually through a simple simulation:

A healthy network (green nodes)
A malicious agent appears (red node)
Infection begins spreading
ACP node intercepts propagation
Infected node is quarantined (gray)
Network stabilizes and recovers

This demonstrates:

Real-time containment of AI risk propagation.

10. Roadmap
Phase 1
Execution tracking
Basic scoring
Phase 2
Propagation graph
Visualization layer
Phase 3 (Current)
Credit propagation model
Containment mechanisms
Phase 4
Token-based incentives
On-chain reputation
Cross-platform integration
11. Conclusion

ACP transforms AI systems from isolated tools into an interconnected trust network.

By introducing propagation-aware credit and real-time containment, ACP enables:

Accountability across agent chains
Incentivized reliability
System-wide resilience

ACP is not just a scoring system —
it is a foundational trust protocol for autonomous AI ecosystems.