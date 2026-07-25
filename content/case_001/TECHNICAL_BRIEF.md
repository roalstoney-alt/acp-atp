# Six-Part Release Technical Brief

## 1. Incident Reality

Link: `research/cases/PATL_CASE_001_OPENAI_HUGGINGFACE/CASE_REPORT.md`

Claim boundary: public-source case analysis only.

## 2. Goal Versus Method Principle

Core proposition: a delegated goal needs explicit method authorization.

Evidence: Boundary Challenge BC-002 through BC-007.

## 3. PAAC Mechanism

Code: `trust_layer/models.py`, `trust_layer/core.py`, `trust_layer/loader.py`

Tests: `tests/test_enforcement.py`

## 4. Boundary Challenge

Code: `challenge/run_boundary_challenge.py`

Evidence: `challenge/BASELINE_RESULTS.json`

## 5. External Integration

Code: `integrations/selected_framework/adapter.py`

Limitation: framework-shaped adapter only; no installed external framework dependency.

## 6. Request For Criticism

Ask reviewers to reproduce one scenario, identify one unclear claim, or propose one stricter control.
