from fastapi import FastAPI, HTTPException
from app.schemas import MARGEEvaluationPayload, PillarEvaluation, EquityPillar, SeverityLevel
from app.tiers.tier1_filter import Tier1Filter
from app.tiers.tier2_judge import Tier2Judge

# Initialize the FastAPI application
app = FastAPI(
    title="M.A.R.G.E. Proxy",
    description="Meta-Alignment & Resilience Guard for Equity - Asynchronous Middleware Proxy",
    version="0.1.0"
)

# Initialize our filters and judges
tier1_filter = Tier1Filter()
tier2_judge = Tier2Judge()

@app.get("/")
def read_root():
    """Health check endpoint to verify the proxy is alive."""
    return {"status": "online", "project": "M.A.R.G.E.", "message": "Equity guard proxy is running."}

@app.post("/evaluate", response_model=MARGEEvaluationPayload)
async def evaluate_incoming_request(payload: dict):
    """
    Receives incoming prompts/parameters, runs Tier 1 heuristic scrutiny,
    conditionally triggers Tier 2 deep audit, and returns a structured safety payload.
    """
    try:
        request_id = payload.get("request_id", "req_unknown")

        # Step 1: Run Tier 1 filter
        path_type, reason = tier1_filter.evaluate_request(payload)

        # Step 2: Route based on path type
        if path_type == "Fast-Path":
            overall_approved = True
            # Clean request gets a baseline passing evaluation
            evaluations = [
                PillarEvaluation(
                    pillar=EquityPillar.SPATIAL_ECONOMIC_ERASURE,
                    flagged=False,
                    severity=SeverityLevel.LOW,
                    confidence_score=0.98,
                    reasoning=reason
                )
            ]
            suggested_correction = None
            metadata = {"tier_processed": "Tier 1 (Fast-Path)"}

        else:
            # Deep-Path: Hand off to Tier 2 Judge for semantic equity audit
            overall_approved = False
            evaluations = await tier2_judge.audit_payload(payload, reason)
            suggested_correction = "Rewrite prompt to remove demographic assumptions and ensure equitable geographic distribution."
            metadata = {"tier_processed": "Tier 1 & Tier 2 (Deep-Path Audit)"}

        # Construct our strict Pydantic response payload
        response_payload = MARGEEvaluationPayload(
            request_id=request_id,
            path_type=path_type,
            overall_approved=overall_approved,
            evaluations=evaluations,
            suggested_correction=suggested_correction,
            metadata=metadata
        )

        return response_payload

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
