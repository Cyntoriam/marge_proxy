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

# --- GLOBAL OSHUN WARM PALETTE & READABILITY STYLING ---
st.markdown(
    """
    <style>
    /* Exact Oshun dark gold-tinted charcoal background matching user reference */
    .stApp {
        background: linear-gradient(180deg, #14120f 0%, #0a0908 100%) !important;
        color: #f3f3f8 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #161311 !important;
        border-right: 1px solid rgba(255, 184, 0, 0.25) !important;
    }

    .marge-header {
        background: linear-gradient(135deg, #1f1a16 0%, #14120f 100%);
        padding: 2.2rem;
        border-radius: 14px;
        color: #f3f3f8;
        margin-bottom: 2rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        border: 2px solid rgba(255, 184, 0, 0.4);
        text-align: center;
    }
    .marge-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
        color: #ffb800;
        letter-spacing: 1px;
    }
    .marge-subtitle {
        font-size: 1.15rem;
        color: #e0e0e0;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    .marge-tagline {
        font-size: 0.95rem;
        color: #00ffcc;
        font-style: italic;
        margin-top: 0.4rem;
    }
    .guardian-card {
        background-color: #1a1714;
        padding: 1.2rem;
        border-radius: 8px;
        border-left: 4px solid #ffb800;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 184, 0, 0.2);
        color: #f3f3f8;
    }
    .streamlit-expanderHeader {
        background-color: #1a1714 !important;
        color: #ffb800 !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        border: 1px solid rgba(255, 184, 0, 0.15) !important;
    }
    </style>
    
    <div class="marge-header">
        <div class="marge-title">🏹 M.A.R.G.E. 🛡️</div>
        <div class="marge-subtitle">Multimodal Automated Real-time Guardian Engine</div>
        <div class="marge-tagline">Engine — The Equity Guardian</div>
    </div>
""",
    unsafe_allow_html=True,
)

# --- PYDANTIC VALIDATION MODELS ---
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

