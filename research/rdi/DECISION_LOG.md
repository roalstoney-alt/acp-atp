# RDI Decision Log

## D-0001 - Record missing Git commit instead of inventing one

Fact: `git rev-parse HEAD` failed because the completed local sprint source is not a Git repository.

Decision: `BASELINE_FREEZE.json` records `git_commit: null` and the exact reason.

Reason changed: none. This preserves evidence integrity.

## D-0002 - Make stack identity mandatory in runtime requests

Fact: Baseline contracts had `agent_version`, but enforcement accepted requests without version, model, or tool identity checks.

Decision: Requests must match `agent_version`, `model_id`, and a declared `tool_id`.

Reason changed: Phase 2 requires Agent/model/tool/version checks.

## D-0003 - Do not consume confirmation-pending requests

Fact: Baseline replay detection consumed a request before a confirmed retry could execute.

Decision: Consume request ids and digests only after an executable ALLOW or ALLOW_WITH_LOG decision.

Reason changed: Phase 2 requires a correct confirmation lifecycle.

## D-0004 - Treat adapter as boundary compatibility, not independent integration

Fact: No common agent framework packages were installed locally and network access is restricted.

Decision: Implement an isolated LangChain-style tool-boundary adapter and label the limitation.

Reason changed: Avoid overstating Phase 6 evidence.
