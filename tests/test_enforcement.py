import unittest
from datetime import datetime, timedelta, timezone

from trust_layer.core import EnforcementEngine
from trust_layer.fixtures import alpha_contracts
from trust_layer.models import ActionRequest, ConfirmationRecord, RevocationRegistry


NOW = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)


def req(
    request_id="req_1",
    contract_id="paac_email_demo",
    agent_id="email-agent.mock",
    action_type="email.draft",
    resource="mailbox",
    params=None,
):
    return ActionRequest(
        request_id=request_id,
        contract_id=contract_id,
        agent_id=agent_id,
        action_type=action_type,
        resource=resource,
        params=params or {"recipients": ["alice@example.com"], "content_hash": "sha256:x"},
        created_at=NOW,
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
        confirmations = {
            "req_1": ConfirmationRecord("req_1", "paac_email_demo", True, "user", NOW)
        }
        result = EnforcementEngine(self.contracts, confirmations=confirmations, now=NOW).evaluate(
            req(action_type="email.send")
        )
        self.assertEqual(result["decision"], "ALLOW_WITH_LOG")

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

    def test_every_decision_generates_evidence_and_credit_event(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(req())
        self.assertTrue(result["evidence"]["event_id"].startswith("ev_"))
        self.assertTrue(result["agent_credit_event"]["event_id"].startswith("ace_"))
        self.assertEqual(result["agent_credit_event"]["source_evidence_id"], result["evidence"]["event_id"])


if __name__ == "__main__":
    unittest.main()
