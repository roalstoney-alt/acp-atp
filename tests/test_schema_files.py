import json
import unittest
from pathlib import Path
from datetime import datetime, timezone

from jsonschema import Draft202012Validator, FormatChecker

from trust_layer.core import EnforcementEngine
from trust_layer.fixtures import alpha_contracts
from trust_layer.loader import PAACValidationError, load_paac_file
from trust_layer.models import ActionRequest


NOW = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)


class SchemaFileTests(unittest.TestCase):
    def test_schema_files_are_valid_json(self):
        for path in Path("schemas").glob("*.json"):
            data = json.loads(path.read_text())
            self.assertIn("$schema", data)
            self.assertEqual(data.get("type"), "object")

    def test_paac_valid_fixture_passes_draft_2020_12_schema(self):
        schema = json.loads(Path("schemas/paac-v0.1.schema.json").read_text())
        fixture = json.loads(Path("tests/fixtures/paac_valid_email.json").read_text())
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        self.assertEqual(list(validator.iter_errors(fixture)), [])

    def test_paac_invalid_fixture_fails_draft_2020_12_schema(self):
        schema = json.loads(Path("schemas/paac-v0.1.schema.json").read_text())
        fixture = json.loads(Path("tests/fixtures/paac_invalid_missing_agent_version.json").read_text())
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        self.assertTrue(list(validator.iter_errors(fixture)))

    def test_loader_constructs_runtime_contract(self):
        contract = load_paac_file("tests/fixtures/paac_valid_email.json")
        self.assertEqual(contract.contract_id, "paac_email_fixture")
        self.assertEqual(contract.agent_id, "email-agent.mock")
        self.assertEqual(contract.agent_version, "0.1.1")
        self.assertEqual(contract.model_id, "mock-llm-email-v1")
        self.assertIn("mock_email_send", contract.declared_tools)
        self.assertEqual(contract.maximum_executions, 10)
        self.assertEqual(contract.delegation_policy, "none")

    def test_loader_rejects_semantically_invalid_contract(self):
        with self.assertRaises(PAACValidationError):
            load_paac_file("tests/fixtures/paac_invalid_semantic_overlap.json")

    def test_generated_events_match_event_schemas(self):
        contracts = alpha_contracts()
        request = ActionRequest(
            request_id="req_schema_event",
            contract_id="paac_email_demo",
            agent_stack=contracts["paac_email_demo"].agent_stack,
            action_type="email.draft",
            resource="mailbox",
            params={"recipients": ["alice@example.com"], "content_hash": "sha256:x"},
            created_at=NOW,
        )
        result = EnforcementEngine(contracts, now=NOW).evaluate(request)
        for schema_name, payload_key in [
            ("evidence-event-v0.1.schema.json", "evidence"),
            ("agent-credit-event-v0.1.schema.json", "agent_credit_event"),
        ]:
            schema = json.loads(Path("schemas", schema_name).read_text())
            validator = Draft202012Validator(schema, format_checker=FormatChecker())
            self.assertEqual(list(validator.iter_errors(result[payload_key])), [])


if __name__ == "__main__":
    unittest.main()
