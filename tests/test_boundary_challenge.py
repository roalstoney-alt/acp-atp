import unittest

from challenge.run_boundary_challenge import run_scenarios


class BoundaryChallengeTests(unittest.TestCase):
    def test_all_boundary_challenge_scenarios_pass(self):
        results = run_scenarios()
        self.assertEqual(len(results), 15)
        self.assertTrue(all(result["passed"] for result in results), results)


if __name__ == "__main__":
    unittest.main()
