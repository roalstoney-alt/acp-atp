import unittest

from integrations.selected_framework.demo import run_demo


class IntegrationAdapterTests(unittest.TestCase):
    def test_selected_framework_adapter_demo(self):
        result = run_demo()
        self.assertEqual(result["allow"], "ALLOW")
        self.assertEqual(result["confirmation_pause"], "REQUIRE_CONFIRMATION")
        self.assertEqual(result["confirmed"], "ALLOW_WITH_LOG")
        self.assertEqual(result["revoked"], "BLOCK")
        self.assertEqual(result["undeclared_tool"], "BLOCK")
        self.assertTrue(result["evidence_integrity"])


if __name__ == "__main__":
    unittest.main()
