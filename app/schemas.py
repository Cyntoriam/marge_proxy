from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


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
	"""Evaluation details for a specific equity pillar."""

	pillar: EquityPillar
	flagged: bool = Field(..., description="Whether this equity pillar was triggered.")
	severity: SeverityLevel = Field(
		SeverityLevel.LOW, description="Severity level of the flagged harm."
	)
	confidence_score: float = Field(
		..., ge=0.0, le=1.0, description="Confidence score of the evaluation."
	)
	reasoning: str = Field(
		..., description="Explanation of why this pillar was flagged or cleared."
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
