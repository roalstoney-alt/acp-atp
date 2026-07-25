# PATL x Cloud Security Alliance AI Controls Crosswalk

Sources:

- CSA AI Controls Matrix v1.1: https://cloudsecurityalliance.org/artifacts/ai-controls-matrix-v1-1
- CSA Agentic AI Autonomy Levels and Control Framework: https://labs.cloudsecurityalliance.org/research/agentic-ai-autonomy-levels-control-framework-v2-csa-styled/
- CSA Securing the Agentic Control Plane: https://labs.cloudsecurityalliance.org/agentic/

No endorsement or compliance is claimed.

| Control family | Status | PATL alignment | Gap |
|---|---|---|---|
| Preventive controls | PARTIAL_ALIGNMENT | PAAC prevents out-of-scope actions at the gateway. | Does not harden cloud infrastructure. |
| Detective controls | PARTIAL_ALIGNMENT | Evidence Chain records every enforcement decision. | No SIEM integration or alerting pipeline. |
| Authorization controls | DIRECT_ALIGNMENT | Contract, action, resource, tool, model, version, delegation, confirmation, revocation, and execution-count checks. | No cloud IAM binding. |
| Audit controls | PARTIAL_ALIGNMENT | Hash chain detects local event mutation. | No signed external audit store. |
| Governance controls | PARTIAL_ALIGNMENT | RDI ledgers track claims, maturity, decisions, and negative results. | No organizational approval workflow. |
| Autonomy-level control | PATL_EXTENSION | Confirmation-required actions create a deterministic pause. | No general autonomy taxonomy scoring. |
| Cloud shared responsibility | TERMINOLOGY_MISMATCH | PATL can sit at application or orchestration boundaries. | Control ownership needs CSA role mapping review. |

Concrete contribution PATL could offer: a reproducible evidence fixture showing authorization checks before agent tool execution.
