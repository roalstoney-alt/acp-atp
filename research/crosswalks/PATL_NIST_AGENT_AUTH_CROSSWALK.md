# PATL x NIST Agent Identity and Authorization Crosswalk

Sources:

- NIST NCCoE concept paper announcement, "Accelerating the Adoption of Software and Artificial Intelligence Agent Identity and Authorization": https://www.nist.gov/news-events/news/2026/02/new-concept-paper-identity-and-authority-software-agents
- NIST AI Agent Standards Initiative: https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative

No endorsement or compliance is claimed.

| Topic | Status | PATL alignment | Gap |
|---|---|---|---|
| Principal identity | PARTIAL_ALIGNMENT | PAAC records a pseudonymous individual principal. | No enterprise identity federation. |
| Agent identity | PARTIAL_ALIGNMENT | PAAC records agent id and version. | No cryptographic proof of agent runtime identity. |
| Model identity | PATL_EXTENSION | Runtime checks declared model id. | Model provenance and attestation are not implemented. |
| Tool authorization | DIRECT_ALIGNMENT | Runtime checks declared tool id and permitted action. | Tool registration is local. |
| Delegated authority | PARTIAL_ALIGNMENT | Undeclared delegated sub-agent id is blocked. | No chained delegation credential format. |
| Revocation | DIRECT_ALIGNMENT | Contract and agent revocation registry blocks execution. | Registry is in-memory in v0.1.1. |
| Auditing | PARTIAL_ALIGNMENT | Hash-chained evidence ledger records decisions. | No non-repudiation, signature, or external log. |
| Lifecycle | REQUIRES_REVIEW | Validity windows and execution budget exist. | No provisioning, renewal, or retirement workflow. |

Concrete contribution PATL could offer: test fixtures for method-level authorization failures in AI agent identity projects.
