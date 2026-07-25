import json
import unittest
from pathlib import Path

import jsonschema

from trust_layer.core import EnforcementEngine
from trust_layer.fixtures import alpha_contracts
from test_enforcement import NOW, req


class SchemaFileTests(unittest.TestCase):
    def test_schema_files_are_valid_json(self):
        for path in Path("schemas").glob("*.json"):
            data = json.loads(path.read_text())
            self.assertIn("$schema", data)
            self.assertEqual(data.get("type"), "object")

    def test_generated_evidence_validates_against_schema(self):
        schema = json.loads(Path("schemas/evidence-event-v0.1.schema.json").read_text())
        result = EnforcementEngine(alpha_contracts(), now=NOW).evaluate(req())
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(result["evidence"], schema)

    def test_valid_paac_document_validates_against_schema(self):
        schema = json.loads(Path("schemas/paac-v0.1.schema.json").read_text())
        document = {
            "paac_version": "0.1",
            "contract_id": "paac_schema_valid",
            "principal": {"type": "individual", "pseudonymous_id": "user_local_001"},
            "agent_stack": {
                "agent_id": "email-agent.mock",
                "agent_version": "0.1",
                "model_id": "model.mock.safe",
                "tool_ids": ["email.mock"],
            },
            "purpose": "Schema validation fixture.",
            "permitted_actions": ["email.draft"],
            "prohibited_actions": ["email.export_contacts"],
            "resources": {"email_allowed_recipient_domains": ["example.com"]},
            "constraints": {"max_execution_count": 1},
            "validity": {"valid_from": "2026-07-21T00:00:00Z", "valid_until": "2026-07-28T00:00:00Z"},
            "confirmation_required_actions": [],
            "log_required_actions": ["email.draft"],
        }
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.validate(document, schema)


if __name__ == "__main__":
    unittest.main()
