import unittest
from pathlib import Path


DASHBOARD_PATH = Path(__file__).resolve().parents[1] / "dashboard.py"


class DashboardBrandingTest(unittest.TestCase):
    def test_dashboard_uses_consistent_guardian_branding(self):
        source = DASHBOARD_PATH.read_text()

        self.assertIn(".guardian-scale-container", source)
        self.assertIn(".guardian-arrow-marker", source)
        self.assertIn("M.A.R.G.E. Guardian Index", source)
        self.assertNotIn("Artemis Keyword Signal Index", source)


if __name__ == "__main__":
    unittest.main()
