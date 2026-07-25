# Integration Conformance

Minimum adapter checks:

- Protected tool call is evaluated by PATL before execution.
- `BLOCK` never executes the tool.
- `REQUIRE_CONFIRMATION` pauses and does not consume the request.
- Exact confirmed request can execute once.
- Changed parameters after confirmation do not execute.
- Revocation blocks later execution.
- Undeclared tool id is blocked.
- Evidence ledger integrity verifies after decisions.
