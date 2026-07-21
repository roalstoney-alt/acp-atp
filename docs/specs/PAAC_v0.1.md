# PAAC v0.1 Specification

PAAC means Personal Agent Authorization Contract.

## Required Fields

- `paac_version`: must be `0.1`.
- `contract_id`: stable contract identifier.
- `principal`: user or delegated principal. v0.1 supports `individual`.
- `agent_stack`: declared agent, model and tool identity.
- `purpose`: human-readable bounded task.
- `permitted_actions`: allowed action verbs.
- `prohibited_actions`: explicit denials.
- `resources`: scoped accounts, paths, recipients or service categories.
- `constraints`: amount, currency, time, count or other limits.
- `validity`: `valid_from` and `valid_until`.
- `confirmation_required_actions`: actions requiring user confirmation.
- `revocation`: optional state.

## Decision Semantics

- `ALLOW`: in-scope low-risk action.
- `ALLOW_WITH_LOG`: in-scope action that must produce evidence.
- `REQUIRE_CONFIRMATION`: in-scope but requires deterministic user confirmation before execution.
- `BLOCK`: out-of-scope, expired, revoked, replayed or prohibited action.

## Compatibility

v0.1 is an alpha schema. Implementers should preserve unknown data outside enforcement-critical fields only if their own compatibility profile permits it. The reference schema currently rejects unknown top-level fields for reviewability.
