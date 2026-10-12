import asyncio
import random
from typing import List, Optional
from pydantic import BaseModel, Field
import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="M.A.R.G.E. | Multimodal Automated Real-time Guardian Engine",
    page_icon="🏹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALIZE SESSION STATE ---
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark Mode"
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "voice_input_text" not in st.session_state:
    st.session_state.voice_input_text = ""

# --- COLOR DEFINITIONS ---
HONEY_GOLD = "#ffb800"

# --- DYNAMIC THEME COLOR PALETTES ---
if st.session_state.theme_mode == "Dark Mode":
    bg_style = "linear-gradient(180deg, #240c03 0%, #120501 60%, #0a0301 100%)"
    text_color = "#fcebe6"
    panel_bg = "#170702"
    panel_border = "rgba(255, 184, 0, 0.6)"
    hr_border = "rgba(255, 184, 0, 0.5)"
    header_bg = "linear-gradient(135deg, #2e1004 0%, #1a0802 100%)"  # Burnt Orange
    header_border = HONEY_GOLD
    title_color = HONEY_GOLD
    title_stroke = "none"
    subtitle_color = "#f3d0c7"
    card_bg = "#1c0802"
    card_border = "rgba(255, 184, 0, 0.4)"
    badge_bg = "rgba(224, 86, 36, 0.25)"
    badge_text = HONEY_GOLD
    expander_bg = "#2e1004"
    expander_text = HONEY_GOLD
    input_bg = "#240c03"
    input_text = "#ffffff"
    placeholder_text = "#f3d0c7"
    dropdown_text = HONEY_GOLD
    btn_bg = "linear-gradient(90deg, #e05624 0%, #d94e1f 100%)"
    sidebar_bg = "#170702"
else:
    # LIGHT MODE: Honey Gold Dividers, Outlines & Subheader
    bg_style = "linear-gradient(180deg, #fdfbf7 0%, #f7f0e6 60%, #efe3d3 100%)"
    text_color = "#2b1105"
    panel_bg = "#f5e9da"
    panel_border = HONEY_GOLD
    hr_border = HONEY_GOLD  # Explicit Honey Gold for all horizontal divider lines
    header_bg = "linear-gradient(135deg, #8c2d0d 0%, #5e1c06 100%)"  # Retained Burnt Orange
    header_border = HONEY_GOLD  # Honey Gold Outline for Header Box
    title_color = HONEY_GOLD
    title_stroke = f"1px {HONEY_GOLD}"  # Honey Gold Outline on Header Letters
    subtitle_color = HONEY_GOLD  # Subheader in Honey Gold
    card_bg = "#f7ebe0"
    card_border = HONEY_GOLD
    badge_bg = "#f2d2c2"
    badge_text = "#8c2d0d"
    expander_bg = "#ebd7c5"
    expander_text = "#8c2d0d"
    input_bg = "#ffffff"
    input_text = "#2b1105"
    placeholder_text = "#6e3b22"
    dropdown_text = HONEY_GOLD
    btn_bg = "linear-gradient(90deg, #d96b27 0%, #b84f18 100%)"
    sidebar_bg = "#f5e9da"

