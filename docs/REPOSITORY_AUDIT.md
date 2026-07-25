# Repository Audit

Date: 2026-07-21

## Scope Inspected

- GitHub repo: `https://github.com/roalstoney-alt/acp-atp`
- Local clone used for integration: canonical Git checkout.
- Existing local static copies inspected: local ACP-ATP static archives.
- Source document: local PATL source document archive.
- Existing code: `agent.py`, `main.py`, `scoring.py`, `sandbox.py`, `registry.py`, `no_protection.py`
- Existing site assets: `index.html`, `graph_demo.html`, `demo.mp4`, `demo2.mp4`

## Current State Findings

- The existing ACP-ATP repo already contained a public site, whitepaper material, videos, and a minimal trust-scoring/sandbox demo.
- The repo did not yet contain PAAC schemas, personal-agent authorization enforcement, evidence event schemas, Agent credit event schemas, or tests for email/travel/file authorization scenarios.
- The ACP-ATP PATL `.docx` is the seed artifact for the personal-agent trust layer. It contains 740 extracted paragraphs with mission, principles, architecture, PAAC outline, gateway decisions, evidence layer, threat model and roadmap.
- The existing ACP-ATP site should be preserved and extended, not replaced.

## Material Risks Found

- The saved `.docx` is not directly testable or machine-readable as a spec.
- Local static folders outside the GitHub clone are not git repositories.
- Before this integration, the GitHub repo had no automated tests for the new personal-agent authorization security claims.
- Existing sandbox demo is educational and not production isolation.

## Preservation Actions

- Existing ACP-ATP files were preserved.
- Personal-agent trust layer was added under `trust_layer/`, `schemas/`, `docs/`, `tests/`, and `demos/`.
- Existing landing page was extended with an on-site trust-layer demo.
- Negative implementation status is explicit: the Personal Agent Trust Layer v0.1 alpha is not production-ready.
