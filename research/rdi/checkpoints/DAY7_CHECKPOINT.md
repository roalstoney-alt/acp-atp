# Day 7 Checkpoint

## Files Created And Modified

Created: Case Study 001 files under `research/cases/PATL_CASE_001_OPENAI_HUGGINGFACE/`.

Modified: PATL runtime, schemas, tests.

## Test Results

`python3 -B -m unittest discover -s tests`: 34 tests passed.

## Newly Verified Claims

- Confirmation-pending requests are not consumed before exact confirmation.
- Changed recipient, changed amount, expired confirmation, undeclared tool, undeclared delegation, model mismatch, agent version mismatch, revocation, replay, and execution budget exhaustion are covered by tests.

## Failed Claims

- None newly failed.

## EML Changes

- Method-level enforcement moved from EML-2 to EML-3 for internal reproduction.
- Evidence-chain mutation detection moved to EML-3 internally.

## Known P0/P1 Risks

P0: no known open authorization-integrity P0 in local v0.1.1 tests.

P1: identity remains declared, not cryptographically attested.

## Negative Results

No external reviewer yet.

## Next Gate Status

G1: PASS draft.

G2: PASS internal.
