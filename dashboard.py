import asyncio
import os
import re
import streamlit as st
from app.tiers.tier2_judge import run_async_marge_audit


st.set_page_config(
    page_title="M.A.R.G.E. v2.10",
    page_icon="🛡️",
    layout="wide",
)

# Sidebar theme preferences
with st.sidebar:
    st.header("Guardian Preferences")
    theme_choice = st.selectbox(
        "Theme Mode", 
        ["Dark (Oshun Sunrise)", "Light (Radiant Day)"]
    )

    st.caption("M.A.R.G.E. v2.10 • Multi-sensory equity middleware.")

is_dark_theme = "Dark" in theme_choice

# Harmonized Theme CSS Injection for both Light and Dark modes
if is_dark_theme:
    theme_css = """
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #0D0D0D !important;
            background-image: 
                radial-gradient(ellipse 80% 50% at 50% 0%, rgba(217, 83, 30, 0.35) 0%, rgba(212, 175, 55, 0.15) 40%, transparent 80%),
                radial-gradient(circle at 50% 15%, rgba(255, 140, 0, 0.22) 0%, transparent 55%),
                linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px) !important;
            background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px !important;
            color: #E0E0E0 !important;
        }
        .marge-header-card {
            background: linear-gradient(135deg, #1A120B 0%, #141414 100%) !important;
            border: 2px solid #D9531E !important;
            padding: 2.5rem 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 15px 40px rgba(217, 83, 30, 0.18);
        }
        .chat-input-container {
            background: rgba(26, 18, 14, 0.85) !important;
            border: 1px solid #D9531E !important;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 25px rgba(217, 83, 30, 0.12);
        }
        .about-card, .equity-card, .flagged-card, .guardian-scale-container, .workflow-step-card {
            background-color: #1A120B !important;
            border: 1px solid #3d2417 !important;
            color: #E0E0E0 !important;
        }
        [data-testid="stSidebar"] {
            background-color: #140E0A !important;
            border-right: 1px solid #3d2417 !important;
            color: #E0E0E0 !important;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
            color: #E0E0E0 !important;
        }
        input, textarea {
            background-color: #1A120B !important;
            color: #E0E0E0 !important;
            border: 1px solid #3d2417 !important;
        }
    """
else:
    theme_css = """
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-color: #FFF9F2 !important;
            background-image: 
                radial-gradient(ellipse 80% 50% at 50% 0%, rgba(217, 83, 30, 0.10) 0%, rgba(212, 175, 55, 0.06) 40%, transparent 80%),
                linear-gradient(rgba(0, 0, 0, 0.015) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 0, 0, 0.015) 1px, transparent 1px) !important;
            background-size: 100% 100%, 40px 40px, 40px 40px !important;
            color: #2C2C2C !important;
        }
        .marge-header-card {
            background: linear-gradient(135deg, #FFFFFF 0%, #FFF3E6 100%) !important;
            border: 2px solid #D9531E !important;
            padding: 2.5rem 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(217, 83, 30, 0.1);
        }
        .chat-input-container {
            background: #FFFFFF !important;
            border: 1px solid #E6D5C3 !important;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            box-shadow: 0 6px 20px rgba(217, 83, 30, 0.06);
        }
        .about-card, .equity-card, .flagged-card, .guardian-scale-container, .workflow-step-card {
            background-color: #FFFFFF !important;
            border: 1px solid #E6D5C3 !important;
            color: #2C2C2C !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
        }
        [data-testid="stSidebar"] {
            background-color: #FDF5ED !important;
            border-right: 1px solid #E6D5C3 !important;
            color: #2C2C2C !important;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div {
            color: #2C2C2C !important;
        }
        input, textarea {
            background-color: #FFFFFF !important;
            color: #2C2C2C !important;
            border: 1px solid #D6C2AB !important;
        }
    """

