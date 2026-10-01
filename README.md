# M.A.R.G.E. (Meta-Alignment & Resilience Guard for Equity)
### "The Equity Guardian"

M.A.R.G.E. (The Equity Guardian) is a sociotechnical equity auditing middleware designed to detect subtle equity risks in AI systems, including microaggressions, biased linguistic judgments, demographic stereotyping, accessibility barriers, and structural disparities in optimization.

Building on lexical auditing tools such as Kat Matfield's Gender Decoder, the project extends its focus toward broader sociotechnical risks across a comprehensive equity taxonomy.

---

## 🏛️ The Five-Pillar Equity Taxonomy

M.A.R.G.E. evaluates prompts and model payloads across five core equity pillars:
1. **Stereotypical & Demographic Framing:** Assumptions about roles or capabilities based on demographic generalizations.
2. **Intersectional Amplification & Burden (Intersectional Microaggressions):** Exclusionary language or slights targeting intersecting identities.
3. **Disability & Accessibility Justice:** Inaccessible defaults and missing accommodations.
4. **Structural, Spatial & Economic Erasure:** Overlooked geographic, infrastructure, and socioeconomic conditions (such as delivery targets ignoring local infrastructure).
5. **Dialectal & Cultural Justice:** Unfair treatment of dialects and cultural vernacular.

---

## ⚙️ Architecture & Intended Pipeline

* **Tier 1 (Heuristic & Routing):** Input and parameter routing via asynchronous FastAPI endpoints and heuristic/regex pattern filtering.
* **Tier 2 (Structured Evaluation):** Structured equity review through the OpenAI SDK (defaults to `gpt-4o-mini`, customizable via `LLM_BASE_URL` and `LLM_MODEL`). Without credentials or if requests fail, illustrative fallback evaluations are returned.
* **Tier 3 (Remediation & Policy):** Policy-based corrections and automated remediation handling.

---

## 📁 Repository Structure

```text
marge_proxy/
├── app/
│   ├── __init__.py
│   ├── main.py                          # Asynchronous FastAPI evaluation router
│   ├── schemas.py                       # Strict Pydantic enforcement models
│   ├── marge_job_hunting_case_studies.py # Structured red-teaming case objects
│   └── tiers/                           # Multi-tiered evaluation & remediation logic
├── docs/
│   └── case_studies_matrix.md           # Human-review matrix & red-team hypotheses
├── test_client.py                       # Automated integration test runner
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### 1. Installation & Environment Setup
Clone the repository and install dependencies using Python 3.10 or newer:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2. Run the FastAPI Server
Launch the asynchronous evaluation backend locally using Uvicorn:

```bash
uvicorn app.main:app --reload
```

*Health check available at `GET http://127.0.0.1:8000/`. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.*

### 3. Execute the Automated Test Client
In a separate terminal window, run the test client to fire red-teaming case studies against the live `/evaluate` endpoint:

```bash
python test_client.py
```

## 🔬 Red-Teaming & Validation (Phase 2)
M.A.R.G.E. treats red-team prompts as active hypotheses to investigate. Detailed human-review scenarios and evaluation rubrics are documented in [`docs/case_studies_matrix.md`](docs/case_studies_matrix.md) and executed programmatically via `app/marge_job_hunting_case_studies.py`.

## ⚖️ Ethical Grounding & Disclaimers
The project draws on ACM Code of Ethics principles 1.2 (avoid harm) and 1.4 (fairness), and IEEE's Ethically Aligned Design. These references motivate the work; they do not certify the implementation or establish legal compliance.

*Prototype Status:* This is not production-grade middleware, does not audit live RAG corpora or agent behavior, and must not be used for automated high-impact decisions. A clean result is not evidence of fairness; involve domain experts and affected communities.
