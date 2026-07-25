# PATL External Reproduction Guide

Target time: 30 minutes for an unfamiliar developer.

## Requirements

- Python 3.11 or newer.
- `jsonschema` Python package.
- No network access is required for tests, demos, or the challenge.
- No real accounts, credentials, payments, or personal files are used.

## Steps

1. Run tests:

```bash
python3 -B -m unittest discover -s tests
```

Expected: all tests pass.

2. Run the PATL demo:

```bash
python3 -B -m trust_layer.demo_runner
```

Expected decisions include `ALLOW`, `ALLOW_WITH_LOG`, `REQUIRE_CONFIRMATION`, and `BLOCK`.

3. Run Boundary Challenge 001:

```bash
python3 -B -m challenge.run_boundary_challenge
```

Expected: `passed` is `15` and `failed` is `0`.

4. Run the adapter demo:

```bash
python3 -B -m integrations.selected_framework.demo
```

Expected: allow, confirmation pause, confirmed allow, revocation block, undeclared-tool block, and `evidence_integrity: true`.

## Status Labels

- NOT_ATTEMPTED
- STARTED
- BLOCKED_ENVIRONMENT
- BLOCKED_DOCUMENTATION
- PARTIAL_REPRODUCTION
- FULL_REPRODUCTION
- RESULT_MISMATCH

## Reviewer Checklist

- Tests ran without local code changes.
- Boundary Challenge result file was generated.
- Evidence integrity verification was observed.
- Any undocumented step was recorded.
- Any mismatch was preserved as a negative result.
