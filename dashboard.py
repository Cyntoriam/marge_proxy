import asyncio
import html
import os
import re
import streamlit as st
from app.tiers.tier2_judge import run_async_marge_audit


st.set_page_config(
    page_title="M.A.R.G.E. | The Equity Guardian",
    page_icon="🏹",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "app_section" not in st.session_state:
    st.session_state.app_section = "🏹 The Guardian Audit"
if "last_results" not in st.session_state:
    st.session_state.last_results = None
if "current_payload" not in st.session_state:
    st.session_state.current_payload = ""

with st.sidebar:
    st.header("Visitor Portal")
    visitor_name = st.text_input(
        "Your Name / Handle", value="Pocketdoc", placeholder="Enter your name..."
    )

    st.markdown("---")
    st.header("API & Engine Config")
    openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=os.environ.get("OPENAI_API_KEY", ""),
        help="Used only for this Streamlit session; it is not written to project files.",
    ).strip()
    ai_engine_mode = st.toggle(
        "Enable AI-to-AI Engine (Async OpenAI)",
        value=False,
        help="Uses asynchronous OpenAI evaluation when an API key is available.",
    )

    st.markdown("---")
    st.header("Navigation Panel")
    if st.button("🏹 The Guardian Audit", use_container_width=True):
        st.session_state.app_section = "🏹 The Guardian Audit"
    if st.button("📖 About & User Guide", use_container_width=True):
        st.session_state.app_section = "📖 About & User Guide"
    app_section = st.session_state.app_section

    st.markdown("---")
    st.header("Guardian Controls & Preferences")
    theme_choice = st.selectbox(
        "Theme Mode",
        ["Dark (Oshun Sunrise)", "Light (Radiant Day)"],
    )
    sound_enabled = st.toggle(
        "Enable Audio Cues",
        value=True,
        help="Plays a gentle chime after an audit completes.",
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
            .marge-header {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 1.2rem 0 0.8rem 0;
                margin-bottom: 1.5rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            .marge-icon {
                font-size: 1.5rem;
                margin-bottom: 0.2rem;
            }
            .marge-title {
                font-size: 1.8rem;
                font-weight: 700;
                letter-spacing: 0.05em;
                margin: 0;
                color: #FAFAFA;
            }
            .marge-subtitle {
                font-size: 0.9rem;
                font-weight: 400;
                color: #A0A0A0;
                margin-top: 0.3rem;
                letter-spacing: 0.02em;
            }
        </style>
        <div class="marge-header">
            <div class="marge-icon">🏹</div>
            <h1 class="marge-title">M.A.R.G.E.</h1>
            <div class="marge-subtitle">Multimodal Automated Real-time Guardian Engine &bull; Equity Audit Dashboard</div>
        </div>
    """, unsafe_allow_html=True)


def _normalize_ai_results(audit_payload):
    assessment = {}
    recommendations = []
    for evaluation in audit_payload.evaluations:
        status = "Potential signal" if evaluation.bias_detected else "No pattern signal detected"
        note = evaluation.why_flagged
        if evaluation.observation:
            note = f"Observation: {evaluation.observation}\n{note}"
        assessment[evaluation.pillar_name] = {
            "status": status,
            "note": note,
            "rewrite": evaluation.suggested_rewrite,
        }
        if evaluation.bias_detected and evaluation.suggested_rewrite:
            recommendations.append(
                f"**{evaluation.pillar_name} Rewrite Suggestion:** {evaluation.suggested_rewrite}"
            )

    return {
        "guardian_signal_index": audit_payload.overall_guardian_index,
        "matched_pillar_count": sum(item.bias_detected for item in audit_payload.evaluations),
        "assessment": assessment,
        "intersectional_explanation": [audit_payload.self_correction_directive],
        "recommendations": recommendations,
        "recommendation_title": "AI-Generated Competency-Focused Rewrites",
        "used_fallback": any(
            "Illustrative fallback only" in item.why_flagged
            for item in audit_payload.evaluations
        ),
    }


def main():
    render_header()
    greeting_name = html.escape(visitor_name.strip() or "Traveler")

    if app_section == "📖 About & User Guide":
        st.markdown(f"### Welcome to the M.A.R.G.E. Knowledge Base, {greeting_name}!")
        st.markdown(
            "M.A.R.G.E. reviews policy language for potential equity and access signals. "
            "The local heuristic scan is illustrative; the optional OpenAI engine returns structured evaluations for human review."
        )
    else:
        st.markdown(f"### Hello, {greeting_name}! Welcome to M.A.R.G.E.")
        st.markdown(
            "Paste your document below to run a Guardian audit and review pillar findings and suggested rewrites."
        )

        st.markdown(
            f"""
            <div class="chat-input-container">
                <div style="color: #D9531E; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.4rem;">
                    🏹 What text, policy, or vision are we guarding today, {greeting_name}?
                </div>
                <div style="font-size: 0.9rem; margin-bottom: 0.8rem; opacity: 0.8;">
                    Run a standard or deep audit, inspect its signals, then approve any suggested text changes.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        user_payload = st.text_area(
            "Payload Content Box",
            placeholder="Type or paste text here...",
            height=160,
            label_visibility="collapsed",
            value=st.session_state.current_payload,
        )
        st.session_state.current_payload = user_payload

        if st.button("Run Instant Audit", type="primary"):
            if not user_payload.strip():
                st.error("Please enter at least 10 characters before running the audit.")
            elif ai_engine_mode and not (
                openai_api_key or os.environ.get("OPENAI_API_KEY") or os.environ.get("LLM_API_KEY")
            ):
                st.error("Enter an OpenAI API key or configure OPENAI_API_KEY / LLM_API_KEY on the server.")
            else:
                scan_mode = (
                    "Deep Intersectional Scan"
                    if "Deep" in st.session_state.get("scan_type", "Deep Architectural Scan")
                    else "Standard Audit"
                )
                if sound_enabled:
                    st.markdown(
                        """
                        <audio autoplay style="display:none;">
                            <source src="https://actions.google.com/sounds/v1/ambiences/morning_birds.ogg" type="audio/ogg">
                        </audio>
                        """,
                        unsafe_allow_html=True,
                    )

                with st.spinner("M.A.R.G.E. is auditing the payload..."):
                    if ai_engine_mode:
                        audit_payload = asyncio.run(
                            run_async_marge_audit(
                                user_payload,
                                st.session_state.get("scan_type", "Deep Architectural Scan"),
                                api_key=openai_api_key or None,
                            )
                        )
                        results = _normalize_ai_results(audit_payload)
                    else:
                        results = evaluate_equity_payload(user_payload, mode=scan_mode)

                if "error" in results:
                    st.error(results["error"])
                else:
                    results["source_payload"] = user_payload
                    results["ai_engine_mode"] = ai_engine_mode
                    st.session_state.last_results = results

        if st.session_state.last_results:
            results = st.session_state.last_results
            signal_index = results["guardian_signal_index"]
            arrow_position = min(max(signal_index, 2), 98)
            st.markdown("<br>", unsafe_allow_html=True)
            st.success(f"Guardian audit complete for {greeting_name}.")
            if results.get("used_fallback"):
                st.warning("Illustrative fallback shown; no live model evaluation was performed.")

            st.markdown(
                f"""
                <div class="guardian-scale-container" style="padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; text-align: center;">
                    <div style="color: #D9531E; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Guardian Index</div>
                    <div style="font-size: 1.6rem; font-weight: 700; margin-top: 0.5rem;">{signal_index} / 100</div>
                    <div style="opacity: 0.8;">{results['matched_pillar_count']} of 5 pillar groups flagged</div>
                    <div class="scale-track"><div class="guardian-arrow-marker" style="left: {arrow_position}%">🏹</div></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if results.get("intersectional_explanation"):
                st.info("\n\n".join(results["intersectional_explanation"]))

            st.markdown("### Five-Pillar Audit Results")
            rewritable_findings = []
            for pillar, details in results["assessment"].items():
                is_flagged = details["status"] == "Potential signal"
                st.markdown(f"**{pillar}** · {details['status']}")
                st.write(details["note"])
                if details.get("rewrite") and is_flagged:
                    st.markdown(f"Suggested rewrite: {details['rewrite']}")
                    rewritable_findings.append((pillar, details["rewrite"]))
                st.markdown("---")

            if results.get("recommendations"):
                st.markdown("### " + (results.get("recommendation_title") or "Pillar Rewrite Suggestions"))
                for recommendation in results["recommendations"]:
                    st.markdown(recommendation)

            if rewritable_findings:
                st.markdown("### Active Document Update")
                apply_rewrites = st.checkbox(
                    "Approve and apply generated equity rewrites directly into the document payload"
                )
                if st.button("Apply Approved Changes Now"):
                    if apply_rewrites:
                        revised_text = results.get("source_payload", user_payload)
                        for pillar, rewrite in rewritable_findings:
                            marker = f"[M.A.R.G.E. Revision ({pillar}):"
                            if marker not in revised_text:
                                revised_text += f"\n\n{marker} {rewrite}]"
                        st.session_state.current_payload = revised_text
                        st.session_state.last_results = None
                        st.success("Approved rewrites applied to the document payload.")
                        st.rerun()
                    else:
                        st.warning("Please check the approval box to confirm and apply changes.")


if __name__ == "__main__":
    main()
