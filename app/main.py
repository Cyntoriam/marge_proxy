import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="M.A.R.G.E. | Multimodal Automated Real-time Guardian Engine",
    page_icon="🏹",
    layout="wide",
)

# --- THEME & OSHUN WARM GOLD HEADER SETUP ---
st.markdown(
    """
    <style>
    .marge-header {
        background-color: #121212;
        padding: 2.2rem;
        border-radius: 12px;
        color: #f3f3f8;
        margin-bottom: 2rem;
        box-shadow: 0 0 20px rgba(255, 184, 0, 0.15);
        border: 1px solid rgba(255, 184, 0, 0.4);
        text-align: center;
    }
    .marge-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
        color: #ffb800;
        letter-spacing: 0.5px;
    }
    .marge-subtitle {
        font-size: 1.15rem;
        color: #e0e0e0;
        font-weight: 300;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .marge-tagline {
        font-size: 0.95rem;
        color: #ffb800;
        font-style: italic;
        margin-top: 0.4rem;
    }
    .guardian-card {
        background-color: #1a1b26;
        padding: 1.2rem;
        border-radius: 8px;
        border-left: 4px solid #ffb800;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.04);
    }
    .severity-pill {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1rem;
        color: #ffffff;
        text-align: center;
    }
    stMarkdown ul {
        list-style: none;
        padding-left: 0;
    }
    stMarkdown ul li::before {
        content: "🏹 ";
        color: #ffb800;
        font-weight: bold;
    }
    </style>
    <div class="marge-header">
        <div class="marge-title">M.A.R.G.E. 🏹</div>
        <div class="marge-subtitle">MULTIMODAL AUTOMATED REAL-TIME GUARDIAN ENGINE</div>
        <div class="marge-tagline">The Equity Guardian — Sociotechnical Middleware</div>
    </div>
""",
    unsafe_allow_html=True,
)

# --- PYDANTIC VALIDATION MODELS (Deterministic Governance & Schema Enforcement) ---
class PillarEvaluation(BaseModel):
    pillar_name: str = Field(..., description="Name of the Five-Pillar taxonomy category.")
    severity_score: float = Field(..., ge=0.0, le=1.0, description="Normalized severity score between 0.0 and 1.0.")
    issue_identified: str = Field(..., description="Description of structural bias or microaggression.")
    detailed_explanation: str = Field(..., description="Explanation of why this violates the pillar context.")
    active_remedy: str = Field(..., description="Actionable structural rewrite or remediation.")

    @field_validator('severity_score')
    @classmethod
    def validate_score_bounds(cls, v: float) -> float:
        if not (0.0 <= v <= 1.0):
            raise ValueError('Severity score must be mathematically bound between 0.0 and 1.0.')
        return v

class MARGEEvaluationPayload(BaseModel):
    original_text: str
    remediated_text: str
    guardian_index: int = Field(..., ge=0, le=100, description="Guardian Index score from 0 to 100.")
    violations: List[PillarEvaluation] = Field(default_factory=list)
    
    @field_validator('guardian_index')
    @classmethod
    def validate_guardian_index(cls, v: int) -> int:
        if not (0 <= v <= 100):
            raise ValueError('Guardian Index must be bound between 0 and 100.')
        return v

# --- SIDEBAR: VISITOR PORTAL & AI-TO-AI CONFIG ---
with st.sidebar:
    st.markdown("### 🏹 Guardian Controls")
    user_handle = st.text_input("Your Name / Handle", value="Pocketdoc")
    
    st.markdown("---")
    st.markdown("### ⚡ AI-to-AI Engine Config")
    enable_ai_to_ai = st.toggle("Enable AI-to-AI Interceptor", value=True)
    st.markdown("<small>Oshun theme active: charcoal and honey-gold.[cite: 1] Self-contained mode: no API request or external service is used.</small>", unsafe_allow_html=True)

# --- FIVE-PILLAR TAXONOMY ---
FIVE_PILLARS = {
    "Pillar 1: Stereotypical & Demographic Framing": "Catches automated assumptions of roles or capabilities based on demographic generalizations.",
    "Pillar 2: Intersectional Microaggressions": "Flags subtle slights, exclusionary phrasing, and dog-whistles targeting compounded identity vectors.",
    "Pillar 3: Disability & Accessibility Justice": "Audits systems for ableist assumptions, inaccessible defaults, and systemic erasure of accommodations.",
    "Pillar 4: Structural, Spatial & Economic Erasure": "Detects when optimization models ignore localized infrastructure or socio-economic realities.",
    "Pillar 5: Dialectal & Cultural Justice": "Protects AAVE, regional dialects, and cultural vernacular against false-positive aggression flags.",
}

# --- ASYNCHRONOUS AUDITING & ACTIVE REMEDIATION ENGINE WITH PURE VALIDATION ---
async def async_marge_deep_audit(target_text: str, ai_to_ai_active: bool) -> MARGEEvaluationPayload:
    await asyncio.sleep(1.0) # Simulate fast async inspection
    
    violations_data = []
    remediated_text = target_text
    text_lower = target_text.lower()

    if any(p in text_lower for p in ["those people", "inner city", "they always"]):
        violations_data.append(
            PillarEvaluation(
                pillar_name="Pillar 1: Stereotypical & Demographic Framing",
                severity_score=0.85,
                issue_identified="Broad geographic or socio-economic generalization used to disenfranchise capabilities.",
                detailed_explanation="The text reduces diverse individuals into a homogenized, stereotyped collective.",
                active_remedy="Completely remove geographic or socio-economic qualifiers when discussing capability and replace with merit-based, individualized language."
            )
        )
        remediated_text = remediated_text.replace("Some folks from the inner city are just not cut out for tech leadership;", "Candidates possess diverse lived experiences and leadership potential;")
        remediated_text = remediated_text.replace("they are often too aggressive during reviews.", "Evaluations must focus strictly on objective technical competencies and collaborative milestones.")

    if any(p in text_lower for p in ["so articulate", "aggressive", "bossy", "where are you really from"]):
        violations_data.append(
            PillarEvaluation(
                pillar_name="Pillar 2: Intersectional Microaggressions",
                severity_score=0.75,
                issue_identified="Coded behavioral microaggression applied to penalize communication styles.",
                detailed_explanation="Using words like 'aggressive' during evaluations disproportionately penalizes marginalized groups under coded double standards.",
                active_remedy="Strip out all subjective behavior-policing adjectives. Substitute with explicit, measurable operational standards."
            )
        )
        remediated_text = remediated_text.replace("too aggressive", "direct and assertive in communication")