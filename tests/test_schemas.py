import unittest

from app.schemas import (
	EquityPillar,
	MargeAuditResponse,
	PillarEvaluation,
	SeverityLevel,
)


class PillarEvaluationSchemaTest(unittest.TestCase):
	def test_new_audit_fields_validate(self):
		evaluation = PillarEvaluation(
			pillar_name=EquityPillar.PROCEDURAL_VOICENESS.value,
			bias_detected=True,
			confidence_score=0.82,
			observation="No remote accommodations",
			why_flagged="This may exclude people with mobility needs.",
			suggested_rewrite="Offer remote participation as an option.",
		)
		response = MargeAuditResponse(
			overall_guardian_index=76,
			evaluations=[evaluation],
			self_correction_directive="Use accessible participation criteria.",
		)

		self.assertEqual(response.evaluations[0].pillar, EquityPillar.PROCEDURAL_VOICENESS)
		self.assertTrue(response.evaluations[0].flagged)

	def test_legacy_fields_remain_accepted_and_serialized(self):
		evaluation = PillarEvaluation(
			pillar=EquityPillar.SPATIAL_ECONOMIC_ERASURE,
			flagged=False,
			severity=SeverityLevel.LOW,
			confidence_score=0.98,
			reasoning="No signal was detected.",
		)

		serialized = evaluation.model_dump()
		self.assertEqual(serialized["pillar_name"], EquityPillar.SPATIAL_ECONOMIC_ERASURE.value)
		self.assertEqual(serialized["pillar"], EquityPillar.SPATIAL_ECONOMIC_ERASURE.value)
		self.assertFalse(serialized["bias_detected"])
		self.assertFalse(serialized["flagged"])
		self.assertEqual(serialized["reasoning"], "No signal was detected.")

	def test_descriptive_pillar_names_are_supported(self):
		evaluation = PillarEvaluation(
			pillar_name="Linguistic Accessibility & Gatekeeping",
			bias_detected=True,
			confidence_score=0.98,
			observation="flawless executive presence",
			why_flagged="May act as a proxy filter.",
			suggested_rewrite="Assess demonstrated communication skills.",
		)

		self.assertEqual(evaluation.pillar, "Linguistic Accessibility & Gatekeeping")
		response = MargeAuditResponse(
			overall_guardian_index=42,
			evaluations=[evaluation],
			self_correction_directive="Use competency-based criteria.",
		)
		serialized = response.model_dump(mode="json")

		self.assertEqual(
			serialized["evaluations"][0]["pillar_name"],
			"Linguistic Accessibility & Gatekeeping",
		)
		self.assertEqual(
			serialized["evaluations"][0]["pillar"],
			"Linguistic Accessibility & Gatekeeping",
		)


if __name__ == "__main__":
	unittest.main()