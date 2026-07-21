# Threat Model and Security Boundaries

## Protected Assets

- User root authority.
- Personal account access.
- Private content.
- Payment authority.
- File integrity and confidentiality.
- Enforcement evidence integrity.

## Attacker Models

- Agent exceeds task scope.
- Prompt injection asks agent to ignore contract.
- Agent replays a consumed request.
- Agent swaps parameters after user confirmation.
- Agent changes model, version, tools or delegation path.
- Agent sends email to a new recipient domain.
- Agent exceeds payment limits.
- Agent deletes or uploads scoped files.
- Agent continues after expiry or revocation.
- Host process tampers with in-memory evidence.

## Implemented

- Contract lookup and agent stack match: `agent_id`, `agent_version`, `model_id` and declared tools.
- Delegation blocking when `delegation_policy` is `none`.
- Action allowlist and denylist.
- Per-request clock evaluation for expiry.
- Revocation checks.
- Explicit request lifecycle: `PENDING`, `AWAITING_CONFIRMATION`, `AUTHORIZED`, `EXECUTED`, `CONSUMED`, `BLOCKED`, `EXPIRED`, `REVOKED`.
- `REQUIRE_CONFIRMATION` does not consume the request.
- Confirmation digest binding over contract, request, agent stack, action, resource and complete parameters.
- Confirmation expiry checks.
- Maximum execution checks.
- Email recipient domain checks.
- Travel payment limit and currency checks.
- File path scope checks for synthetic POSIX paths.
- Evidence and Agent credit event generation.
- Minimal in-memory hash-chained evidence ledger with `verify_integrity()`.
- Automated adversarial tests for replay, substitution, version/model/tool/delegation mismatch and ledger mutation.

## Simulated

- User confirmation signatures.
- Agent identity attestation.
- Local authority vault.
- Email, travel, payment and file service execution.

## Proposed

- Hardware-backed or OS-backed signing keys.
- Signed PAAC bundles.
- Signed evidence logs or append-only transparency service.
- OS-level tool interception.
- Durable replay and revocation store.
- Connector-level sandboxing.

## Unresolved

- P0: Agent identity is declared, not cryptographically attested.
- P0: The reference ledger and lifecycle state are in-memory and can be lost or modified by a malicious host process.
- P1: Replay protection is not durable across process restart.
- P1: File path checks do not address symlink races, mount aliases or platform-specific path normalization.
- P1: No real connector sandbox exists in alpha.
