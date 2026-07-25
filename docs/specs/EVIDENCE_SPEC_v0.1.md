# Evidence Event Specification v0.1

PATL evidence events record enforcement decisions without storing raw private content by default.

## Required Properties

- `event_version`
- `event_type`
- `event_id`
- `request_id`
- `contract_id`
- `agent_id`
- `action_type`
- `resource`
- `decision`
- `reasons`
- `violations`
- `policy_version`
- `created_at`
- `content_ref`

## Privacy Boundary

`content_ref` should be a hash or pointer. Raw message bodies, passwords, full screen captures and unrelated personal data must not enter the default evidence event.

## Implemented

The reference implementation creates deterministic hash-derived event IDs, stores events in a local in-memory ledger, links each event to the previous event hash, and verifies local chain integrity.

## Proposed

Future versions should support signatures, external transparency logs, durable storage and selective disclosure proofs.
