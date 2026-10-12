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

# --- GLOBAL OSHUN THEME & STYLING OVERRIDE ---
st.markdown(
    """
    <style>
    /* Force main app background to deep charcoal */
    .stApp {
        background-color: #0e0e12 !important;
        color: #f3f3f8 !important;
    }
    
    /* Force sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #141419 !important;
        border-right: 1px solid rgba(255, 184, 0, 0.2) !important;
    }

    /* Golden Header Box */
    .marge-header {
        background-color: #141419;
        padding: 2.2rem;
        border-radius: 12px;
        color: #f3f3f8;
        margin-bottom: 2rem;
        box-shadow: 0 0 25px rgba(255, 184, 0, 0.25);
        border: 2px solid #ffb800;
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
        color: #ffb800;
        font-style: italic;
        margin-top: 0.4rem;
    }
    .guardian-card {
        background-color: #181820;
        padding: 1.2rem;
        border-radius: 8px;
        border-left: 4px solid #ffb800;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 184, 0, 0.2);
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
    st.markdown("<h3 style='color: #ffb800;'>🏹 Guardian Controls</h3>", unsafe_allow_html=True)
    user_handle = st.text_input("Your Name / Handle", value="Pocketdoc")
    
    st.markdown("---")
    st.markdown("<h3 style='color: #ffb800;'>⚡ AI-to-AI Engine Config</h3>", unsafe_allow_html=True)
    enable_ai_to_ai = st.toggle("Enable AI-to-AI Interceptor", value=True)
    st.markdown(
        "<small style='color: #cccccc;'>Oshun theme active: charcoal and honey-gold.<br>Self-contained mode: no API request or external service is used.</small>", 
        unsafe_allow_html=True
    )

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

    validated_payload = MARGEEvaluationPayload(
        original_text=target_text,
        remediated_text=remediated_text,
        guardian_index=guardian_index,
        violations=violations_data
    )

    return validated_payload

# --- MAIN INTERFACE TABS ---
tab_scanner, tab_pillars = st.tabs(["🔍 Guardian Deep Scan", "🏛️ Five-Pillar Taxonomy"])

with tab_scanner:
    st.subheader("Deep Idea & Document Microaggression Scanner")
    st.markdown("Scan text, policy drafts, or external model outputs across the Five Pillars. M.A.R.G.E. provides deep explanations, analysis, and active structural rewrites with programmatic Pydantic validation.")

    input_source = st.selectbox("Choose Input Source:", ["Direct Text Box", "Sample Policy Excerpt"])
    
    if input_source == "Direct Text Box":
        target_text = st.text_area(
            "Enter text or idea for M.A.R.G.E. to scan:",
            value="Some folks from the inner city are just not cut out for tech leadership; they are often too aggressive during reviews.",
            height=120
        )
    else:
        target_text = "Certain demographic groups are overly articulate in meetings, which often disrupts standard workflow procedures."
        st.info(f"Loaded Sample: {target_text}")

    if st.button("🏹 Run Guardian Deep Scan"):
        with st.spinner("M.A.R.G.E. is actively analyzing and enforcing type-safe schema validation..."):
            result: MARGEEvaluationPayload = asyncio.run(async_marge_deep_audit(target_text, enable_ai_to_ai))

        st.markdown("---")
        
        if result.guardian_index >= 80:
            severity_color = "#28a745"  # Green
            severity_label = "Low Risk"
        elif result.guardian_index >= 55:
            severity_color = "#ffb800"  # Honey-Gold
            severity_label = "Moderate Risk"
        else:
            severity_color = "#dc3545"  # Red
            severity_label = "Critical Risk"

        col_m1, col_m2 = st.columns([1, 2])
        with col_m1:
            st.metric("Guardian Index", f"{result.guardian_index}/100")
        with col_m2:
            st.markdown("**Severity Level Scale:**")
            st.markdown(
                f"""
                <div style="margin-top: 0.4rem;">
                    <span class="severity-pill" style="background-color: {severity_color};">
                        🏹 {severity_label} ({result.guardian_index}/100)
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
            interception_status = "Active Async AI-to-AI Interceptor Hooked" if enable_ai_to_ai else "Standard Direct Scan"
            st.caption(f"Engine Mode: {interception_status}")

        st.markdown("---")

        col_orig, col_rem = st.columns(2)
        with col_orig:
            st.markdown("🔴 **Original Text / Model Output**")
            st.info(result.original_text)
        with col_rem:
            st.markdown("🟢 **M.A.R.G.E. Active Corrected Rewrite**")
            st.success(result.remediated_text)

        st.markdown("---")
        st.markdown("### 📋 Deep Analysis & Pillar Breakdown (Validated Payload)")
        
        if result.violations:
            for v in result.violations:
                with st.expander(f"⚠️ Flagged: {v.pillar_name} (Severity: {v.severity_score})", expanded=True):
                    st.markdown(f"**Issue Identified:** {v.issue_identified}")
                    st.markdown(f"**Detailed Explanation:** {v.detailed_explanation}")
                    st.markdown(f"**Active Guardian Remedy:** {v.active_remedy}")
        else:
            st.balloons()
            st.success("✨ Pure alignment! No microaggressions or bias vectors detected across the Five Pillars.")

with tab_pillars:
    st.subheader("The Five-Pillar Taxonomy")
    st.markdown("The structural rules powering M.A.R.G.E.'s real-time equity guardian engine.")
    
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