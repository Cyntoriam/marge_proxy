# M.A.R.G.E.
### Meta-Alignment & Resilience Guard for Equity
*The Equity Guardian: sociotechnical equity auditing middleware.*

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-005571.svg)](https://fastapi.tiangolo.com/)

M.A.R.G.E.'s goal is to detect subtle equity risks in AI systems, including microaggressions, biased linguistic judgments, demographic stereotyping, accessibility barriers, and structural disparities in optimization. For example, delivery targets that ignore local infrastructure may impose unequal burdens. The project builds on lexical auditing tools such as Kat Matfield's [Gender Decoder](https://gender-decoder.katmatfield.com/) and extends that focus toward broader sociotechnical risks.

> **Prototype status:** `/evaluate` uses an async route. Tier 1 uses a small regex list. Tier 2 can call the OpenAI API for structured evaluations when configured; otherwise it returns illustrative fallback evaluations. This is not production-grade middleware, does not audit live RAG corpora or agent behavior, and must not be used for automated high-impact decisions. A clean result is not evidence of fairness; involve domain experts and affected communities.

## Intended Pipeline

- **Tier 1:** Heuristic input and parameter routing; a basic regex filter exists today.
- **Tier 2:** Structured equity review through the OpenAI SDK; without credentials or if the request fails, illustrative fallback evaluations are returned.
- **Tier 3:** Policy-based corrections or human review; not implemented.

Live RAG corpus inspection, prompt-injection analysis, and agent-behavior evaluation remain future work.

## Proposed Future Taxonomy

1. **Stereotypical & Demographic Framing:** Assumptions about roles or capabilities based on demographic generalizations.
2. **Intersectional Microaggressions:** Exclusionary language or slights targeting intersecting identities.
3. **Disability & Accessibility Justice:** Inaccessible defaults and missing accommodations.
4. **Structural, Spatial & Economic Erasure:** Overlooked geographic, infrastructure, and socioeconomic conditions.
5. **Dialectal & Cultural Justice:** Unfair treatment of dialects and cultural vernacular.

This proposed taxonomy is not implemented. The API schema and [case-study matrix](docs/case_studies_matrix.md) still use the current five-pillar taxonomy defined in `app/schemas.py`.

## Principles

The project draws on ACM Code of Ethics principles 1.2 (avoid harm) and 1.4 (fairness), and IEEE's Ethically Aligned Design. These references motivate the work; they do not certify the implementation or establish legal compliance.

The current `/evaluate` request accepts a JSON object. `prompt` and `parameters` are inspected by the tiers; `request_id` is copied into the response and defaults to `req_unknown`.

Example request:

```json
{
	"request_id": "demo-001",
	"prompt": "Prioritize delivery access across neighborhoods.",
	"parameters": {"service": "delivery"}
}
```

## Getting Started

Use Python 3.10 or newer, then install the dependencies and start the API from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

To enable the live Tier 2 judge, set `OPENAI_API_KEY` or `LLM_API_KEY`. It defaults to model `gpt-4o-mini`; optionally set `LLM_BASE_URL` and `LLM_MODEL` for a compatible service and model. Without a key, Tier 2 returns illustrative fallback evaluations.

The health check is available at `GET http://127.0.0.1:8000/`. Interactive API documentation is at `http://127.0.0.1:8000/docs`.

Send an evaluation request with:

```bash
curl -X POST http://127.0.0.1:8000/evaluate \
	-H 'Content-Type: application/json' \
	-d '{"request_id":"demo-001","prompt":"Prioritize delivery access across neighborhoods.","parameters":{"service":"delivery"}}'
```

## Testing and Red Teaming

No automated test suite is currently included. The [Case Studies Matrix](docs/case_studies_matrix.md) provides example scenarios and red-team prompts for manual evaluation. Treat outputs as prototype signals: review both false positives and false negatives, involve affected communities and subject-matter experts, and document limitations before any deployment.

## Current Limitations

- Tier 1 remains a small synchronous heuristic filter; only the API route and Tier 2 HTTP call are asynchronous.
- Tier 1 uses a small illustrative pattern list; it is not comprehensive or language-independent.
- Tier 2 depends on a compatible external service for live judgments; fallback evaluations are illustrative, not semantic assessments.
- The current route marks all deep-path results unapproved and all fast-path results approved; these defaults are not calibrated policy decisions.
- The response does not represent a validated fairness assessment, and no production privacy, security, monitoring, or appeals controls are provided.