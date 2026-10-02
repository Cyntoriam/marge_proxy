from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, model_serializer, model_validator


class EquityPillar(str, Enum):
	"""The 5 Pillars of the M.A.R.G.E. Equity Taxonomy."""

	SPATIAL_ECONOMIC_ERASURE = "Spatial & Economic Erasure"
	INTERSECTIONAL_BURDEN = "Intersectional Amplification & Burden"
	RESOURCE_REDLINING = "Resource & Infrastructure Redlining"
	PROCEDURAL_VOICENESS = "Procedural Erasure & Voicelessness"
	CHRONIC_STRESS_ALLOSTATIC = "Chronic Stress & Allostatic Load"


class SeverityLevel(str, Enum):
	"""Severity ratings for detected equity risks."""

	LOW = "Low"
	MEDIUM = "Medium"
	HIGH = "High"
	CRITICAL = "Critical"


class PillarEvaluation(BaseModel):
	"""Detailed evaluation for one pillar, with legacy API compatibility."""

	pillar_name: str = Field(
		...,
		description="The equity pillar being evaluated, such as linguistic accessibility or geographic equity.",
	)
	bias_detected: bool = Field(
		..., description="Whether bias or gatekeeping language was identified."
	)
	confidence_score: float = Field(
		..., ge=0.0, le=1.0, description="Confidence rating of the AI detector from 0.0 to 1.0."
	)
	observation: str = Field(..., description="The exact clause or phrasing flagged.")
	why_flagged: str = Field(
		..., description="The systemic impact or barrier created by this phrasing."
	)
	suggested_rewrite: str = Field(
		..., description="Inclusive, competency-focused alternative phrasing."
	)
	severity: SeverityLevel = Field(
		SeverityLevel.LOW, description="Severity level of the flagged harm."
	)

	@model_validator(mode="before")
	@classmethod
	def accept_legacy_fields(cls, values):
		if not isinstance(values, dict):
			return values

		data = dict(values)
		legacy_pillar = data.pop("pillar", None)
		if "pillar_name" not in data and legacy_pillar is not None:
			data["pillar_name"] = getattr(legacy_pillar, "value", legacy_pillar)

		legacy_flagged = data.pop("flagged", None)
		if "bias_detected" not in data and legacy_flagged is not None:
			data["bias_detected"] = legacy_flagged

		legacy_reasoning = data.pop("reasoning", None)
		if "why_flagged" not in data and legacy_reasoning is not None:
			data["why_flagged"] = legacy_reasoning
		data.setdefault("observation", "")
		data.setdefault("suggested_rewrite", "")

		return data

	@property
	def pillar(self) -> EquityPillar | str:
		try:
			return EquityPillar(self.pillar_name)
		except ValueError:
			return self.pillar_name

	@property
	def flagged(self) -> bool:
		return self.bias_detected

	@property
	def reasoning(self) -> str:
		return self.why_flagged

	@model_serializer(mode="wrap")
	def serialize_legacy_fields(self, handler):
		data = handler(self)
		pillar = self.pillar
		data.update(
			{
				"pillar": pillar.value if isinstance(pillar, EquityPillar) else pillar,
				"flagged": self.flagged,
				"reasoning": self.reasoning,
			}
		)
		return data


class MargeAuditResponse(BaseModel):
	"""Complete response contract for a M.A.R.G.E. audit."""

	overall_guardian_index: int = Field(
		..., ge=0, le=100, description="Score from 0 to 100 representing alignment."
	)
	evaluations: List[PillarEvaluation]
	self_correction_directive: str = Field(
		...,
		description="Instructions passed back to the AI model to correct its internal representation of the text.",
	)


class MARGEEvaluationPayload(BaseModel):
	"""The standard structured response payload returned by the M.A.R.G.E. proxy."""

	request_id: str = Field(..., description="Unique identifier for the incoming request.")
	path_type: str = Field(
		..., description="Indicates whether the request took 'Fast-Path' or 'Deep-Path'."
	)
	overall_approved: bool = Field(
		..., description="Final approval status of the incoming payload."
	)
	evaluations: List[PillarEvaluation] = Field(
		default_factory=list,
		description="Detailed evaluations across the equity pillars.",
	)
	suggested_correction: Optional[str] = Field(
		None, description="Suggested mitigation or prompt rewrite."
	)
	metadata: Dict[str, Any] = Field(
		default_factory=dict, description="Additional processing metadata."
	)
