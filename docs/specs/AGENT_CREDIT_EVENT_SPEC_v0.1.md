# Agent Credit Event Specification v0.1

Agent credit events summarize enforcement outcomes for reputation and review. v0.1.1 adds lifecycle status to keep credit summaries aligned with authorization state.

## Required Properties

- `event_version`: `patl-agent-credit-v0.1.1`.
- `event_type`: `patl.agent_credit_event`.
- `event_id`
- `source_evidence_id`
- `agent_id`
- `contract_id`
- `action_type`
- `decision`
- `lifecycle_status`
- `violation_count`
- `created_at`

## Rule

Agent credit cannot override permission. Credit may be used later for routing, review priority or lower-friction confirmation, but the deterministic PAAC boundary remains authoritative.

## Implemented

- One Agent credit event is emitted per enforcement evidence event.
- Credit events inherit the enforcement decision and lifecycle status from evidence.

## Simulated

- No external reputation network is connected.

## Proposed

- Aggregated credit views and independent audit feeds.
