# PAAC v0.1 Specification

PAAC means Personal Agent Authorization Contract. v0.1.1 keeps the public schema version at `0.1` and tightens runtime interpretation for authorization integrity.

## Required Fields

- `paac_version`: must be `0.1`.
- `contract_id`: stable contract identifier.
- `principal`: individual principal with pseudonymous ID.
- `agent_stack`: `agent_id`, `agent_version`, `model_id` and declared `tool_ids`.
- `purpose`: human-readable bounded task.
- `permitted_actions`: allowed action verbs.
- `prohibited_actions`: explicit denials.
- `resources`: scoped accounts, paths, recipients or service categories.
- `constraints`: amount, currency, time, count or other limits.
- `validity`: `valid_from` and `valid_until`.
- `confirmation_required_actions`: permitted actions requiring user confirmation.
- `log_required_actions`: permitted actions that must produce evidence.
- `maximum_executions`: maximum successful executions under the contract.
- `delegation_policy`: `none` or `single_agent`.
- `revocation`: `revoked` and nullable `revoked_at`.

## Runtime Lifecycle

Every request is evaluated through an explicit lifecycle:

`PENDING -> AWAITING_CONFIRMATION -> AUTHORIZED -> EXECUTED -> CONSUMED`

Terminal block states are `BLOCKED`, `EXPIRED` and `REVOKED`.

`REQUIRE_CONFIRMATION` leaves the request in `AWAITING_CONFIRMATION` and does not increment `execution_count`. A request is consumed only after deterministic authorization and simulated execution.

## Confirmation Binding

A confirmation record binds to a canonical digest of:

- `contract_id`
- `request_id`
- agent stack
- `action_type`
- `resource`
- complete normalized parameters

Confirmation records include `issued_at`, `expires_at`, `nonce`, `request_digest` and an optional simulated signature. Any parameter, model, tool, agent or resource substitution changes the digest and is rejected.

## Decision Semantics

- `ALLOW`: in-scope low-risk action.
- `ALLOW_WITH_LOG`: in-scope action that must produce evidence.
- `REQUIRE_CONFIRMATION`: in-scope but requires deterministic user confirmation before execution.
- `BLOCK`: out-of-scope, expired, revoked, replayed, exceeded or prohibited action.

## Loader Semantics

The reference loader performs Draft 2020-12 JSON Schema validation, semantic validation and runtime `PAACContract` construction. It rejects action overlap, invalid validity windows, confirmation/log actions outside the allowlist and inconsistent revocation state.

## Compatibility

v0.1 is an alpha schema. The reference schema rejects unknown top-level fields for reviewability. Implementers may add compatibility profiles, but enforcement-critical fields must remain canonicalized before authorization.
