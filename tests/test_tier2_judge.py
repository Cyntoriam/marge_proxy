import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from app.schemas import EquityPillar, PillarEvaluation
from app.tiers.tier2_judge import MARGEJudgeResponse, evaluate_with_llm, run_async_marge_audit


class AsyncMargeAuditTest(unittest.IsolatedAsyncioTestCase):
	async def test_configured_openai_path_uses_structured_parse(self):
		evaluations = [
			PillarEvaluation(
				pillar_name=pillar.value,
				bias_detected=False,
				confidence_score=0.9,
				observation="",
				why_flagged="No signal was detected.",
				suggested_rewrite="",
			)
			for pillar in EquityPillar
		]
		parsed = MARGEJudgeResponse(evaluations=evaluations)
		completion = SimpleNamespace(
			choices=[SimpleNamespace(message=SimpleNamespace(parsed=parsed))]
		)
		class MockAsyncClient:
			def __init__(self):
				self.beta = SimpleNamespace(
					chat=SimpleNamespace(
						completions=SimpleNamespace(
							parse=AsyncMock(return_value=completion)
						)
					)
				)

			async def __aenter__(self):
				return self

			async def __aexit__(self, *_args):
				return False

		client = MockAsyncClient()

		with (
			patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}),
			patch("app.tiers.tier2_judge.openai.AsyncOpenAI", return_value=client),
		):
			result = await evaluate_with_llm(
				"Policy text", {"scan_type": "Deep Architectural Scan"}
			)

		self.assertEqual(len(result), 5)
		messages = client.beta.chat.completions.parse.await_args.kwargs["messages"]
		self.assertIn("Deep Architectural Scan", messages[0]["content"])

	async def test_builds_response_from_structured_evaluations(self):
		evaluations = [
			PillarEvaluation(
				pillar_name=EquityPillar.SPATIAL_ECONOMIC_ERASURE.value,
				bias_detected=True,
				confidence_score=0.9,
				observation="on-site only",
				why_flagged="May restrict access for people who cannot travel.",
				suggested_rewrite="Offer remote participation where practical.",
			),
			PillarEvaluation(
				pillar_name=EquityPillar.INTERSECTIONAL_BURDEN.value,
				bias_detected=False,
				confidence_score=0.8,
				observation="",
				why_flagged="No matching signal was observed.",
				suggested_rewrite="",
			),
		]

		with patch(
			"app.tiers.tier2_judge.evaluate_with_llm",
			new=AsyncMock(return_value=evaluations),
		) as evaluator:
			result = await run_async_marge_audit("on-site only", "Deep Architectural Scan")

		evaluator.assert_awaited_once_with(
			"on-site only", {"scan_type": "Deep Architectural Scan"}
		)
		self.assertEqual(result.overall_guardian_index, 80)
		self.assertIn("Offer remote participation", result.self_correction_directive)

	async def test_explicit_api_key_is_forwarded(self):
		evaluations = [
			PillarEvaluation(
				pillar_name=EquityPillar.SPATIAL_ECONOMIC_ERASURE.value,
				bias_detected=False,
				confidence_score=0.9,
				observation="",
				why_flagged="No signal was detected.",
				suggested_rewrite="",
			)
		]
		with patch(
			"app.tiers.tier2_judge.evaluate_with_llm",
			new=AsyncMock(return_value=evaluations),
		) as evaluator:
			await run_async_marge_audit(
				"Policy text", "Standard Guardian Scan", api_key="test-key"
			)

		evaluator.assert_awaited_once_with(
			"Policy text",
			{"scan_type": "Standard Guardian Scan"},
			api_key="test-key",
		)


if __name__ == "__main__":
	unittest.main()