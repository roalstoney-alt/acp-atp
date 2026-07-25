# Agent Credit Event Specification v0.1

Agent credit events summarize enforcement outcomes for reputation and review.

## Required Properties

- `event_version`
- `event_type`
- `event_id`
- `source_evidence_id`
- `agent_id`
- `contract_id`
- `action_type`
- `decision`
- `violation_count`
- `created_at`

## Rule

Agent credit cannot override permission. Credit may be used later for routing, review priority or lower-friction confirmation, but the deterministic PAAC boundary remains authoritative.

## Implemented

The alpha implementation emits one Agent credit event per enforcement evidence event.
