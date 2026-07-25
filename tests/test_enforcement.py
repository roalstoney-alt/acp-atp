import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone

from trust_layer.core import EnforcementEngine
from trust_layer.evidence import EvidenceLedger, request_digest
from trust_layer.fixtures import alpha_contracts
from trust_layer.loader import load_contracts_from_json
from trust_layer.models import ActionRequest, ConfirmationRecord, RevocationRegistry


NOW = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)


def req(
    request_id="req_1",
    contract_id="paac_email_demo",
    agent_id="email-agent.mock",
    action_type="email.draft",
    resource="mailbox",
    params=None,
    metadata=None,
    created_at=NOW,
):
    return ActionRequest(
        request_id=request_id,
        contract_id=contract_id,
        agent_id=agent_id,
        action_type=action_type,
        resource=resource,
        params=params or {"recipients": ["alice@example.com"], "content_hash": "sha256:x"},
        created_at=created_at,
        metadata=metadata
        or {
            "agent_version": "0.1",
            "model_id": "model.mock.safe",
            "tool_id": f"{action_type.split('.')[0]}.mock",
        },
    )


def confirmation_for(request, nonce="nonce-1", confirmed_at=NOW, expires_at=None):
    return ConfirmationRecord(
        request_id=request.request_id,
        contract_id=request.contract_id,
        request_digest=request_digest(request),
        nonce=nonce,
        confirmed=True,
        confirmed_by="user",
        confirmed_at=confirmed_at,
        expires_at=expires_at or confirmed_at + timedelta(minutes=5),
    )


