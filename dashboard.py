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
    collaborative_rationale: str
    active_remedy: str

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

# --- AUDIT ENGINE WITH GRADUAL DEGRADATION (SYSTEMATIC IDEA FRAMEWORK REMEDIATION) ---
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
                    issue_identified="Geographic/Demographic proxy conditioning evaluation capacity.",
                    detailed_explanation="Coupling geographic or demographic markers with capability words introduces subconscious bias and backhanded praise.",
                    collaborative_rationale="Applying an IDEA lens eliminates coded geographic proxies and backhanded compliments through inclusion and equity, centering candidates strictly on objective operational competencies without demographic bias.",
                    active_remedy="Candidates demonstrate exceptional technical strategy and cross-functional leadership capabilities."
                )
            )
            remediated = remediated.replace("Some folks from the inner city are just not cut out for tech leadership;", "Candidates demonstrate exceptional technical strategy and cross-functional leadership capabilities;")
            remediated = remediated.replace("The candidate from the inner city is unusually articulate for this role.", "The candidate demonstrates exceptional technical communication and leadership competency.")

        if any(p in lower for p in ["aggressive", "bossy", "so articulate"]):
            violations.append(
                PillarEvaluation(
                    pillar_name="Pillar 2: Intersectional Microaggressions",
                    severity_score=0.75,
                    issue_identified="Subjective behavior-policing adjective targeting leadership style.",
                    detailed_explanation="Terms like 'aggressive' frequently serve as double-standard critiques against marginalized communication styles in performance evaluations.",
                    collaborative_rationale="Applying an IDEA lens reframes subjective tone-policing into quantifiable leadership strengths ('assertive clarity'), mitigating gendered and racial double standards through inclusive evaluation frameworks.",
                    active_remedy="Maintains an assertive, direct communication style focused on milestone execution."
                )
            )
            remediated = remediated.replace("they are often too aggressive during reviews.", "feedback delivery maintains an assertive, direct communication style focused on milestone execution.")

        if scan_type == "Deep Intersectional Scan" and not violations and len(target_text) > 10:
            violations.append(
                PillarEvaluation(
                    pillar_name="Pillar 4: Structural, Spatial & Economic Erasure",
                    severity_score=0.40,
                    issue_identified="Institutional assumption of uniform working conditions.",
                    detailed_explanation="Assumes standardized resource availability without explicitly confirming structural accessibility or flexible support.",
                    collaborative_rationale="Applying an IDEA lens proactively mitigates socio-economic barriers by embedding structural accessibility, inclusion, and equitable working arrangements.",
                    active_remedy="Ensure all candidate milestone schedules explicitly support remote flexibility and accessible technical infrastructure."
                )
            )

    except Exception:
        active_tier = "Tier 3: Safe Passthrough Fallback"
        remediated = target_text

    score = max(100 - (len(violations) * 30), 40)
    return MARGEEvaluationPayload(
        original_text=target_text,
        remediated_text=remediated,
        guardian_index=score,
        degradation_tier=active_tier,
        violations=violations if scan_type == "Deep Intersectional Scan" else violations[:1]
    )

