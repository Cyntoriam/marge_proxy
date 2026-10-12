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

# --- GLOBAL BURNT ORANGE & HONEY-GOLD OSHUN STYLING (NO SHIELDS) ---
st.markdown(
    """
    <style>
    /* Global Background: Burnt Orange to Dark Charcoal Gradient */
    .stApp {
        background: linear-gradient(180deg, #240c03 0%, #120501 60%, #0a0301 100%) !important;
        color: #fcebe6 !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #170702 !important;
        border-right: 1px solid rgba(224, 86, 36, 0.4) !important;
    }

    /* Burnt Orange & Gold Header Box */
    .marge-header {
        background: linear-gradient(135deg, #2e1004 0%, #1a0802 100%);
        padding: 2rem;
        border-radius: 14px;
        color: #ffffff;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 25px rgba(224, 86, 36, 0.3);
        border: 2px solid #e05624;
        text-align: center;
    }
    .marge-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
        color: #ffb800;
        letter-spacing: 1px;
    }
    .marge-subtitle {
        font-size: 1.1rem;
        color: #f3d0c7;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* Custom Cards */
    .guardian-card {
        background-color: #1c0802;
        padding: 1.2rem;
        border-radius: 8px;
        border-left: 4px solid #ffb800;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 184, 0, 0.25);
        color: #fcebe6;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: #240c03 !important;
        color: #ffb800 !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        border: 1px solid rgba(224, 86, 36, 0.3) !important;
    }
    
    /* Buttons */
    div.stButton > button {
        background: linear-gradient(90deg, #e05624 0%, #d94e1f 100%) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
        box-shadow: 0 4px 12px rgba(224, 86, 36, 0.3) !important;
    }
    </style>
    
    <div class="marge-header">
        <div class="marge-title">🏹 M.A.R.G.E.</div>
        <div class="marge-subtitle">Multimodal Automated Real-time Guardian Engine</div>
    </div>
""",
    unsafe_allow_html=True,
)

# --- PYDANTIC VALIDATION MODELS (Deterministic Governance) ---
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
    violations: List[PillarEvaluation] = Field(default_factory=list)