class EnforcementTests(unittest.TestCase):
    def setUp(self):
        self.contracts = alpha_contracts()

    def test_allow_with_log_for_scoped_email_draft(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(req())
        self.assertEqual(result["decision"], "ALLOW_WITH_LOG")

    def test_send_requires_confirmation(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(req(action_type="email.send"))
        self.assertEqual(result["decision"], "REQUIRE_CONFIRMATION")

    def test_confirmed_send_allows_with_log(self):
        request = req(action_type="email.send", metadata={
            "agent_version": "0.1",
            "model_id": "model.mock.safe",
            "tool_id": "email.mock",
            "confirmation_nonce": "nonce-1",
        })
        confirmations = {
            "req_1": confirmation_for(request)
        }
        result = EnforcementEngine(self.contracts, confirmations=confirmations, now=NOW).evaluate(request)
        self.assertEqual(result["decision"], "ALLOW_WITH_LOG")

    def test_confirmation_round_trip_does_not_consume_request(self):
        request = req(action_type="email.send")
        engine = EnforcementEngine(self.contracts, now=NOW)
        first = engine.evaluate(request)
        self.assertEqual(first["decision"], "REQUIRE_CONFIRMATION")
        confirmed = replace(request, metadata={**request.metadata, "confirmation_nonce": "nonce-1"})
        engine.confirmations[request.request_id] = confirmation_for(confirmed)
        second = engine.evaluate(confirmed)
        self.assertEqual(second["decision"], "ALLOW_WITH_LOG")

    def test_changed_recipient_after_confirmation_blocks(self):
        confirmed = req(action_type="email.send", metadata={
            "agent_version": "0.1",
            "model_id": "model.mock.safe",
            "tool_id": "email.mock",
            "confirmation_nonce": "nonce-1",
        })
        changed = replace(confirmed, params={"recipients": ["mallory@example.com"], "content_hash": "sha256:x"})
        confirmations = {"req_1": confirmation_for(confirmed)}
        result = EnforcementEngine(self.contracts, confirmations=confirmations, now=NOW).evaluate(changed)
        self.assertEqual(result["decision"], "REQUIRE_CONFIRMATION")

    def test_changed_payment_amount_after_confirmation_blocks(self):
        confirmed = req(
            contract_id="paac_travel_demo",
            agent_id="travel-agent.mock",
            action_type="travel.purchase",
            resource="travel_api",
            params={"amount": 400, "currency": "USD"},
            metadata={"agent_version": "0.1", "model_id": "model.mock.safe", "tool_id": "travel.mock", "confirmation_nonce": "nonce-1"},
        )
        changed = replace(confirmed, params={"amount": 450, "currency": "USD"})
        confirmations = {"req_1": confirmation_for(confirmed)}
        result = EnforcementEngine(self.contracts, confirmations=confirmations, now=NOW).evaluate(changed)
        self.assertEqual(result["decision"], "REQUIRE_CONFIRMATION")

    def test_changed_currency_after_confirmation_blocks(self):
        confirmed = req(
            contract_id="paac_travel_demo",
            agent_id="travel-agent.mock",
            action_type="travel.purchase",
            resource="travel_api",
            params={"amount": 400, "currency": "USD"},
            metadata={"agent_version": "0.1", "model_id": "model.mock.safe", "tool_id": "travel.mock", "confirmation_nonce": "nonce-1"},
        )
        changed = replace(confirmed, params={"amount": 400, "currency": "CAD"})
        confirmations = {"req_1": confirmation_for(confirmed)}
        result = EnforcementEngine(self.contracts, confirmations=confirmations, now=NOW).evaluate(changed)
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("currency_mismatch", result["violations"])

    def test_changed_resource_after_confirmation_requires_new_confirmation(self):
        confirmed = req(action_type="email.send", resource="mailbox", metadata={
            "agent_version": "0.1",
            "model_id": "model.mock.safe",
            "tool_id": "email.mock",
            "confirmation_nonce": "nonce-1",
        })
        changed = replace(confirmed, resource="other_mailbox")
        confirmations = {"req_1": confirmation_for(confirmed)}
        result = EnforcementEngine(self.contracts, confirmations=confirmations, now=NOW).evaluate(changed)
        self.assertEqual(result["decision"], "REQUIRE_CONFIRMATION")

    def test_expired_confirmation_requires_new_confirmation(self):
        request = req(action_type="email.send", metadata={
            "agent_version": "0.1",
            "model_id": "model.mock.safe",
            "tool_id": "email.mock",
            "confirmation_nonce": "nonce-1",
        })
        confirmations = {"req_1": confirmation_for(request, expires_at=NOW - timedelta(seconds=1))}
        result = EnforcementEngine(self.contracts, confirmations=confirmations, now=NOW).evaluate(request)
        self.assertEqual(result["decision"], "REQUIRE_CONFIRMATION")

    def test_blocks_unapproved_email_domain(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(
            req(params={"recipients": ["eve@attacker.test"]})
        )
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("unexpected_recipient", result["violations"])

    def test_blocks_payment_above_limit(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(
            req(
                contract_id="paac_travel_demo",
                agent_id="travel-agent.mock",
                action_type="travel.purchase",
                resource="travel_api",
                params={"amount": 501, "currency": "USD"},
            )
        )
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("payment_limit_exceeded", result["violations"])

    def test_travel_purchase_under_limit_requires_confirmation(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(
            req(
                contract_id="paac_travel_demo",
                agent_id="travel-agent.mock",
                action_type="travel.purchase",
                resource="travel_api",
                params={"amount": 400, "currency": "USD"},
            )
        )
        self.assertEqual(result["decision"], "REQUIRE_CONFIRMATION")

    def test_blocks_file_delete(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(
            req(
                contract_id="paac_file_demo",
                agent_id="file-agent.mock",
                action_type="file.delete",
                resource="/workspace/demo/a.txt",
                params={"path": "/workspace/demo/a.txt"},
            )
        )
        self.assertEqual(result["decision"], "BLOCK")

    def test_blocks_file_upload(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(
            req(
                contract_id="paac_file_demo",
                agent_id="file-agent.mock",
                action_type="file.upload",
                resource="/workspace/demo/a.txt",
                params={"path": "/workspace/demo/a.txt"},
            )
        )
        self.assertEqual(result["decision"], "BLOCK")

    def test_blocks_path_escape(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(
            req(
                contract_id="paac_file_demo",
                agent_id="file-agent.mock",
                action_type="file.rename",
                resource="/etc/passwd",
                params={"path": "/etc/passwd"},
            )
        )
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("path_scope_violation", result["violations"])

    def test_blocks_expired_contract(self):
        result = EnforcementEngine(self.contracts, now=NOW + timedelta(days=30)).evaluate(req())
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("expired_authorization", result["violations"])

    def test_blocks_revoked_contract(self):
        reg = RevocationRegistry()
        reg.revoke_contract("paac_email_demo")
        result = EnforcementEngine(self.contracts, revocations=reg, now=NOW).evaluate(req())
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("revocation_bypass_attempt", result["violations"])

    def test_blocks_agent_mismatch(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(req(agent_id="other-agent"))
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("agent_mismatch", result["violations"])

    def test_blocks_unknown_contract(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(req(contract_id="missing_contract"))
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("missing_authorization", result["violations"])

    def test_blocks_replay(self):
        engine = EnforcementEngine(self.contracts, now=NOW)
        first = engine.evaluate(req())
        second = engine.evaluate(req())
        self.assertEqual(first["decision"], "ALLOW_WITH_LOG")
        self.assertEqual(second["decision"], "BLOCK")
        self.assertIn("replay", second["violations"])

    def test_blocks_agent_version_mismatch(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(
            req(metadata={"agent_version": "0.2", "model_id": "model.mock.safe", "tool_id": "email.mock"})
        )
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("agent_version_mismatch", result["violations"])

    def test_blocks_model_mismatch(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(
            req(metadata={"agent_version": "0.1", "model_id": "model.mock.other", "tool_id": "email.mock"})
        )
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("model_mismatch", result["violations"])

    def test_blocks_undeclared_tool(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(
            req(metadata={"agent_version": "0.1", "model_id": "model.mock.safe", "tool_id": "shell.mock"})
        )
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("undeclared_tool", result["violations"])

    def test_blocks_undeclared_sub_agent(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(
            req(metadata={
                "agent_version": "0.1",
                "model_id": "model.mock.safe",
                "tool_id": "email.mock",
                "delegated_agent_id": "other-agent.mock",
            })
        )
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("undeclared_delegation", result["violations"])

    def test_blocks_execution_count_exhaustion(self):
        self.contracts["paac_email_demo"].constraints["max_execution_count"] = 1
        engine = EnforcementEngine(self.contracts, now=NOW)
        first = engine.evaluate(req(request_id="req_1"))
        second = engine.evaluate(req(request_id="req_2"))
        self.assertEqual(first["decision"], "ALLOW_WITH_LOG")
        self.assertEqual(second["decision"], "BLOCK")
        self.assertIn("execution_budget_exhausted", second["violations"])

    def test_evidence_mutation_breaks_integrity(self):
        ledger = EvidenceLedger()
        engine = EnforcementEngine(self.contracts, ledger=ledger, now=NOW)
        engine.evaluate(req(request_id="req_1"))
        engine.evaluate(req(request_id="req_2"))
        self.assertTrue(ledger.verify_integrity())
        ledger.events[0]["decision"] = "ALLOW"
        self.assertFalse(ledger.verify_integrity())

    def test_invalid_paac_input_rejected_by_schema_loader(self):
        bad_contract = {
            "paac_version": "0.1",
            "contract_id": "bad",
            "principal": {"type": "individual", "pseudonymous_id": "user_local_001"},
            "agent_stack": {"agent_id": "email-agent.mock", "agent_version": "0.1", "model_id": "model.mock.safe"},
            "purpose": "Missing actions.",
            "permitted_actions": ["email.draft"],
            "prohibited_actions": [],
            "resources": {},
            "constraints": {},
            "validity": {"valid_from": "2026-07-21T00:00:00Z", "valid_until": "2026-07-28T00:00:00Z"},
        }
        with self.assertRaises(ValueError):
            load_contracts_from_json([bad_contract])

    def test_runtime_clock_advances_per_request_when_no_fixed_now(self):
        engine = EnforcementEngine(self.contracts)
        active = engine.evaluate(req(request_id="req_1", created_at=NOW))
        expired = engine.evaluate(req(request_id="req_2", created_at=NOW + timedelta(days=30)))
        self.assertEqual(active["decision"], "ALLOW_WITH_LOG")
        self.assertEqual(expired["decision"], "BLOCK")
        self.assertIn("expired_authorization", expired["violations"])

    def test_every_decision_generates_evidence_and_credit_event(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(req())
        self.assertTrue(result["evidence"]["event_id"].startswith("ev_"))
        self.assertTrue(result["agent_credit_event"]["event_id"].startswith("ace_"))
        self.assertEqual(result["agent_credit_event"]["source_evidence_id"], result["evidence"]["event_id"])


if __name__ == "__main__":
    unittest.main()
