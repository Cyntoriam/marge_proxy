import re
from typing import Any, Dict, Tuple


class Tier1Filter:
	"""
	Tier 1: Pre-generation heuristic and regex filtering.
	Separates benign requests ('Fast-Path') from high-risk vectors ('Deep-Path').
	"""

	def __init__(self):
		self.high_risk_patterns = [
			r"exclude\s+(?:zipcode|postal code|neighborhood)",
			r"impossible\s+delivery\s+window",
			r"demographic\s+assumption",
			r"lower\s+priority\s+zone",
		]

	def evaluate_request(self, payload: Dict[str, Any]) -> Tuple[str, str]:
		content = payload.get("prompt", "") + " " + str(payload.get("parameters", {}))
		content_lower = content.lower()

		for pattern in self.high_risk_patterns:
			if re.search(pattern, content_lower):
				return "Deep-Path", f"Triggered high-risk heuristic pattern: {pattern}"

		return "Fast-Path", "Passed initial heuristic scrutiny."
