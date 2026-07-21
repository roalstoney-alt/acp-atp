import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone

from trust_layer.core import EnforcementEngine
from trust_layer.evidence import request_digest
from trust_layer.fixtures import alpha_contracts
from trust_layer.models import ActionRequest, ConfirmationRecord, RevocationRegistry


NOW = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)


def req(
    request_id="req_1",
    contract_id="paac_email_demo",
    action_type="email.draft",
    resource="mailbox",
    params=None,
    agent_stack=None,
):
    contracts = alpha_contracts()
    stack = agent_stack or contracts[contract_id].agent_stack
    return ActionRequest(
        request_id=request_id,
        contract_id=contract_id,
        agent_stack=stack,
        action_type=action_type,
        resource=resource,
        params=params or {"recipients": ["alice@example.com"], "content_hash": "sha256:x"},
        created_at=NOW,
    )


def confirmation(request, confirmed=True, issued_at=NOW, expires_at=None):
    return ConfirmationRecord(
        request_id=request.request_id,
        contract_id=request.contract_id,
        confirmed=confirmed,
        confirmed_by="user",
        confirmed_at=NOW,
        issued_at=issued_at,
        expires_at=expires_at or NOW + timedelta(minutes=5),
        nonce=f"nonce-{request.request_id}",
        request_digest=request_digest(request),
        signature="simulated:user-confirmation",
    )


