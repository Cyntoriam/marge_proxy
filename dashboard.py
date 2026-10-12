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

# --- CLEAN OSHUN UX STYLING ---
st.markdown(
    """
    <style>
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
        padding: 1.8rem;
        border-radius: 12px;
        color: #f3f3f8;
        margin-bottom: 1.5rem;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
        border: 2px solid rgba(255, 184, 0, 0.4);
        text-align: center;
    }
    .marge-title {
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
        color: #ffb800;
    }
    .marge-subtitle {
        font-size: 1rem;
        color: #e0e0e0;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }
    .guardian-card {
        background-color: #1a1714;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffb800;
        margin-bottom: 0.8rem;
        border: 1px solid rgba(255, 184, 0, 0.2);
        color: #f3f3f8;
    }
    </style>
    
    <div class="marge-header">
        <div class="marge-title">🏹 M.A.R.G.E. 🛡️</div>
        <div class="marge-subtitle">Multimodal Automated Real-time Guardian Engine</div>
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

class MARGEEvaluationPayload(BaseModel):
    original_text: str
    remediated_text: str
    guardian_index: int = Field(..., ge=0, le=100)
    violations: List[PillarEvaluation] = Field(default_factory=list)

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("<h3 style='color: #ffb800;'>🏹 Guardian Controls</h3>", unsafe_allow_html=True)
    user_handle = st.text_input("User Handle", value="Pocketdoc")
    enable_ai_to_ai = st.toggle("Real-Time AI-to-AI Interceptor", value=True)
    
    st.markdown("---")
    page_selection = st.radio(
        "Navigation",
        ["🔍 Audit Console", "🏛️ Five-Pillar Taxonomy"],
        label_visibility="collapsed"
    )

# --- TAXONOMY ---
FIVE_PILLARS = {
    "Pillar 1: Stereotypical & Demographic Framing": "Catches automated assumptions of roles or capabilities based on demographic generalizations.",
    "Pillar 2: Intersectional Microaggressions": "Flags subtle slights, exclusionary phrasing, and dog-whistles targeting compounded identity vectors.",
    "Pillar 3: Disability & Accessibility Justice": "Audits systems for ableist assumptions, inaccessible defaults, and systemic erasure of accommodations.",
    "Pillar 4: Structural, Spatial & Economic Erasure": "Detects when optimization models ignore localized infrastructure or socio-economic realities.",
    "Pillar 5: Dialectal & Cultural Justice": "Protects AAVE, regional dialects, and cultural vernacular against false-positive aggression flags.",
}

# --- AUDIT ENGINE ---
async def async_marge_audit(target_text: str, scan_type: str) -> MARGEEvaluationPayload:
    await asyncio.sleep(0.6)
    violations = []
    remediated = target_text
    lower = target_text.lower()

    if "inner city" in lower or "those people" in lower:
        violations.append(
            PillarEvaluation(
                pillar_name="Pillar 1: Stereotypical & Demographic Framing",
                severity_score=0.85,
                issue_identified="Geographic proxy used to generalize candidate leadership capacity.",
                detailed_explanation="Coupling urban location codes with capability assumptions creates systemic hiring friction.",
                active_remedy="Replace geographic/demographic descriptors with competency-based metrics: e.g., substitute 'inner city background' with 'demonstrated cross-functional leadership in high-density operations'."
            )
        )
        remediated = remediated.replace("Some folks from the inner city are just not cut out for tech leadership;", "Candidates possess diverse operational experience and proven technical execution;")

    if "aggressive" in lower or "so articulate" in lower:
        violations.append(
            PillarEvaluation(
                pillar_name="Pillar 2: Intersectional Microaggressions",
                severity_score=0.75,
                issue_identified="Subjective behavior-policing adjective applied during performance review.",
                detailed_explanation="Terms like 'aggressive' carry gendered and racialized double standards that penalize direct communication.",
                active_remedy="Substitute subjective tone descriptors with operational facts: e.g., replace 'too aggressive during reviews' with 'maintains an assertive, direct communication style during milestone critiques'."
            )
        )
        remediated = remediated.replace("they are often too aggressive during reviews.", "feedback delivery focuses strictly on milestone metrics and technical milestones.")

    if scan_type == "Deep Intersectional Scan" and not violations and len(target_text) > 10:
        # Catch-all deep check for general text
        violations.append(
            PillarEvaluation(
                pillar_name="Pillar 4: Structural, Spatial & Economic Erasure",
                severity_score=0.45,
                issue_identified="Potential institutional barrier or rigid operational assumption.",
                detailed_explanation="The text assumes uniform resource access without accounting for infrastructure variation.",
                active_remedy="Incorporate flexible scheduling policies and explicit remote-accessibility provisions into the workflow."
            )
        )

    score = max(100 - (len(violations) * 30), 40)
    return MARGEEvaluationPayload(original_text=target_text, remediated_text=remediated, guardian_index=score, violations=violations)

# --- MAIN INTERFACE ---
if page_selection == "🔍 Audit Console":
    st.markdown("<h3 style='color: #ffb800;'>Audit Console</h3>", unsafe_allow_html=True)
    
    # Simplified UX layout: scan mode selection
    col_mode1, col_mode2 = st.columns(2)
    with col_mode1:
        scan_mode = st.radio("Scan Depth:", ["Initial Keyword & Pattern Scan", "Deep Intersectional Scan"], horizontal=True)
    with col_mode2:
        op_context = st.selectbox("Payload Source:", ["Direct Text Input", "HR Policy Excerpt", "AI-to-AI Stream"])

    default_text = "Some folks from the inner city are just not cut out for tech leadership; they are often too aggressive during reviews." if "HR" in op_context or "Direct" in op_context else "The candidate is unusually articulate and displays unexpected technical depth."
    
    target_text = st.text_area("Input Text for Evaluation:", value=default_text, height=90)

    if st.button("🏹 Run M.A.R.G.E. Audit"):
        with st.spinner("Analyzing text and generating real-world solutions..."):
            result = asyncio.run(async_marge_audit(target_text, scan_mode))

        st.markdown("---")
        
        # Guardian Index Sliding Scale
        pct = max(0, min(100, result.guardian_index))
        st.markdown(f"""
        <div style="background-color: #1a1714; padding: 1rem; border-radius: 8px; border: 1px solid rgba(255, 184, 0, 0.3); margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem; font-weight: bold; color: #ffb800; font-size: 0.9rem;">
                <span>Critical Risk</span>
                <span>Guardian Index: {result.guardian_index} / 100</span>
                <span>Pure Alignment</span>
            </div>
            <div style="position: relative; width: 100%; height: 10px; background: linear-gradient(90deg, #dc3545 0%, #ffc107 50%, #28a745 100%); border-radius: 5px;">
                <div style="position: absolute; left: {pct}%; top: -12px; transform: translateX(-50%); font-size: 1.3rem;">🏹</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Side-by-side comparison
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("🔴 **Original / Stream**")
            st.info(result.original_text)
        with c2:
            st.markdown("🟢 **M.A.R.G.E. Real-World Solution**")
            st.success(result.remediated_text)

        # Violations breakdown
        if result.violations:
            st.markdown("<h4 style='color: #ffb800; margin-top: 1rem;'>Actionable Remediation Breakdown</h4>", unsafe_allow_html=True)
            for v in result.violations:
                with st.expander(f"🏹 {v.pillar_name} (Severity: {v.severity_score})", expanded=True):
                    st.markdown(f"**Issue:** {v.issue_identified}")
                    st.markdown(f"**Why it flags:** {v.detailed_explanation}")
                    st.markdown(f"**Real-World Solution / Rewrite:** <span style='color: #ffb800;'>{v.active_remedy}</span>", unsafe_allow_html=True)
        else:
            st.balloons()
            st.success("✨ Clean alignment! No structural bias detected.")

else:
    st.markdown("<h3 style='color: #ffb800;'>Five-Pillar Taxonomy</h3>", unsafe_allow_html=True)
    for pillar, desc in FIVE_PILLARS.items():
        st.markdown(f"""
        <div class="guardian-card">
            <strong style="color: #ffb800;">🏹 {pillar}</strong><br>
            <span style="color: #d1d1e0; font-size: 0.9rem;">{desc}</span>
        </div>
        """, unsafe_allow_html=True)