# Design Decisions

## 2026-07-21: Integrate Trust Layer Into Existing ACP-ATP Repo

The existing ACP-ATP GitHub repo already contains site, whitepaper and demo assets. The Personal Agent Trust Layer is integrated as a module under `trust_layer/` instead of replacing the ACP-ATP project.

## 2026-07-21: Use Modular Python

The user requested a modular Python reference implementation unless the existing codebase strongly supported another stack. No PATL codebase existed, so Python was selected.

## 2026-07-21: No Real Connectors

Email, travel and file demos use synthetic request objects and mock contracts. This follows the requirement not to connect to real email, payment or personal accounts.

## 2026-07-21: Deterministic Critical Controls

Critical controls are implemented in `PolicyEvaluator` and `EnforcementEngine`, not delegated to model judgment.

## 2026-07-21: Evidence Before Credit

Agent credit events are derived from evidence events so credit cannot become an independent permission source.
