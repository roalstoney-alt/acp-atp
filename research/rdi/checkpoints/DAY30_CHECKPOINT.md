# Day 30 Checkpoint

## Files Created And Modified

Created: RDI governance, Case Study 001, Boundary Challenge, crosswalks, reproduction guide, adapter package, outreach drafts, release drafts, and monthly report.

Modified: PATL runtime, schemas, fixtures, demo runner, tests, and project metadata.

## Test Results

- `python3 -B -m unittest discover -s tests`: 34 tests passed.
- `python3 -B -m challenge.run_boundary_challenge`: 15 passed, 0 failed.
- `python3 -B -m integrations.selected_framework.demo`: expected decision sequence observed.

## Newly Verified Claims

- PATL v0.1.1 closes the local confirmation-binding and evidence-chain defects covered by tests.
- The challenge is locally reproducible.
- The adapter demonstrates a pre-tool authorization boundary.

## Failed Claims

- Git commit could not be recorded.
- Independent reproduction has not occurred.
- Dependency-backed framework integration has not occurred.
- No outreach has been sent.

## EML Changes

See `research/rdi/EML_LEDGER.csv`.

## Known P0/P1 Risks

P0: none open in local test scope.

P1: no cryptographic attestation, no durable revocation registry, no external evidence log, no dependency-backed framework integration, no independent reproduction.

## Negative Results

See `research/rdi/NEGATIVE_RESULTS.md`.

## Next Gate Status

G8: PASS draft.

G9: PASS report, with external evidence still insufficient.