class EnforcementTests(unittest.TestCase):
    def setUp(self):
        self.contracts = alpha_contracts()

    def test_allow_with_log_for_scoped_email_draft(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(req())
        self.assertEqual(result["decision"], "ALLOW_WITH_LOG")
        self.assertEqual(result["lifecycle_status"], "CONSUMED")
        self.assertEqual(result["lifecycle_transitions"], ["PENDING", "AUTHORIZED", "EXECUTED", "CONSUMED"])

    def test_require_confirmation_does_not_consume_request(self):
        request = req(action_type="email.send")
        confirmations = {}
        engine = EnforcementEngine(self.contracts, confirmations=confirmations, now=NOW)
        first = engine.evaluate(request)
        self.assertEqual(first["decision"], "REQUIRE_CONFIRMATION")
        self.assertEqual(first["lifecycle_status"], "AWAITING_CONFIRMATION")
        self.assertEqual(self.contracts["paac_email_demo"].execution_count, 0)

        confirmations[request.request_id] = confirmation(request)
        second = engine.evaluate(request)
        self.assertEqual(second["decision"], "ALLOW_WITH_LOG")
        self.assertEqual(second["lifecycle_status"], "CONSUMED")
        self.assertEqual(second["lifecycle_transitions"][0], "AWAITING_CONFIRMATION")
        self.assertEqual(self.contracts["paac_email_demo"].execution_count, 1)

    def test_confirmation_binds_complete_request_digest(self):
        request = req(action_type="email.send")
        confirmations = {request.request_id: confirmation(request)}
        result = EnforcementEngine(self.contracts, confirmations=confirmations, now=NOW).evaluate(request)
        self.assertEqual(result["decision"], "ALLOW_WITH_LOG")
        self.assertEqual(result["evidence"]["request_digest"], request_digest(request))

    def test_rejects_parameter_substitution_after_confirmation(self):
        original = req(action_type="email.send", params={"recipients": ["alice@example.com"], "content_hash": "sha256:x"})
        changed = req(action_type="email.send", params={"recipients": ["bob@example.com"], "content_hash": "sha256:x"})
        confirmations = {original.request_id: confirmation(original)}
        result = EnforcementEngine(self.contracts, confirmations=confirmations, now=NOW).evaluate(changed)
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("parameter_substitution", result["violations"])

    def test_rejects_pending_request_parameter_substitution(self):
        original = req(action_type="email.send", params={"recipients": ["alice@example.com"], "content_hash": "sha256:x"})
        changed = req(action_type="email.send", params={"recipients": ["bob@example.com"], "content_hash": "sha256:x"})
        engine = EnforcementEngine(self.contracts, now=NOW)
        first = engine.evaluate(original)
        second = engine.evaluate(changed)
        self.assertEqual(first["decision"], "REQUIRE_CONFIRMATION")
        self.assertEqual(second["decision"], "BLOCK")
        self.assertIn("parameter_substitution", second["violations"])

    def test_expired_confirmation_does_not_consume_request(self):
        request = req(action_type="email.send")
        confirmations = {request.request_id: confirmation(request, expires_at=NOW - timedelta(seconds=1))}
        result = EnforcementEngine(self.contracts, confirmations=confirmations, now=NOW).evaluate(request)
        self.assertEqual(result["decision"], "REQUIRE_CONFIRMATION")
        self.assertEqual(result["lifecycle_status"], "AWAITING_CONFIRMATION")
        self.assertEqual(self.contracts["paac_email_demo"].execution_count, 0)

    def test_confirmation_denial_blocks(self):
        request = req(action_type="email.send")
        confirmations = {request.request_id: confirmation(request, confirmed=False)}
        result = EnforcementEngine(self.contracts, confirmations=confirmations, now=NOW).evaluate(request)
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("invalid_confirmation", result["violations"])

    def test_blocks_unapproved_email_domain(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(
            req(params={"recipients": ["eve@attacker.test"]})
        )
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("unexpected_recipient", result["violations"])

    def test_blocks_payment_above_limit(self):
        request = req(
            contract_id="paac_travel_demo",
            action_type="travel.purchase",
            resource="travel_api",
            params={"amount": 501, "currency": "USD"},
        )
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(request)
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("payment_limit_exceeded", result["violations"])

    def test_travel_purchase_under_limit_requires_confirmation(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(
            req(
                contract_id="paac_travel_demo",
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
                action_type="file.rename",
                resource="/etc/passwd",
                params={"path": "/etc/passwd"},
            )
        )
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("path_scope_violation", result["violations"])

    def test_blocks_expired_contract_with_injected_clock(self):
        times = iter([NOW, NOW, NOW + timedelta(days=30), NOW + timedelta(days=30)])
        engine = EnforcementEngine(self.contracts, clock=lambda: next(times))
        first = engine.evaluate(req(request_id="req_clock_1"))
        second = engine.evaluate(req(request_id="req_clock_2"))
        self.assertEqual(first["decision"], "ALLOW_WITH_LOG")
        self.assertEqual(second["decision"], "BLOCK")
        self.assertEqual(second["lifecycle_status"], "EXPIRED")
        self.assertIn("expired_authorization", second["violations"])

    def test_blocks_revoked_contract(self):
        reg = RevocationRegistry()
        reg.revoke_contract("paac_email_demo")
        result = EnforcementEngine(self.contracts, revocations=reg, now=NOW).evaluate(req())
        self.assertEqual(result["decision"], "BLOCK")
        self.assertEqual(result["lifecycle_status"], "REVOKED")
        self.assertIn("revocation_bypass_attempt", result["violations"])

    def test_blocks_agent_mismatch(self):
        stack = replace(self.contracts["paac_email_demo"].agent_stack, agent_id="other-agent")
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(req(agent_stack=stack))
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("agent_mismatch", result["violations"])

    def test_blocks_agent_version_mismatch(self):
        stack = replace(self.contracts["paac_email_demo"].agent_stack, agent_version="9.9.9")
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(req(agent_stack=stack))
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("agent_version_mismatch", result["violations"])

    def test_blocks_model_mismatch(self):
        stack = replace(self.contracts["paac_email_demo"].agent_stack, model_id="other-model")
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(req(agent_stack=stack))
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("model_mismatch", result["violations"])

    def test_blocks_undeclared_tools(self):
        stack = replace(
            self.contracts["paac_email_demo"].agent_stack,
            tool_ids=self.contracts["paac_email_demo"].agent_stack.tool_ids + ("mock_contacts_export",),
        )
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(req(agent_stack=stack))
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("undeclared_tools", result["violations"])

    def test_blocks_undeclared_delegation(self):
        stack = replace(self.contracts["paac_email_demo"].agent_stack, delegated_by="planner-agent.mock")
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(req(agent_stack=stack))
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("undeclared_delegation", result["violations"])

    def test_blocks_unknown_contract(self):
        stack = self.contracts["paac_email_demo"].agent_stack
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(req(contract_id="missing_contract", agent_stack=stack))
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("missing_authorization", result["violations"])

    def test_blocks_replay_after_consumption(self):
        engine = EnforcementEngine(self.contracts, now=NOW)
        first = engine.evaluate(req())
        second = engine.evaluate(req())
        third = engine.evaluate(req())
        self.assertEqual(first["decision"], "ALLOW_WITH_LOG")
        self.assertEqual(second["decision"], "BLOCK")
        self.assertEqual(third["decision"], "BLOCK")
        self.assertIn("replay", second["violations"])
        self.assertIn("replay", third["violations"])

    def test_blocks_maximum_executions_exceeded(self):
        self.contracts["paac_email_demo"].maximum_executions = 1
        engine = EnforcementEngine(self.contracts, now=NOW)
        first = engine.evaluate(req(request_id="req_exec_1"))
        second = engine.evaluate(req(request_id="req_exec_2"))
        self.assertEqual(first["decision"], "ALLOW_WITH_LOG")
        self.assertEqual(second["decision"], "BLOCK")
        self.assertIn("execution_limit_exceeded", second["violations"])

    def test_every_decision_generates_evidence_and_credit_event(self):
        result = EnforcementEngine(self.contracts, now=NOW).evaluate(req())
        self.assertTrue(result["evidence"]["event_id"].startswith("ev_"))
        self.assertTrue(result["agent_credit_event"]["event_id"].startswith("ace_"))
        self.assertEqual(result["agent_credit_event"]["source_evidence_id"], result["evidence"]["event_id"])
        self.assertEqual(result["ledger_record"]["sequence"], 1)

    def test_evidence_ledger_detects_mutation(self):
        engine = EnforcementEngine(self.contracts, now=NOW)
        engine.evaluate(req())
        self.assertTrue(engine.ledger.verify_integrity())
        engine.ledger.records[0]["event"]["decision"] = "ALLOW"
        self.assertFalse(engine.ledger.verify_integrity())


if __name__ == "__main__":
    unittest.main()
