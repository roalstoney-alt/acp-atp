# PATL Foundational Paper v0.1

## Abstract

Personal AI agents are moving from advisory interfaces toward execution systems. They will send messages, search services, manage files, schedule travel and initiate transactions. This creates a gap between human intent and machine execution: agents can gain practical authority faster than users, platforms and auditors can constrain or revoke it.

The Personal Agent Trust Layer proposes an open authorization, enforcement and evidence layer between user intent, agent reasoning, application execution and independent review.

## Thesis

Delegation is not ownership. A user can authorize an agent to complete a task without granting broad control over accounts, devices, data or future actions.

## Design Commitments

- User-held root authority.
- Least authority by default.
- Deterministic controls for critical actions.
- Immediate revocation.
- Minimal evidence over surveillance.
- Agent-stack attribution.
- Portable trust records.

## Reference Architecture

1. Personal Authority Vault: holds root authority and signs bounded contracts. Simulated in v0.1.
2. PAAC Contract Engine: represents bounded task authority.
3. ATP Execution Gateway: returns `ALLOW`, `ALLOW_WITH_LOG`, `REQUIRE_CONFIRMATION` or `BLOCK`.
4. Evidence Layer: records decisions without raw private content by default.
5. Agent Credit Layer: derives behavioral credit events from evidence.
6. Audit Profile: verifies authorization, scope and revocation without unnecessary disclosure.

## Alpha Contribution

PATL v0.1 alpha implements the contract/gateway/evidence core locally with synthetic email, travel and file scenarios. It proves the control model can be reviewed and tested without connecting to real accounts.

## Non-Claims

PATL v0.1 alpha does not provide production key custody, real connector security, platform sandboxing, identity attestation, fraud prevention or legal dispute resolution.
