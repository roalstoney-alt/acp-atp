# Changelog

## v0.1.1-alpha - 2026-07-21

- Replaced simple replay handling with explicit request lifecycle state.
- Ensured `REQUIRE_CONFIRMATION` does not consume requests or execution allowance.
- Bound confirmations to canonical request digests including agent stack and full parameters.
- Added confirmation `issued_at`, `expires_at`, `nonce`, `request_digest` and simulated signature support.
- Added canonical PAAC JSON loader with Draft 2020-12 JSON Schema and semantic validation.
- Aligned PAAC schema, dataclasses and spec around agent stack, declared tools, max executions, delegation, validity and revocation.
- Added injectable per-request clock.
- Added agent version, model, undeclared tool and undeclared delegation blocking.
- Upgraded evidence ledger to an in-memory hash chain with integrity verification.
- Added adversarial tests for confirmation substitution, replay after consumption, execution caps and evidence mutation.

## v0.1-alpha - 2026-07-21

- Created PATL alpha project.
- Added PAAC v0.1, evidence and Agent credit schemas.
- Added deterministic enforcement implementation.
- Added synthetic email, travel and file demos.
- Added tests for confirmation, blocking, expiry, revocation, replay and evidence.
- Added audit, gap matrix, security docs, roadmap, launch content and FAQ.