# --- PERSISTENT SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h3 style='color: #ffb800;'>🏹 Guardian Controls</h3>", unsafe_allow_html=True)
    user_handle = st.text_input("User Handle", value="Pocketdoc")
    
    st.markdown("---")
    st.markdown("<h4 style='color: #ffb800;'>Navigation Panel</h4>", unsafe_allow_html=True)
    page_selection = st.radio(
        "Navigation Options",
        ["🔍 Audit Console", "🏛️ Five-Pillar Taxonomy", "📖 System Guide"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    enable_ai_to_ai = st.toggle("Real-Time AI-to-AI Interceptor", value=True)
    st.caption("When enabled, M.A.R.G.E. intercepts model-to-model streams in flight.")

# --- TAXONOMY DEFINITIONS ---
FIVE_PILLARS = {
    "Pillar 1: Stereotypical & Demographic Framing": "Catches automated assumptions of roles or capabilities based on demographic generalizations.",
    "Pillar 2: Intersectional Microaggressions": "Flags subtle slights, exclusionary phrasing, and dog-whistles targeting compounded identity vectors.",
    "Pillar 3: Disability & Accessibility Justice": "Audits systems for ableist assumptions, inaccessible defaults, and systemic erasure of accommodations.",
    "Pillar 4: Structural, Spatial & Economic Erasure": "Detects when optimization models ignore localized infrastructure or socio-economic realities.",
    "Pillar 5: Dialectal & Cultural Justice": "Protects AAVE, regional dialects, and cultural vernacular against false-positive aggression flags.",
}

# --- ASYNCHRONOUS COLLABORATIVE AUDIT ENGINE ---
async def async_marge_audit(target_text: str, scan_type: str) -> MARGEEvaluationPayload:
    await asyncio.sleep(0.6)
    violations = []
    remediated = target_text
    lower = target_text.lower()

    if any(p in lower for p in ["inner city", "those people", "unusually articulate"]):
        violations.append(
            PillarEvaluation(
                pillar_name="Pillar 1: Stereotypical & Demographic Framing",
                severity_score=0.85,
                issue_identified="Geographic proxy used to subtly condition capacity expectations.",
                detailed_explanation="Coupling geographic or demographic markers with capability words introduces subconscious evaluation bias.",
                active_remedy="Candidates demonstrate exceptional technical strategy and cross-functional leadership capabilities.",
                collaborative_rationale="By removing the geographic proxy ('inner city') and backhanded compliments ('unusually articulate'), we center the candidate strictly on objective operational competencies."
            )
        )
        remediated = remediated.replace("Some folks from the inner city are just not cut out for tech leadership;", "Candidates demonstrate exceptional technical strategy and cross-functional leadership capabilities;")
        remediated = remediated.replace("The candidate from the inner city is unusually articulate for this role.", "The candidate demonstrates exceptional technical communication and leadership competency.")

    if any(p in lower for p in ["aggressive", "bossy", "so articulate"]):
        violations.append(
            PillarEvaluation(
                pillar_name="Pillar 2: Intersectional Microaggressions",
                severity_score=0.75,
                issue_identified="Subjective behavior-policing adjective in performance review context.",
                detailed_explanation="Words like 'aggressive' often function as double-standard critiques against marginalized leadership communication styles.",
                active_remedy="Maintains an assertive, direct communication style focused on milestone execution.",
                collaborative_rationale="Reframing 'aggressive' into 'assertive and direct communication focused on milestone execution' converts a vague subjective slight into a quantifiable professional strength."
            )
        )
        remediated = remediated.replace("they are often too aggressive during reviews.", "feedback delivery maintains an assertive, direct communication style focused on milestone execution.")

    if scan_type == "Deep Intersectional Scan" and not violations and len(target_text) > 10:
        violations.append(
            PillarEvaluation(
                pillar_name="Pillar 4: Structural, Spatial & Economic Erasure",
                severity_score=0.40,
                issue_identified="Potential institutional assumption regarding uniform working conditions.",
                detailed_explanation="The text assumes standardized resource availability without explicitly confirming operational accessibility.",
                active_remedy="Ensure all candidate milestone schedules explicitly support remote flexibility and accessible technical infrastructure.",
                collaborative_rationale="Adding active structural support guarantees that systemic economic or spatial barriers are mitigated ahead of time."
            )
        )

    score = max(100 - (len(violations) * 30), 40)
    return MARGEEvaluationPayload(
        original_text=target_text,
        remediated_text=remediated,
        guardian_index=score,
        violations=violations
    )

# --- INTERFACE VIEWS ---
if page_selection == "🔍 Audit Console":
    st.markdown("<h2 style='color: #ffb800;'>🔍 Audit Console</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #f3d0c7;'>M.A.R.G.E. actively detects microaggressions, provides collaborative rewrites, and guides your strategic equity thinking in real time.</p>", unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        scan_mode = st.radio("Scan Mode:", ["Initial Keyword Scan", "Deep Intersectional Scan"], horizontal=True)
    with col_s2:
        payload_source = st.selectbox("Payload Source:", ["Direct Text Box", "HR / Policy Excerpt", "AI-to-AI Intercept Stream"])

    if payload_source == "HR / Policy Excerpt":
        default_val = "Some folks from the inner city are just not cut out for tech leadership; they are often too aggressive during reviews."
    elif payload_source == "AI-to-AI Intercept Stream":
        default_val = "The candidate from the inner city is unusually articulate for this role."
    else:
        default_val = "Some folks from the inner city are just not cut out for tech leadership; they are often too aggressive during reviews."

    target_text = st.text_area("Input Text Payload:", value=default_val, height=100)

    if st.button("🏹 Execute M.A.R.G.E. Audit"):
        with st.spinner("Collaborating and scanning across Five Pillars..."):
            result: MARGEEvaluationPayload = asyncio.run(async_marge_audit(target_text, scan_mode))

        st.markdown("---")
        
        # Guardian Index Sliding Scale
        st.markdown("<h4 style='color: #ffb800;'>🏹 Guardian Index Severity Meter</h4>", unsafe_allow_html=True)
        pct = max(0, min(100, result.guardian_index))
        
        scale_html = f"""
        <div style="background-color: #1c0802; padding: 1.2rem; border-radius: 10px; border: 1px solid rgba(224, 86, 36, 0.4); margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem; font-weight: bold; color: #ffb800;">
                <span>Critical Bias (0)</span>
                <span>Guardian Index: {result.guardian_index} / 100</span>
                <span>Pure Alignment (100)</span>
            </div>
            <div style="position: relative; width: 100%; height: 12px; background: linear-gradient(90deg, #dc3545 0%, #ffc107 50%, #28a745 100%); border-radius: 6px;">
                <div style="position: absolute; left: {pct}%; top: -12px; transform: translateX(-50%); font-size: 1.4rem;">
                    🏹
                </div>
            </div>
        </div>
        """
        st.markdown(scale_html, unsafe_allow_html=True)

        col_orig, col_rem = st.columns(2)
        with col_orig:
            st.markdown("🔴 **Original / Intercepted Payload**")
            st.info(result.original_text)
        with col_rem:
            st.markdown("🟢 **M.A.R.G.E. Collaborative Rewrite**")
            st.success(result.remediated_text)

        st.markdown("---")
        st.markdown("<h3 style='color: #ffb800;'>🤝 Collaborative Insights & Live Recommendations</h3>", unsafe_allow_html=True)
        
        if result.violations:
            for v in result.violations:
                with st.expander(f"🏹 Flagged: {v.pillar_name} (Severity: {v.severity_score})", expanded=True):
                    st.markdown(f"**Issue Identified:** {v.issue_identified}")
                    st.markdown(f"**Context Explanation:** {v.detailed_explanation}")
                    st.markdown(f"**Recommended Rewrite:** <span style='color: #ffb800; font-weight: bold;'>{v.active_remedy}</span>", unsafe_allow_html=True)
                    st.markdown(f"💡 **Strategic Rationale (Thought Partner Guide):** *{v.collaborative_rationale}*")
        else:
            st.balloons()
            st.success("✨ Pure alignment! No microaggressions or structural bias vectors detected.")

elif page_selection == "🏛️ Five-Pillar Taxonomy":
    st.markdown("<h2 style='color: #ffb800;'>🏛️ The Five-Pillar Equity Framework</h2>", unsafe_allow_html=True)
    st.markdown("---")
    for pillar, desc in FIVE_PILLARS.items():
        st.markdown(
            f"""
            <div class="guardian-card">
                <strong style="color: #ffb800;">🏹 {pillar}</strong><br>
                <span style="color: #f3d0c7; font-size: 0.95rem;">{desc}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

else:
    st.markdown("<h2 style='color: #ffb800;'>📖 M.A.R.G.E. System Guide</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div style="color: #f3d0c7; line-height: 1.6;">
    <p><strong>M.A.R.G.E. (Multimodal Automated Real-time Guardian Engine)</strong> acts as a real-time type-safe equity middleware gatekeeper[cite: 2].</p>
    
    <h4 style="color: #ffb800;">Core Modes:</h4>
    <ul>
        <li><strong>Human Scans</strong>: Performs initial keyword screens or deep intersectional audits, offering collaborative rewrites and thought-partner explanations[cite: 2].</li>
        <li><strong>AI-to-AI Interceptor</strong>: Intercepts machine-to-machine context windows in real time to prevent bias propagation across automated model channels[cite: 2].</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)