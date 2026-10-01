# M.A.R.G.E. (Meta-Alignment & Resilience Guard for Equity)
### "The Equity Guardian"

M.A.R.G.E. is a lightweight FastAPI prototype for auditing AI prompts and system logic for equity risks. It is designed to flag issues such as spatial redlining, demographic stereotyping, accessibility bias, coded microaggressions, and dialectal exclusion before a model or workflow goes live.

This repo is intentionally honest about scope: it is not a production fairness engine, live policy oracle, or verified social-science benchmark. It is a red-teaming scaffold and prototype policy-audit layer for experimentation, documentation, and iterative review.

---

## Five-Pillar Equity Taxonomy

The current implementation and schema are aligned to the following five pillars:

1. **Stereotypical & Demographic Framing** — demographic assumptions and proxy-based penalties in screening.
2. **Intersectional Amplification & Burden** — coded bias, gendered double standards, and compound proxy effects.
3. **Disability & Accessibility Justice** — ableist assumptions and caregiving/medical-leave penalties.
4. **Structural, Spatial & Economic Erasure** — geographic exclusion, transit disparities, and infrastructure-based redlining.
5. **Dialectal & Cultural Justice** — unfair treatment of vernacular, community language, and non-dominant speech styles.

The future taxonomic language in the project docs is conceptually useful, but the live schema in `app/schemas.py` is the authoritative implementation standard.

---

## Repository Structure

```text
marge_proxy/
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI evaluation router
│   ├── schemas.py                      # Strict Pydantic response models
│   ├── marge_job_hunting_case_studies.py # Structured red-teaming case objects
│   └── tiers/
│       ├── __init__.py
│       ├── tier1_filter.py
│       └── tier2_judge.py
├── docs/
│   └── case_studies_matrix.md          # Human-review matrix and red-team scenarios
├── test_client.py                      # Local integration smoke test
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Getting Started

### 1. Installation

```bash
git clone https://github.com/your-username/marge_proxy.git
cd marge_proxy
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the application

```bash
uvicorn app.main:app --reload
```

The app exposes:

- `GET /` for health check
- `POST /evaluate` for structured equity review

### 3. Run the automated client

In a separate terminal:

```bash
python test_client.py
```

The client exercises the job-hunting red-teaming cases against the local `/evaluate` endpoint.

---

## Prototype Status

This project currently includes:

- an async FastAPI route
- Tier 1 heuristic routing logic
- optional Tier 2 review using an OpenAI-compatible client
- illustrative fallback evaluations when no external service is configured

This project does not currently include:

- production-grade governance controls
- validated fairness benchmarks
- live RAG or agent-behavior audit coverage
- a calibrated policy engine for enforcement decisions

A "clean" result is not evidence of fairness. Human review, subject-matter expertise, and affected-community input remain essential.

---

## Red-Teaming and Review

The repository includes a structured case-study matrix at [docs/case_studies_matrix.md](docs/case_studies_matrix.md) and a programmable red-team set in `app/marge_job_hunting_case_studies.py`.

These artifacts are designed for exploratory assessment and human review, not as formal performance claims. The current implementations are intentionally illustrative and should be treated as a prototype foundation for future work.