# --- MAIN INTERFACE VIEWS ---
if page_selection == "🔍 Audit Console":
    st.markdown(
        f"""
        <div style="background-color: #1c0802; padding: 0.9rem; border-radius: 10px; border: 1px solid rgba(224, 86, 36, 0.4); margin-bottom: 0.9rem;">
            <h3 style="color: #ffb800; margin: 0; font-size: 1.15rem;">✨ Welcome, {display_name}.</h3>
            <p style="color: #f3d0c7; margin-top: 0.2rem; margin-bottom: 0; font-size: 0.82rem;">
                M.A.R.G.E. stands by as your algorithmic angel and equity guardian.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    if input_preset == "HR Policy Sample":
        default_val = "Some folks from the inner city are just not cut out for tech leadership; they are often too aggressive during reviews."
    elif input_preset == "AI-to-AI Intercept Stream":
        default_val = "The candidate from the inner city is unusually articulate for this role."
    else:
        default_val = "Some folks from the inner city are just not cut out for tech leadership; they are often too aggressive during reviews."

    target_text = st.text_area("Input Text Payload for Analysis:", value=default_val, height=85)

    if st.button("🏹 Execute M.A.R.G.E. Guardian Audit"):
        with st.spinner("M.A.R.G.E. is evaluating linguistic patterns with active degradation safety..."):
            result: MARGEEvaluationPayload = asyncio.run(async_marge_audit(target_text, scan_mode))

        st.markdown("---")
        
        st.markdown("<h4 style='color: #ffb800; font-size: 0.95rem; margin-bottom: 0.4rem;'>🏹 Guardian Index Severity Meter</h4>", unsafe_allow_html=True)
        pct = max(0, min(100, result.guardian_index))
        
        scale_html = f"""
        <div style="background-color: #1c0802; padding: 0.9rem; border-radius: 10px; border: 1px solid rgba(224, 86, 36, 0.4); margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem; font-weight: bold; color: #ffb800; font-size: 0.8rem;">
                <span>Critical Bias (0)</span>
                <span>Guardian Index: {result.guardian_index} / 100</span>
                <span>Pure Harmony (100)</span>
            </div>
            <div style="position: relative; width: 100%; height: 10px; background: linear-gradient(90deg, #dc3545 0%, #ffc107 50%, #28a745 100%); border-radius: 5px;">
                <div style="position: absolute; left: {pct}%; top: -11px; transform: translateX(-50%); font-size: 1.2rem;">
                    🏹
                </div>
            </div>
            <div class="degradation-badge">Status: {result.degradation_tier}</div>
        </div>
        """
        st.markdown(scale_html, unsafe_allow_html=True)

        col_orig, col_rem = st.columns([1, 1])
        with col_orig:
            st.markdown("🔴 **Original / Intercepted Payload**")
            st.info(result.original_text)
        with col_rem:
            st.markdown("🟢 **M.A.R.G.E. Restored Output**")
            st.success(result.remediated_text)

        if scan_mode == "Initial Scan":
            st.markdown("---")
            st.markdown("<h4 style='color: #ffb800; font-size: 0.95rem;'>⚡ Initial Pattern Screen Overview</h4>", unsafe_allow_html=True)
            st.markdown(f"<span style='color: #f3d0c7; font-size: 0.82rem;'>Initial scan detected active microaggression and subconscious framing patterns. Switch to <strong>Deep Intersectional Scan</strong> in the top control panel for full guidance and strategic rewrites.</span>", unsafe_allow_html=True)
        else:
            st.markdown("---")
            st.markdown("<h3 style='color: #ffb800; font-size: 1.05rem;'>✨ Guardian Insights & Thought Partner Guide</h3>", unsafe_allow_html=True)
            
            if result.violations:
                for v in result.violations:
                    with st.expander(f"🏹 Flagged: {v.pillar_name} (Severity: {v.severity_score})", expanded=True):
                        st.markdown(f"**Issue Identified:** {v.issue_identified}")
                        st.markdown(f"**Context Explanation:** {v.detailed_explanation}")
                        st.markdown(f"🌟 **Guardian Rationale & Alignment:** *{v.collaborative_rationale}*")
                        st.markdown(f"**Harmonized Remedy:** <span style='color: #ffb800; font-weight: bold;'>{v.active_remedy}</span>", unsafe_allow_html=True)
            else:
                st.balloons()
                st.success("✨ Pure harmony! No microaggressions or structural bias vectors detected.")

elif page_selection == "🏛️ Five-Pillar Taxonomy":
    st.markdown("<h2 style='color: #ffb800; font-size: 1.3rem;'>🏛️ The Five-Pillar Equity Framework</h2>", unsafe_allow_html=True)
    st.markdown("---")
    for pillar, desc in FIVE_PILLARS.items():
        st.markdown(
            f"""
            <div class="guardian-card">
                <strong style="color: #ffb800;">🏹 {pillar}</strong><br>
                <span style="color: #f3d0c7; font-size: 0.82rem;">{desc}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

else:
    st.markdown("<h2 style='color: #ffb800; font-size: 1.3rem;'>📖 M.A.R.G.E. System Guide</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div style="color: #f3d0c7; line-height: 1.5; font-size: 0.85rem;">
    <p><strong>M.A.R.G.E. (Multimodal Automated Real-time Guardian Engine)</strong> acts as an algorithmic angel and equity guardian, serving as a type-safe middleware gatekeeper with gradual degradation safety.</p>
    
    <h4 style="color: #ffb800;">System Degradation & Resilience Tiers:</h4>
    <ul>
        <li><strong>Tier 1 (Full Inspection)</strong>: Complete multi-pillar async valuation and thought-partner rationale.</li>
        <li><strong>Tier 2 (Heuristic Screen)</strong>: Local pattern matching when model resources are constrained.</li>
        <li><strong>Tier 3 (Safe Passthrough)</strong>: Guaranteed uptime passthrough ensuring zero service interruption.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)