import unittest

from trust_layer.demo_runner import run_demo


class DemoTests(unittest.TestCase):
    def test_demo_covers_required_decision_types(self):
        decisions = {result["decision"] for result in run_demo()}
        self.assertIn("ALLOW", decisions)
        self.assertIn("ALLOW_WITH_LOG", decisions)
        self.assertIn("REQUIRE_CONFIRMATION", decisions)
        self.assertIn("BLOCK", decisions)

    def test_demo_blocks_file_delete_and_upload(self):
        results = run_demo()
        blocked = [r for r in results if r["decision"] == "BLOCK"]
        reasons = {reason for result in blocked for reason in result["reasons"]}
        self.assertIn("action_explicitly_prohibited", reasons)


if __name__ == "__main__":
    unittest.main()
