import unittest
from pathlib import Path


DASHBOARD_PATH = Path(__file__).resolve().parents[1] / "dashboard.py"


class DashboardBrandingTest(unittest.TestCase):
    def test_dashboard_uses_consistent_guardian_branding(self):
        source = DASHBOARD_PATH.read_text()

        self.assertIn(".guardian-scale-container", source)
        self.assertIn(".guardian-arrow-marker", source)
        self.assertIn("Guardian Index", source)
        self.assertNotIn("M.A.R.G.E. Guardian Index", source)
        self.assertNotIn("Artemis Keyword Signal Index", source)

    def test_equity_evaluator_uses_guardian_signal_contract(self):
        namespace = {}
        exec(DASHBOARD_PATH.read_text(), namespace)
        result = namespace["evaluate_equity_payload"]("The team is fast-paced and open to all candidates.")

        self.assertIn("guardian_signal_index", result)
        self.assertNotIn("keyword_signal_index", result)
        self.assertIn("assessment", result)


if __name__ == "__main__":
    unittest.main()
