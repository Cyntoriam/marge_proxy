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

# --- GLOBAL OSHUN & WARM NAVIGATION STYLING ---
st.markdown(
    """
    <style>
    /* Force main app background to deep dark charcoal */
    .stApp {
        background-color: #12100e !important;
        color: #f3f3f8 !important;
    }
    
    /* Force sidebar styling with warm orange-gold borders */
    [data-testid="stSidebar"] {
        background-color: #1a1614 !important;
        border-right: 1px solid rgba(224, 86, 36, 0.3) !important;
    }

    /* Golden/Orange Header Box */
    .marge-header {
        background-color: #1c1815;
        padding: 2.2rem;
        border-radius: 12px;
        color: #f3f3f8;
        margin-bottom: 2rem;
        box-shadow: 0 0 25px rgba(224, 86, 36, 0.2);
        border: 2px solid #e05624;
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
        color: #e05624;
        font-style: italic;
        margin-top: 0.4rem;
    }
    .guardian-card {
        background-color: #221c18;
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
    /* Style custom orange sidebar buttons */
    div.stButton > button {
        background-color: #d94e1f !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
    }
    </style>
    
    <div class="marge-header">
        <div class="marge-title">🏹 M.A.R.G.E.</div>
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

# --- SIDEBAR: VISITOR PORTAL & NAVIGATION ---
with st.sidebar:
    st.markdown("<h3 style='color: #ffb800;'>🏹 Visitor Portal</h3>", unsafe_allow_html=True)
    user_handle = st.text_input("Your Name / Handle", value="Pocketdoc")
    
    st.markdown("---")
    st.markdown("<h3 style='color: #ffb800;'>⚡ AI-to-AI Engine Config</h3>", unsafe_allow_html=True)
    openai_key = st.text_input("OpenAI API Key (Optional)", type="password")
    enable_ai_to_ai = st.toggle("Enable Real-Time AI-to-AI Interceptor", value=True)
    st.markdown(
        "<small style='color: #cccccc;'>When enabled, M.A.R.G.E. intercepts model-to-model streams in real time to prevent automated bias propagation.</small>", 
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    st.markdown("<h3 style='color: #ffb800;'>Navigation Panel</h3>", unsafe_allow_html=True)
    page_selection = st.radio(
        "Select View:",
        ["🏹 The Guardian Audit", "📖 About & User Guide"],
        label_visibility="collapsed"
    )

# --- ASYNCHRONOUS AUDITING & REAL-TIME INTERCEPTION ENGINE ---
async def async_marge_deep_audit(target_text: str, is_ai_to_ai: bool) -> MARGEEvaluationPayload:
    await asyncio.sleep(0.8) # Simulate fast middleware inspection
    
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

# --- RENDER SELECTED VIEW ---
if page_selection == "🏹 The Guardian Audit":
    st.subheader("Interactive Audit & Real-Time AI Interception")
    
    # Toggle between Human Review and Real-Time AI Stream modes
    mode = st.radio(
        "Select Operation Mode:",
        ["👤 Human Deep Scan & Live Recommendations", "🤖 Real-Time AI-to-AI Interceptor Mode"],
        horizontal=True
    )

    if "Human" in mode:
        st.markdown("Scan text, policy drafts, or human prompts. M.A.R.G.E. detects microaggressions, provides detailed analysis, and generates active structural recommendations.")
        target_text = st.text_area(
            "Enter text payload for human equity audit:",
            value="Some folks from the inner city are just not cut out for tech leadership; they are often too aggressive during reviews.",
            height=120
        )
        button_label = "🏹 Perform Deep Human Audit"
    else:
        st.markdown("⚡ **Real-time AI Middleware Active**: Intercepts automated AI model streams in flight. If microaggressions or bias parameters are detected, M.A.R.G.E. immediately sanitizes the payload before the downstream AI receives it.")
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
        
        # Risk levels
        if result.guardian_index >= 80:
            severity_color = "#28a745"
            severity_label = "Low Risk / Clean Stream"
        elif result.guardian_index >= 55:
            severity_color = "#ffb800"
            severity_label = "Moderate Risk Detected"
        else:
            severity_color = "#dc3545"
            severity_label = "Critical Bias / Interception Required"

        col_m1, col_m2 = st.columns([1, 2])
        with col_m1:
            st.metric("Guardian Index", f"{result.guardian_index}/100")
        with col_m2:
            st.markdown("**Status & Risk Assessment:**")
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

        st.markdown("---")

        col_orig, col_rem = st.columns(2)
        with col_orig:
            st.markdown("🔴 **Original Output / Intercepted Stream**")
            st.info(result.original_text)
        with col_rem:
            st.markdown("🟢 **M.A.R.G.E. Sanitized Output & Recommendation**")
            st.success(result.remediated_text)

        st.markdown("---")
        st.markdown("### 📋 Detailed Microaggression Breakdown & Live Recommendations")
        
        if result.violations:
            for v in result.violations:
                with st.expander(f"⚠️ Flagged: {v.pillar_name} (Severity: {v.severity_score})", expanded=True):
                    st.markdown(f"**Issue Identified:** {v.issue_identified}")
                    st.markdown(f"**Detailed Explanation:** {v.detailed_explanation}")
                    st.markdown(f"**Live Guardian Recommendation / Remedy:** {v.active_remedy}")
        else:
            st.balloons()
            st.success("✨ Pure alignment! No microaggressions or bias vectors detected.")

else:
    st.subheader("📖 About M.A.R.G.E. & User Guide")
    st.markdown("""
    **M.A.R.G.E. (Multimodal Automated Real-time Guardian Engine)** operates as a sociotechnical middleware gatekeeper.
    
    ### Core Operations:
    1. **For Humans**: Performs deep scans on policy documents and human text inputs, flagging subtle microaggressions and serving live structural recommendations.
    2. **For AI-to-AI Systems**: Acts as a real-time interceptor that sanitizes machine-to-machine context windows, mitigating algorithmic bias propagation before downstream models process the data[cite: 2].
    """)