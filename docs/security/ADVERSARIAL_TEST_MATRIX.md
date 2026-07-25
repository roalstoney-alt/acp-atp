# Adversarial Test Matrix

| Attack Case | Expected Decision | Implemented Test |
| --- | --- | --- |
| Unknown contract | `BLOCK` | `test_blocks_unknown_contract` |
| Agent identity mismatch | `BLOCK` | `test_blocks_agent_mismatch` |
| Expired contract | `BLOCK` | `test_blocks_expired_contract` |
| Revoked contract | `BLOCK` | `test_blocks_revoked_contract` |
| Replay same request | `BLOCK` | `test_blocks_replay` |
| Email to unapproved domain | `BLOCK` | `test_blocks_unapproved_email_domain` |
| Email send without confirmation | `REQUIRE_CONFIRMATION` | `test_send_requires_confirmation` |
| Payment above limit | `BLOCK` | `test_blocks_payment_above_limit` |
| Payment under limit without confirmation | `REQUIRE_CONFIRMATION` | `test_travel_purchase_under_limit_requires_confirmation` |
| File delete | `BLOCK` | `test_blocks_file_delete` |
| File upload | `BLOCK` | `test_blocks_file_upload` |
| File path escape | `BLOCK` | `test_blocks_path_escape` |
| Evidence missing | fail test | `test_every_decision_generates_evidence_and_credit_event` |