st.markdown(
    f"""
    <style>
        {theme_css}
        .marge-fullname {{
            color: #C84512 !important;
            font-size: 1.05rem;
            font-weight: 600;
            text-transform: uppercase;
            margin-top: 0.5rem;
            margin-bottom: 0.75rem;
            letter-spacing: 1px;
        }}
        .stButton > button {{
            background: linear-gradient(135deg, #D9531E 0%, #C84512 100%) !important;
            color: #FFFFFF !important;
            font-weight: 600;
            border: none;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(217, 83, 30, 0.3);
        }}
        .intersectional-banner {{
            border: 1px solid #D9531E !important;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            line-height: 1.6;
        }}
        .recommendation-banner {{
            border: 1px solid #81C784 !important;
            padding: 1rem;
            border-radius: 8px;
            margin: 1.5rem 0;
            line-height: 1.6;
        }}
        .scale-track {{
            position: relative;
            width: 100%;
            height: 16px;
            background: linear-gradient(90deg, #D4AF37 0%, #D9531E 55%, #E57373 100%) !important;
            border-radius: 8px;
            margin: 2rem 0 1rem;
        }}
        .guardian-arrow-marker {{
            position: absolute;
            top: -28px;
            transform: translateX(-50%);
            font-size: 1.8rem;
            transition: left 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .workflow-step-card {{
            border: 1px dashed #D9531E !important;
            padding: 1.2rem;
            border-radius: 8px;
            margin: 1.2rem 0;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


PILLAR_RULES = {
    "Spatial/Economic Erasure": {
        "patterns": (
            r"\b(?:bypass|exclude|exclusion|peripheral|low[- ]density|"
            r"underserved|redlin\w*|low[- ]income|order volume is low|"
            r"relocat\w*|suburban|headquarters|corridor|downtown|commute|"
            r"on[- ]?site|campus hub)\b",
        ),
        "deep_patterns": (r"\b(?:food desert|transit desert|service desert)\b",),
        "note": "Location, service access, or economic exclusion language needs context review.",
        "rewrite": "Offer flexible geographic or remote participation paths; replace restrictive location qualifiers with accessible access points.",
    },
    "Intersectional Microaggressions": {
        "patterns": (
            r"\b(?:aggressive|articulate|unprofessional|emotional|polished|"
            r"assertive|traditional university|pedigree|assimilation|backward|"
            r"culture|prestige|executive presence|institutional culture|"
            r"etiquette)\b",
        ),
        "deep_patterns": (r"\b(?:angry woman|angry black|culture fit)\b",),
        "note": "Potentially subjective descriptors can carry different implications across identities.",
        "rewrite": "Substitute subjective demeanor or prestige filters with explicit, competency-based contributions and role criteria.",
    },
    "Accessibility Justice": {
        "patterns": (
            r"\b(?:without accommodations|no accommodations|inaccessible|"
            r"wheelchair|screen reader|captions|disability|disabled|hour\w*|"
            r"on[- ]site|schedule|subtitles|transcript|fast[- ]paced|rhythm|"
            r"impromptu|rapid[- ]fire|residency|uninterrupted|evening|"
            r"velocity|huddles)\b",
        ),
        "deep_patterns": (r"\b(?:cognitive access|assistive technology|accessible format)\b",),
        "note": "Accessibility-related language was found; review whether the described needs are supported.",
        "rewrite": "Replace rigid scheduling, rapid pacing, or unannounced expectations with structured timelines, async options, and clear accommodations.",
    },
    "Stereotypical Framing": {
        "patterns": (
            r"\b(?:all women|all men|women are naturally|men are naturally|"
            r"older workers|young and energetic|professional appearance|"
            r"leadership roles|standard|traditional|align naturally|"
            r"high[- ]potential|impeccable|pathfinders)\b",
        ),
        "deep_patterns": (
            r"\b(?:naturally suited|born to|people like them|aggressive)\b",
        ),
        "note": "Generalizations or appearance criteria may encode assumptions about a group.",
        "rewrite": "Eliminate demographic or stylistic generalizations; evaluate performance against consistent, objective project outcomes.",
    },
    "Dialectal Justice": {
        "patterns": (
            r"\b(?:accent|grammar|non[- ]standard dialect|speak properly|"
            r"native speaker|broken english|dialect|vernacular|prose|"
            r"communication rhythms|polished clarity|direct|discourse|cadence)\b",
        ),
        "deep_patterns": (r"\b(?:professional language|clear english|communication style)\b",),
        "note": "Language-variety terms can be used to unfairly judge dialect or fluency; review context.",
        "rewrite": "Focus evaluation solely on functional clarity rather than specific dialect, cadence, or linguistic style.",
    },
}


def evaluate_equity_payload(text: str, mode: str = "Standard Audit") -> dict:
    if len(text.strip()) < 10:
        return {"error": "Please provide at least 10 characters for a useful pattern analysis."}

    content = text.lower()
    deep_scan = mode == "Deep Intersectional Scan"
    assessment = {}
    for pillar, rules in PILLAR_RULES.items():
        patterns = rules["patterns"]
        if deep_scan:
            patterns += rules["deep_patterns"]
        detected = any(re.search(pattern, content) for pattern in patterns)
        assessment[pillar] = {
            "status": "Potential signal" if detected else "No pattern signal detected",
            "note": rules["note"] if detected else "No matching pattern found; this is not evidence that the content is equitable.",
            "rewrite": rules["rewrite"] if detected else "",
        }

    matched_pillar_count = sum(
        details["status"] == "Potential signal" for details in assessment.values()
    )
    guardian_signal_index = matched_pillar_count * 20

    intersectional_explanation = None
    recommendations = None
    recommendation_title = None
    if deep_scan:
        flagged_pillars = {
            pillar
            for pillar, details in assessment.items()
            if details["status"] == "Potential signal"
        }
        explanation_blocks = [
            f"Analytical overview: The Deep Intersectional Scan marked {len(flagged_pillars)} of 5 pillars for potential signals."
        ]
        intersectional_explanation = explanation_blocks
        
        recommendations = [
            f"**{pillar} Rewrite Suggestion:** {PILLAR_RULES[pillar]['rewrite']}"
            for pillar in PILLAR_RULES if pillar in flagged_pillars
        ]
        recommendation_title = "Actionable Pillar Rewrite Suggestions"

        if not recommendations:
            recommendations.append(
                "No heuristic rules triggered in deep scan, so no automatic rewrite is suggested."
            )

    return {
        "mode": mode,
        "payload_length": len(text),
        "matched_pillar_count": matched_pillar_count,
        "guardian_signal_index": guardian_signal_index,
        "assessment": assessment,
        "intersectional_explanation": intersectional_explanation,
        "recommendations": recommendations,
        "recommendation_title": recommendation_title,
    }


def render_header():
    st.markdown("""
        <style>
            .marge-header-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 1.2rem 0 1rem 0;
                margin-bottom: 1.5rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            .marge-icon { font-size: 1.8rem; margin-bottom: 0.1rem; }
            .marge-title { font-size: 1.8rem; font-weight: 700; letter-spacing: 0.05em; margin: 0; color: #FAFAFA; }
            .marge-subtitle { font-size: 0.9rem; font-weight: 400; color: #D4AF37; margin-top: 0.3rem; margin-bottom: 0.8rem; letter-spacing: 0.02em; }
            .scale-track-wrapper { width: 80%; max-width: 400px; margin: 0 auto; }
            .scale-labels { display: flex; justify-content: space-between; font-size: 0.75rem; color: #A0A0A0; margin-bottom: 0.2rem; }
            .scale-bar { height: 6px; background: linear-gradient(90deg, #d9534f 0%, #f0ad4e 50%, #5cb85c 100%); border-radius: 3px; position: relative; }
        </style>
        <div class="marge-header-container">
            <div class="marge-icon">🏹</div>
            <h1 class="marge-title">M.A.R.G.E.</h1>
            <div class="marge-subtitle">Multimodal Automated Real-time Guardian Engine &bull; Equity Audit Dashboard</div>
            <div class="scale-track-wrapper">
                <div class="scale-labels">
                    <span>Critical Bias Risk</span>
                    <span>Neutral</span>
                    <span>Optimized Alignment</span>
                </div>
                <div class="scale-bar"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_human_mode(scan_type: str):
    st.markdown(f"### 🏹 Guardian Audit Workspace ({scan_type})")
    st.markdown("*Review policy language through a conversational mentorship experience. This workspace uses the local heuristic evaluator.*")

    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant",
            "content": "🏹 Hello! Share your policy text or ideas with me. We can review them together for equity, bias, and inclusive language.",
        }]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Type your policy text or chat with M.A.R.G.E...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        mode = "Deep Intersectional Scan" if scan_type == "Deep Architectural Scan" else "Standard Audit"
        result = evaluate_equity_payload(prompt, mode=mode)
        if "error" in result:
            response = result["error"]
        else:
            flagged = [
                pillar for pillar, details in result["assessment"].items()
                if details["status"] == "Potential signal"
            ]
            response = (
                f"🎯 **{scan_type} complete. Guardian Index: "
                f"{result['guardian_signal_index']}/100.**\n\n"
            )
            if flagged:
                response += "Potential signals: " + ", ".join(flagged) + ".\n\n"
            else:
                response += "No heuristic signals matched. This is not proof that the text is equitable.\n\n"
            response += "What pillar or community group would you like to explore further?"

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)


def render_ai_engine_mode(scan_type: str):
    st.markdown("### ⚙️ M.A.R.G.E. Asynchronous AI-to-AI Engine")
    st.markdown("*Run asynchronous structured evaluations against OpenAI at the selected scan depth. The self-correction directive is prepared for review, not automatically dispatched.*")

    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Used for this Streamlit session only. Leave blank to use OPENAI_API_KEY or LLM_API_KEY from the server environment.",
    ).strip()

    policy_input = st.text_area(
        "Policy Payload for Model-Level Evaluation:",
        value="Candidates must possess flawless executive presence, clear and unaccented communication cadence, and a prestigious university pedigree with zero remote accommodations.",
        height=100,
    )

    if st.button(f"Execute Async {scan_type}"):
        if not policy_input.strip():
            st.warning("Enter policy text before running the architectural audit.")
            return
        if not openai_api_key and not (
            os.environ.get("OPENAI_API_KEY") or os.environ.get("LLM_API_KEY")
        ):
            st.error("Enter an OpenAI API key or configure OPENAI_API_KEY / LLM_API_KEY on the server.")
            return

        with st.spinner(f"Running asynchronous M.A.R.G.E. evaluation via OpenAI..."):
            audit_payload = asyncio.run(
                run_async_marge_audit(
                    policy_input, scan_type, api_key=openai_api_key or None
                )
            )

        used_fallback = any(
            "Illustrative fallback only" in evaluation.why_flagged
            for evaluation in audit_payload.evaluations
        )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🏛️ Human-Facing Mentorship")
            flagged = [item for item in audit_payload.evaluations if item.bias_detected]
            if flagged:
                st.info("💡 **M.A.R.G.E.:** Potential signals were identified. Review the observations and suggested rewrites before making policy decisions.")
            else:
                st.info("💡 **M.A.R.G.E.:** No signals were returned. This does not prove the policy is equitable; human review remains important.")
            st.metric("Guardian Index", audit_payload.overall_guardian_index)

        with col2:
            st.markdown("#### ⚙️ Async OpenAI Schema Payload")
            st.code(audit_payload.model_dump_json(indent=2), language="json")

        if used_fallback:
            st.warning("Illustrative fallback shown; no live model evaluation was performed.")
        else:
            st.success("Structured audit completed. Review the directive before applying any downstream changes.")


def main():
    render_header()
    if "interaction_mode" not in st.session_state:
        st.session_state.interaction_mode = "💬 Human Conversational & Mentorship"
    if "scan_type" not in st.session_state:
        st.session_state.scan_type = "Standard Guardian Scan"

    with st.sidebar:
        st.markdown("### ⚙️ Guardian Navigation")
        st.markdown("Select an interaction mode:")

        if st.button("💬 Human Conversational & Mentorship", use_container_width=True):
            st.session_state.interaction_mode = "💬 Human Conversational & Mentorship"
        if st.button("⚙️ AI-to-AI Architectural Engine", use_container_width=True):
            st.session_state.interaction_mode = "⚙️ AI-to-AI Architectural Engine"

        st.markdown("---")
        st.markdown("### 🔍 Audit Depth")
        if st.button("📌 Standard Guardian Scan", use_container_width=True):
            st.session_state.scan_type = "Standard Guardian Scan"
        if st.button("🔬 Deep Architectural Scan", use_container_width=True):
            st.session_state.scan_type = "Deep Architectural Scan"

        st.markdown(f"**Active Mode:** `{st.session_state.interaction_mode}`")
        st.markdown(f"**Active Depth:** `{st.session_state.scan_type}`")

    if st.session_state.interaction_mode == "💬 Human Conversational & Mentorship":
        render_human_mode(st.session_state.scan_type)
    else:
        render_ai_engine_mode(st.session_state.scan_type)


if globals().get("__name__") == "__main__":
    main()
