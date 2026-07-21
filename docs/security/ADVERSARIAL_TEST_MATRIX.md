# Adversarial Test Matrix

| Attack Case | Expected Decision | Implemented Test |
| --- | --- | --- |
| Unknown contract | `BLOCK` | `test_blocks_unknown_contract` |
| Agent identity mismatch | `BLOCK` | `test_blocks_agent_mismatch` |
| Agent version mismatch | `BLOCK` | `test_blocks_agent_version_mismatch` |
| Model mismatch | `BLOCK` | `test_blocks_model_mismatch` |
| Undeclared tool | `BLOCK` | `test_blocks_undeclared_tools` |
| Undeclared delegation | `BLOCK` | `test_blocks_undeclared_delegation` |
| Expired contract via injected clock | `BLOCK` | `test_blocks_expired_contract_with_injected_clock` |
| Revoked contract | `BLOCK` | `test_blocks_revoked_contract` |
| Replay consumed request | `BLOCK` | `test_blocks_replay_after_consumption` |
| Maximum executions exceeded | `BLOCK` | `test_blocks_maximum_executions_exceeded` |
| Email to unapproved domain | `BLOCK` | `test_blocks_unapproved_email_domain` |
| Email send without confirmation | `REQUIRE_CONFIRMATION` | `test_require_confirmation_does_not_consume_request` |
| Confirmation parameter substitution | `BLOCK` | `test_rejects_parameter_substitution_after_confirmation` |
| Pending request parameter substitution | `BLOCK` | `test_rejects_pending_request_parameter_substitution` |
| Expired confirmation | `REQUIRE_CONFIRMATION` | `test_expired_confirmation_does_not_consume_request` |
| Denied confirmation | `BLOCK` | `test_confirmation_denial_blocks` |
| Payment above limit | `BLOCK` | `test_blocks_payment_above_limit` |
| Payment under limit without confirmation | `REQUIRE_CONFIRMATION` | `test_travel_purchase_under_limit_requires_confirmation` |
| File delete | `BLOCK` | `test_blocks_file_delete` |
| File upload | `BLOCK` | `test_blocks_file_upload` |
| File path escape | `BLOCK` | `test_blocks_path_escape` |
| Evidence missing | fail test | `test_every_decision_generates_evidence_and_credit_event` |
| Evidence mutation | integrity failure | `test_evidence_ledger_detects_mutation` |
| PAAC schema violation | validation failure | `test_paac_invalid_fixture_fails_draft_2020_12_schema` |
| PAAC semantic violation | validation failure | `test_loader_rejects_semantically_invalid_contract` |
