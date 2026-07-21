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
- Agent tries replaying a previously allowed request.
- Agent tries to send to a new recipient.
- Agent tries to exceed payment limits.
- Agent tries to delete or upload scoped files.
- Agent continues after revocation.
- Agent swaps identity or version.

## Implemented Controls

- Contract lookup and agent identity match.
- Action allowlist and denylist.
- Expiry checks.
- Revocation checks.
- Replay detection.
- Email recipient domain checks.
- Travel payment limit and currency checks.
- File path scope checks.
- Deterministic confirmation requirement.
- Evidence and Agent credit event generation.

## Simulated Controls

- User confirmation.
- Agent identity attestation.
- Local authority vault.

## Proposed Controls

- Hardware-backed keys.
- Signed PAAC bundles.
- Signed evidence logs.
- Independent audit network.
- OS-level tool interception.

## Unresolved Risks

- In-memory replay protection is not durable across process restart.
- Agent identity is declared, not cryptographically attested.
- File path checks are POSIX-style and do not cover symlink races or platform-specific path behavior.
- No real connector sandbox exists in alpha.
- No protection against malicious host process tampering.