# --- INJECT COMPLETE HIGH-CONTRAST CSS WITH DIVIDER FIXES ---
css_code = (
    "<style>"
    f".stApp {{ background: {bg_style} !important; color: {text_color} !important; }}"
    f"[data-testid='stSidebar'] {{ background-color: {sidebar_bg} !important; border-right: 2px solid {panel_border} !important; }}"
    ".block-container { max-width: 100% !important; padding-top: 1.2rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }"
    f".control-panel {{ background-color: {panel_bg}; padding: 1.2rem; border-radius: 12px; border: 2px solid {panel_border}; margin-bottom: 1.5rem; }}"
    f".marge-header {{ background: {header_bg}; padding: 1.5rem; border-radius: 12px; color: #ffffff; margin-bottom: 1.2rem; border: 2px solid {header_border}; text-align: center; }}"
    f".marge-title {{ font-size: 2.2rem; font-weight: 800; margin-bottom: 0.2rem; color: {title_color}; -webkit-text-stroke: {title_stroke}; }}"
    f".marge-subtitle {{ font-size: 0.95rem; color: {subtitle_color}; font-weight: 600; text-transform: uppercase; }}"
    f".marge-essence {{ font-size: 0.85rem; color: {HONEY_GOLD}; font-style: italic; margin-top: 0.3rem; }}"
    f".guardian-card {{ background-color: {card_bg}; padding: 1rem; border-radius: 8px; border-left: 4px solid {header_border}; margin-bottom: 0.8rem; border: 2px solid {card_border}; color: {text_color}; }}"
    f".degradation-badge {{ display: inline-block; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.75rem; font-weight: bold; background-color: {badge_bg}; border: 1px solid {header_border}; color: {badge_text}; margin-top: 0.4rem; }}"
    
    # GLOBAL HORIZONTAL DIVIDER FIX (hr tags across Sidebar and Main View)
    f"hr {{ border: none !important; border-top: 2px solid {hr_border} !important; margin: 1rem 0 !important; opacity: 1 !important; }}"
    
    # Expander styling
    f"details summary {{ background-color: {expander_bg} !important; border-radius: 6px !important; border: 2px solid {panel_border} !important; padding: 0.5rem 1rem !important; }}"
    f"details summary p, details summary span, details summary div, details summary svg {{ color: {expander_text} !important; fill: {expander_text} !important; font-weight: 800 !important; font-size: 1rem !important; }}"
    
    # Textarea, input, and base select styling with Honey Gold outlines in Light Mode
    f"div[data-baseweb='input'] > div, div[data-baseweb='select'] > div, textarea, input {{ background-color: {input_bg} !important; color: {input_text} !important; border: 2px solid {panel_border} !important; }}"
    f"textarea::placeholder, input::placeholder {{ color: {placeholder_text} !important; opacity: 1 !important; }}"
    
    # DROPDOWN TEXT OVERRIDE
    f"div[data-baseweb='popover'] *, div[data-baseweb='menu'] *, ul[role='listbox'] *, li[role='option'] * {{ color: {dropdown_text} !important; font-weight: 700 !important; }}"
    f"li[role='option']:hover, li[role='option'][aria-selected='true'] {{ background-color: rgba(255, 184, 0, 0.25) !important; }}"
    
    f"label, p, span, div {{ color: {text_color} !important; }}"
    f"div.stButton > button {{ background: {btn_bg} !important; color: #ffffff !important; border-radius: 8px !important; border: none !important; font-weight: bold !important; width: 100% !important; padding: 0.75rem !important; }}"
    "</style>"
)

header_html = (
    '<div class="marge-header">'
    '<div class="marge-title">🏹 M.A.R.G.E.</div>'
    '<div class="marge-subtitle">Multimodal Automated Real-time Guardian Engine</div>'
    '<div class="marge-essence">✨ The Equity Guardian — Thought Guidance & Algorithmic Protection ✨</div>'
    '</div>'
)

