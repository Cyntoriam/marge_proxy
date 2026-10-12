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

# --- GLOBAL BURNT ORANGE & MOBILE-FIRST FLUID STYLING ---
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #240c03 0%, #120501 60%, #0a0301 100%) !important;
        color: #fcebe6 !important;
    }
    
    .block-container {
        max-width: 100% !important;
        padding-top: 1.2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* Main Page Control Panel */
    .control-panel {
        background-color: #170702;
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid rgba(224, 86, 36, 0.4);
        margin-bottom: 1.5rem;
    }

    /* Header Box */
    .marge-header {
        background: linear-gradient(135deg, #2e1004 0%, #1a0802 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: #ffffff;
        margin-bottom: 1.2rem;
        box-shadow: 0 6px 20px rgba(224, 86, 36, 0.3);
        border: 2px solid #e05624;
        text-align: center;
    }
    .marge-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
        color: #ffb800;
        letter-spacing: 0.5px;
    }
    .marge-subtitle {
        font-size: 0.95rem;
        color: #f3d0c7;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }
    .marge-essence {
        font-size: 0.85rem;
        color: #ffb800;
        font-style: italic;
        margin-top: 0.3rem;
    }
    .guardian-card {
        background-color: #1c0802;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffb800;
        margin-bottom: 0.8rem;
        border: 1px solid rgba(255, 184, 0, 0.25);
        color: #fcebe6;
    }
    .degradation-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: bold;
        background-color: rgba(224, 86, 36, 0.25);
        border: 1px solid #e05624;
        color: #ffb800;
        margin-top: 0.4rem;
    }
    .streamlit-expanderHeader {
        background-color: #240c03 !important;
        color: #ffb800 !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        border: 1px solid rgba(224, 86, 36, 0.3) !important;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #e05624 0%, #d94e1f 100%) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
        box-shadow: 0 4px 12px rgba(224, 86, 36, 0.3) !important;
        width: 100% !important;
        padding: 0.75rem !important;
    }
    </style>
    
    <div class="marge-header">
        <div class="marge-title">🏹 M.A.R.G.E.</div>
        <div class="marge-subtitle">Multimodal Automated Real-time Guardian Engine</div>
        <div class="marge-essence">✨ The Equity Guardian — Thought Guidance & Algorithmic Protection ✨</div>
    </div>
""",
    unsafe_allow_html=True,
)

# --- PYDANTIC VALIDATION MODELS ---
class PillarEvaluation(BaseModel):
    pillar_name: str
    severity_score: float = Field(..., ge=0.0, le=1.0)
    issue_identified: str
    detailed_explanation: str
    active_remedy: str
    collaborative_rationale: str

class MARGEEvaluationPayload(BaseModel):
    original_text: str
    remediated_text: str
    guardian_index: int = Field(..., ge=0, le=100)
    degradation_tier: str = Field(default="Tier 1: Full Deep Inspection")
    violations: List[PillarEvaluation] = Field(default_factory=list)

# --- IN-PAGE CONTROL PANEL ---
st.markdown("<div class='control-panel'>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #ffb800; margin-top: 0;'>🏹 Guardian Portal & Controls</h4>", unsafe_allow_html=True)

col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1, 1, 1])

with col_ctrl1:
    raw_handle = st.text_input("Your Name / Handle", value="Pocketdoc")
    formatted_handle = raw_handle.strip() if raw_handle.strip() else "Guardian"
    display_name = f"Dr. {formatted_handle}" if not formatted_handle.startswith("Dr.") and "pocketdoc" in formatted_handle.lower() else formatted_handle

with col_ctrl2:
    page_selection = st.selectbox("Navigation View", ["🔍 Audit Console", "🏛️ Five-Pillar Taxonomy", "📖 System Guide"])

with col_ctrl3:
    enable_ai_to_ai = st.toggle("AI-to-AI Interceptor", value=True)

# Conditional Audit Parameters
scan_mode = "Initial Scan"
input_preset = "Custom Text Entry"

if page_selection == "🔍 Audit Console":
    st.markdown("---")
    col_sub1, col_sub2 = st.columns(2)
    with col_sub1:
        scan_mode = st.radio("Scan Depth", ["Initial Scan", "Deep Intersectional Scan"], horizontal=True)
    with col_sub2:
        input_preset = st.selectbox("Input Type / Preset Example", ["Custom Text Entry", "HR Policy Sample", "AI-to-AI Intercept Stream"])

st.markdown("</div>", unsafe_allow_html=True)

# --- TAXONOMY DEFINITIONS ---
FIVE_PILLARS = {
    "Pillar 1: Stereotypical & Demographic Framing": "Catches automated assumptions of roles or capabilities based on demographic generalizations.",
    "Pillar 2: Intersectional Microaggressions": "Flags subtle slights, exclusionary phrasing, and dog-whistles targeting compounded identity vectors.",
    "Pillar 3: Disability & Accessibility Justice": "Audits systems for ableist assumptions, inaccessible defaults, and systemic erasure of accommodations.",
    "Pillar 4: Structural, Spatial & Economic Erasure": "Detects when optimization models ignore localized infrastructure or socio-economic realities.",
    "Pillar 5: Dialectal & Cultural Justice": "Protects AAVE, regional dialects, and cultural vernacular against false-positive aggression flags.",
}

# --- AUDIT ENGINE WITH GRADUAL DEGRADATION ---
async def async_marge_audit(target_text: str, scan_type: str) -> MARGEEvaluationPayload:
    await asyncio.sleep(0.4)
    violations = []
    remediated = target_text
    lower = target_text.lower()
    active_tier = "Tier 1: Full Deep Inspection"

    try:
        if any(p in lower for p in ["inner city", "those people", "unusually articulate"]):
            violations.append(
                PillarEvaluation(
                    pillar_name="Pillar 1: Stereotypical & Demographic Framing",
                    severity_score=0.85,
                    issue_identified="Geographic proxy used to subtly condition capacity expectations.",
                    detailed_explanation="Coupling geographic or demographic markers with capability words introduces subconscious evaluation bias.",
                    active_remedy="Candidates demonstrate exceptional technical strategy and cross-functional leadership capabilities.",
                    collaborative_rationale="By dissolving geographic proxies and backhanded praise, we elevate the candidate to their true operational brilliance."
                )
            )
            remediated = remediated.replace("Some folks from the inner city are just not cut out for tech leadership;", "Candidates demonstrate exceptional technical strategy and cross-functional leadership capabilities;")
            remediated = remediated.replace("The candidate from the inner city is unusually articulate for this role.", "The candidate demonstrates exceptional technical communication and leadership competency.")

        if any(p in lower for p in ["aggressive", "bossy", "so articulate"]):
            violations.append(
                PillarEvaluation(
                    pillar_name="Pillar 2: Intersectional Microaggressions",
                    severity_score=0.7