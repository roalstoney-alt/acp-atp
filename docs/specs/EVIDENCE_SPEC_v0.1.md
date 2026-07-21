# Evidence Event Specification v0.1

PATL evidence events record enforcement decisions without storing raw private content by default. v0.1.1 adds lifecycle and request-digest fields while keeping the schema filename stable.

## Required Properties

- `event_version`: `patl-evidence-v0.1.1`.
- `event_type`: `patl.enforcement_decision`.
- `event_id`
- `request_id`
- `request_digest`
- `contract_id`
- `agent_stack`
- `agent_id`
- `action_type`
- `resource`
- `decision`
- `lifecycle_status`
- `lifecycle_transitions`
- `reasons`
- `violations`
- `policy_version`
- `created_at`
- `content_ref`

## Ledger Record

The reference `EvidenceLedger` stores each event in a minimal hash chain:

- `ledger_id`
- `sequence`
- `previous_event_hash`
- `event`
- `event_hash`
- `recorded_at`

`verify_integrity()` recomputes each event hash and previous hash pointer. Mutation of a stored event is detected by the automated test suite.

## Privacy Boundary

`content_ref` should be a hash or pointer. Raw message bodies, passwords, full screen captures and unrelated personal data must not enter the default evidence event.

## Implemented

- Deterministic hash-derived event IDs.
- Request digest bound to contract, request, agent stack, action, resource and parameters.
- In-memory hash-chained ledger with mutation detection.

## Simulated

- Confirmation signatures are represented as simulated strings.
- Service execution is simulated by the local enforcement result.

## Proposed

- Real local signing keys.
- Transparency logs.
- Selective disclosure proofs.

## Unresolved

- The alpha ledger is in-memory and not durable across process restarts.
- The host process can mutate memory; no tamper-resistant storage is implemented.