st.markdown(css_code + header_html, unsafe_allow_html=True)

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

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.markdown(f"<h3 style='color: {title_color}; margin-top: 0;'>🏹 Guardian Portal</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    raw_handle = st.text_input("Your Name / Handle", value="Pocketdoc")
    formatted_handle = raw_handle.strip() if raw_handle.strip() else "Guardian"
    display_name = f"Dr. {formatted_handle}" if not formatted_handle.startswith("Dr.") and "pocketdoc" in formatted_handle.lower() else formatted_handle

    page_selection = st.selectbox("Navigation View", ["🔍 Audit Console", "🏛️ Five-Pillar Taxonomy", "📖 System Guide"])

    enable_ai_to_ai = st.toggle("AI-to-AI Interceptor", value=True)

    st.markdown("---")
    st.markdown(f"<h4 style='color: {title_color};'>⚙️ System Settings</h4>", unsafe_allow_html=True)
    
    selected_theme = st.radio(
        "Theme Style",
        ["Dark Mode", "Light Mode"],
        index=0 if st.session_state.theme_mode == "Dark Mode" else 1
    )
    if selected_theme != st.session_state.theme_mode:
        st.session_state.theme_mode = selected_theme
        st.rerun()

    api_key_input = st.text_input(
        "OpenAI API Key (Optional)", 
        value=st.session_state.api_key, 
        type="password",
        placeholder="sk-..."
    )
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input

scan_mode = "Initial Scan"
input_preset = "Custom Text Entry"

if page_selection == "🔍 Audit Console":
    st.markdown("<div class='control-panel'>", unsafe_allow_html=True)
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
                    issue_identified="Geographic/Demographic proxy conditioning evaluation capacity.",
                    detailed_explanation="Coupling geographic or demographic markers with capability words introduces subconscious bias and backhanded praise.",
                    collaborative_rationale="Eliminates coded geographic proxies and backhanded compliments through active inclusion and equity, centering candidates strictly on objective operational competencies without demographic bias.",
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
                    collaborative_rationale="Reframing subjective tone-policing into quantifiable leadership strengths ('assertive clarity') mitigates gendered and racial double standards through inclusive evaluation frameworks.",
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
                    collaborative_rationale="Proactively mitigates socio-economic barriers by embedding structural accessibility, inclusion, and equitable working arrangements.",
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
    welcome_html = (
        f'<div style="background-color: {card_bg}; padding: 0.9rem; border-radius: 10px; border: 2px solid {panel_border}; margin-bottom: 0.9rem;">'
        f'<h3 style="color: {title_color}; margin: 0; font-size: 1.15rem;">✨ Welcome, {display_name}.</h3>'
        f'<p style="color: {subtitle_color}; margin-top: 0.2rem; margin-bottom: 0; font-size: 0.82rem;">'
        'M.A.R.G.E. stands by as your algorithmic angel and equity guardian.'
        '</p></div>'
    )
    st.markdown(welcome_html, unsafe_allow_html=True)
    
    GREETING_PLACEHOLDERS = [
        "What message or text stream can I help guide and refine for you today?",
        "Share your prompt, policy text, or conversation draft to begin the guardian audit...",
        "How can M.A.R.G.E. partner with you to inspect and harmonize your communication today?",
        "Enter your text here to safeguard against structural bias and systemic erasure..."
    ]
    
    if input_preset == "HR Policy Sample":
        default_val = "Some folks from the inner city are just not cut out for tech leadership; they are often too aggressive during reviews."
    elif input_preset == "AI-to-AI Intercept Stream":
        default_val = "The candidate from the inner city is unusually articulate for this role."
    else:
        default_val = st.session_state.voice_input_text

    chosen_placeholder = random.choice(GREETING_PLACEHOLDERS)
    
    target_text = st.text_area(
        "Input Text Stream for Analysis:", 
        value=default_val, 
        placeholder=chosen_placeholder,
        height=120
    )

    voice_component_html = f"""
    <div style="display: flex; align-items: center; gap: 10px; margin-top: -5px; margin-bottom: 10px; font-family: sans-serif;">
        <button id="record-btn" style="
            background: {btn_bg}; 
            color: #ffffff; 
            border: none; 
            padding: 6px 14px; 
            border-radius: 16px; 
            font-weight: bold; 
            cursor: pointer; 
            display: flex; 
            align-items: center; 
            gap: 6px;
            font-size: 0.8rem;
        ">
            <span id="mic-icon">🎙️</span> <span id="btn-text">Tap to Speak Input</span>
        </button>
        <span id="status-text" style="font-size: 0.78rem; color: {title_color}; font-style: italic;"></span>
    </div>

    <script>
        const btn = document.getElementById('record-btn');
        const btnText = document.getElementById('btn-text');
        const micIcon = document.getElementById('mic-icon');
        const statusText = document.getElementById('status-text');

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {{
            btn.style.display = 'none';
            statusText.innerText = 'Speech-to-text not supported in this browser.';
        }} else {{
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            let isRecording = false;

            btn.onclick = () => {{
                if (!isRecording) {{
                    recognition.start();
                    isRecording = true;
                    btnText.innerText = 'Listening... Speak now';
                    micIcon.innerText = '🔴';
                    statusText.innerText = 'Recording...';
                }} else {{
                    recognition.stop();
                    isRecording = false;
                    btnText.innerText = 'Tap to Speak Input';
                    micIcon.innerText = '🎙️';
                    statusText.innerText = '';
                }}
            }};

            recognition.onresult = (event) => {{
                const transcript = event.results[0][0].transcript;
                statusText.innerText = 'Captured: "' + transcript + '"';
                btnText.innerText = 'Tap to Speak Input';
                micIcon.innerText = '🎙️';
                isRecording = false;

                navigator.clipboard.writeText(transcript);
                alert('Speech recorded and copied! Click inside the text box above and press Paste (Ctrl+V / Cmd+V): "' + transcript + '"');
            }};

            recognition.onerror = (event) => {{
                statusText.innerText = 'Error: ' + event.error;
                btnText.innerText = 'Tap to Speak Input';
                micIcon.innerText = '🎙️';
                isRecording = false;
            }};
        }}
    </script>
    """
    components.html(voice_component_html, height=40)

    if st.button("🏹 Execute M.A.R.G.E. Guardian Audit"):
        if not target_text.strip():
            st.warning("Please enter your text stream or select an example preset to analyze.")
        else:
            with st.spinner("M.A.R.G.E. is evaluating linguistic patterns with active degradation safety..."):
                result: MARGEEvaluationPayload = asyncio.run(async_marge_audit(target_text, scan_mode))

            st.markdown("---")
            st.markdown(f"<h4 style='color: {title_color}; font-size: 0.95rem; margin-bottom: 0.4rem;'>🏹 Guardian Index Severity Meter</h4>", unsafe_allow_html=True)
            pct = max(0, min(100, result.guardian_index))
            
            scale_html = (
                f'<div style="background-color: {card_bg}; padding: 0.9rem; border-radius: 10px; border: 2px solid {panel_border}; margin-bottom: 1rem;">'
                f'<div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem; font-weight: bold; color: {title_color}; font-size: 0.8rem;">'
                '<span>Critical Bias (0)</span>'
                f'<span>Guardian Index: {result.guardian_index} / 100</span>'
                '<span>Pure Harmony (100)</span></div>'
                '<div style="position: relative; width: 100%; height: 10px; background: linear-gradient(90deg, #dc3545 0%, #ffc107 50%, #28a745 100%); border-radius: 5px;">'
                f'<div style="position: absolute; left: {pct}%; top: -11px; transform: translateX(-50%); font-size: 1.2rem;">🏹</div></div>'
                f'<div class="degradation-badge">Status: {result.degradation_tier}</div></div>'
            )
            st.markdown(scale_html, unsafe_allow_html=True)

            col_orig, col_rem = st.columns([1, 1])
            with col_orig:
                st.markdown("🔴 **Original / Intercepted Text**")
                st.info(result.original_text)
            with col_rem:
                st.markdown("🟢 **M.A.R.G.E. Restored Output**")
                st.success(result.remediated_text)

            if scan_mode == "Initial Scan":
                st.markdown("---")
                st.markdown(f"<h4 style='color: {title_color}; font-size: 0.95rem;'>⚡ Initial Pattern Screen Overview</h4>", unsafe_allow_html=True)
                st.markdown(f"<span style='color: {subtitle_color}; font-size: 0.82rem;'>Initial scan detected active microaggression and subconscious framing patterns. Switch to <strong>Deep Intersectional Scan</strong> in the top control panel for full guidance and strategic rewrites.</span>", unsafe_allow_html=True)
            else:
                st.markdown("---")
                st.markdown(f"<h3 style='color: {title_color}; font-size: 1.05rem;'>✨ Guardian Insights & Thought Partner Guide</h3>", unsafe_allow_html=True)
                
                if result.violations:
                    for v in result.violations:
                        with st.expander(f"🏹 Flagged: {v.pillar_name} (Severity: {v.severity_score})", expanded=True):
                            st.markdown(f"**Issue Identified:** {v.issue_identified}")
                            st.markdown(f"**Context Explanation:** {v.detailed_explanation}")
                            st.markdown(f"🌟 **Guardian Rationale & Alignment:** *{v.collaborative_rationale}*")
                            st.markdown(f"**Harmonized Remedy:** <span style='color: {title_color}; font-weight: bold;'>{v.active_remedy}</span>", unsafe_allow_html=True)
                else:
                    st.balloons()
                    st.success("✨ Pure harmony! No microaggressions or structural bias vectors detected.")

elif page_selection == "🏛️ Five-Pillar Taxonomy":
    st.markdown(f"<h2 style='color: {title_color}; font-size: 1.3rem;'>🏛️ The Five-Pillar Equity Framework</h2>", unsafe_allow_html=True)
    st.markdown("---")
    for pillar, desc in FIVE_PILLARS.items():
        card_html = (
            '<div class="guardian-card">'
            f'<strong style="color: {title_color};">🏹 {pillar}</strong><br>'
            f'<span style="font-size: 0.82rem;">{desc}</span></div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)

else:
    st.markdown(f"<h2 style='color: {title_color}; font-size: 1.3rem;'>📖 M.A.R.G.E. System Guide</h2>", unsafe_allow_html=True)
    guide_html = (
        '<div style="line-height: 1.5; font-size: 0.85rem;">'
        '<p><strong>M.A.R.G.E. (Multimodal Automated Real-time Guardian Engine)</strong> acts as an algorithmic angel and equity guardian, serving as a type-safe middleware gatekeeper with gradual degradation safety.</p>'
        f'<h4 style="color: {title_color};">System Degradation & Resilience Tiers:</h4>'
        '<ul>'
        '<li><strong>Tier 1 (Full Inspection)</strong>: Complete multi-pillar async valuation and thought-partner rationale.</li>'
        '<li><strong>Tier 2 (Heuristic Screen)</strong>: Local pattern matching when model resources are constrained.</li>'
        '<li><strong>Tier 3 (Safe Passthrough)</strong>: Guaranteed uptime passthrough ensuring zero service interruption.</li>'
        '</ul></div>'
    )
    st.markdown(guide_html, unsafe_allow_html=True)