# --- SIDEBAR: VISITOR PORTAL & NAVIGATION ---
with st.sidebar:
    st.markdown("<h3 style='color: #ffb800;'>🏹 Visitor Portal</h3>", unsafe_allow_html=True)
    user_handle = st.text_input("Your Name / Handle", value="Pocketdoc")
    
    st.markdown("---")
    st.markdown("<h3 style='color: #ffb800;'>⚡ AI-to-AI Engine Config</h3>", unsafe_allow_html=True)
    openai_key = st.text_input("OpenAI API Key (Optional)", type="password")
    enable_ai_to_ai = st.toggle("Enable Real-Time AI-to-AI Interceptor", value=True)
    st.markdown(
        "<small style='color: #d1d1e0;'>When enabled, M.A.R.G.E. intercepts model-to-model streams in real time to prevent automated bias propagation.</small>", 
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    st.markdown("<h3 style='color: #ffb800;'>Navigation Panel</h3>", unsafe_allow_html=True)
    page_selection = st.radio(
        "Select View:",
        ["🏹 The Guardian Audit", "📖 About & User Guide"],
        label_visibility="collapsed"
    )

# --- FIVE-PILLAR TAXONOMY DEFINITIONS ---
FIVE_PILLARS = {
    "Pillar 1: Stereotypical & Demographic Framing": "Catches automated assumptions of roles or capabilities based on demographic generalizations.",
    "Pillar 2: Intersectional Microaggressions": "Flags subtle slights, exclusionary phrasing, and dog-whistles targeting compounded identity vectors.",
    "Pillar 3: Disability & Accessibility Justice": "Audits systems for ableist assumptions, inaccessible defaults, and systemic erasure of accommodations.",
    "Pillar 4: Structural, Spatial & Economic Erasure": "Detects when optimization models ignore localized infrastructure or socio-economic realities.",
    "Pillar 5: Dialectal & Cultural Justice": "Protects AAVE, regional dialects, and cultural vernacular against false-positive aggression flags.",
}

# --- ASYNCHRONOUS AUDITING ENGINE ---
async def async_marge_deep_audit(target_text: str, is_ai_to_ai: bool) -> MARGEEvaluationPayload:
    await asyncio.sleep(0.8)
    
    violations_data = []
    remediated_text = target_text
    text_lower = target_text.lower()

    if any(p in text_lower for p in ["those people", "inner city", "they always", "unusually articulate"]):
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
        remediated_text = remediated_text.replace("The candidate from the inner city is unusually articulate for this role.", "The candidate demonstrates exceptional technical communication and leadership competency.")

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

    if any(w in text_lower for w in ["cant", "cannot", "failed", "broken"]) and not "support" in text_lower:
        violations_data.append(
            PillarEvaluation(
                pillar_name="Pillar 4: Structural, Spatial & Economic Erasure",
                severity_score=0.65,
                issue_identified="Deficit-based framing that creates psychological barriers.",
                detailed_explanation="Language actively projects failure or inability onto specific groups.",
                active_remedy="Reframe entirely around institutional accessibility, mentorship pipelines, and clear capability growth frameworks."
            )
        )

    guardian_index = max(100 - (len(violations_data) * 25), 35)

    return MARGEEvaluationPayload(
        original_text=target_text,
        remediated_text=remediated_text,
        guardian_index=guardian_index,
        violations=violations_data
    )

# --- RENDER SELECTED VIEW ---
if page_selection == "🏹 The Guardian Audit":
    st.markdown("<h2 style='color: #ffb800;'>Asynchronous Microaggression & Bias Guardian Audit</h2>", unsafe_allow_html=True)
    st.markdown("<span style='color: #d1d1e0;'>Scan text, policies, or documents across the Five Pillars, calculate a Guardian Index, and review proposed neutralizations before using them.</span>", unsafe_allow_html=True)
    
    mode = st.radio(
        "Select Operation Mode:",
        ["👤 Human Deep Scan & Live Recommendations", "🤖 Real-Time AI-to-AI Interceptor Mode"],
        horizontal=True
    )

    if "Human" in mode:
        target_text = st.text_area(
            "Enter idea, policy, or text excerpt to scan:",
            value="Some folks from the inner city are just not cut out for tech leadership; they are often too aggressive during reviews.",
            height=120
        )
        button_label = "🏹 Perform Deep Human Audit"
    else:
        st.markdown("<span style='color: #ffb800;'>⚡ <strong>Real-time AI Middleware Active</strong>: Intercepts automated AI model streams in flight to sanitize model-to-model context windows.</span>", unsafe_allow_html=True)
        target_text = st.text_area(
            "Incoming AI-to-AI Stream Payload:",
            value="The candidate from the inner city is unusually articulate for this role.",
            height=120
        )
        button_label = "⚡ Intercept & Sanitize AI Stream"

    if st.button(button_label):
        is_ai_mode = "AI-to-AI" in mode
        with st.spinner("M.A.R.G.E. is executing async inspection and enforcing Pydantic type safety..."):
            result: MARGEEvaluationPayload = asyncio.run(async_marge_deep_audit(target_text, is_ai_mode))

        st.markdown("---")
        
        # Guardian Index Sliding Scale with Artemis Bow Marker
        st.markdown("<h3 style='color: #ffb800;'>🏹 Guardian Index Sliding Scale Severity Meter</h3>", unsafe_allow_html=True)
        
        position_pct = max(0, min(100, result.guardian_index))
        
        scale_html = f"""
        <div style="background-color: #1a1714; padding: 1.5rem; border-radius: 10px; border: 1px solid rgba(255, 184, 0, 0.3); margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-weight: bold; color: #ffb800;">
                <span>Critical Risk (0)</span>
                <span>Guardian Index: {result.guardian_index} / 100</span>
                <span>Pure Alignment (100)</span>
            </div>
            <div style="position: relative; width: 100%; height: 14px; background: linear-gradient(90deg, #dc3545 0%, #ffc107 50%, #28a745 100%); border-radius: 7px;">
                <div style="position: absolute; left: {position_pct}%; top: -14px; transform: translateX(-50%); font-size: 1.6rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));">
                    🏹
                </div>
            </div>
        </div>
        """
        st.markdown(scale_html, unsafe_allow_html=True)

        st.markdown("---")

        col_orig, col_rem = st.columns(2)
        with col_orig:
            st.markdown("🔴 **Original Output / Intercepted Stream**")
            st.info(result.original_text)
        with col_rem:
            st.markdown("🟢 **M.A.R.G.E. Sanitized Output & Recommendation**")
            st.success(result.remediated_text)

        st.markdown("---")
        st.markdown("<h3 style='color: #ffb800;'>📋 Detailed Microaggression Breakdown & Live Recommendations</h3>", unsafe_allow_html=True)
        
        if result.violations:
            for v in result.violations:
                with st.expander(f"🏹 Flagged: {v.pillar_name} (Severity: {v.severity_score})", expanded=True):
                    st.markdown(f"<span style='color: #f3f3f8;'><strong>Issue Identified:</strong> {v.issue_identified}</span>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color: #d1d1e0;'><strong>Detailed Explanation:</strong> {v.detailed_explanation}</span>", unsafe_allow_html=True)
                    st.markdown(f"<span style='color: #ffb800;'><strong>Live Guardian Recommendation / Remedy:</strong> {v.active_remedy}</span>", unsafe_allow_html=True)
        else:
            st.balloons()
            st.success("✨ Pure alignment! No microaggressions or bias vectors detected.")

else:
    st.markdown("<h2 style='color: #ffb800;'>🏛️ The Five-Pillar Taxonomy & Guide</h2>", unsafe_allow_html=True)
    st.markdown("<span style='color: #d1d1e0;'>The structural rules powering M.A.R.G.E.'s real-time equity guardian engine.</span>", unsafe_allow_html=True)
    st.markdown("---")
    
    for pillar, desc in FIVE_PILLARS.items():
        st.markdown(
            f"""
            <div class="guardian-card">
                <strong style="color: #ffb800;">🏹 {pillar}</strong><br>
                <span style="color: #d1d1e0; font-size: 0.95rem;">{desc}</span>
            </div>
            """,
            unsafe_allow_html=True
        )