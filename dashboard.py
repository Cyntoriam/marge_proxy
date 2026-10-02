import asyncio
import html
import os
import re
import streamlit as st
from app.tiers.tier2_judge import run_async_marge_audit


st.set_page_config(
    page_title="M.A.R.G.E. | Multimodal Automated Real-time Guardian Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "app_section" not in st.session_state:
    st.session_state.app_section = "🏹 The Guardian Audit"
if "current_payload" not in st.session_state:
    st.session_state.current_payload = ""
if "last_results" not in st.session_state:
    st.session_state.last_results = None

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
        help="Use structured OpenAI evaluation when a key is configured.",
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
            r"relocat\w*|suburban|headquarters|corridor|downtown|commute|inner city|"
            r"those people|you people|they always|"
            r"on[- ]?site|campus hub)\b",
        ),
        "deep_patterns": (r"\b(?:food desert|transit desert|service desert)\b",),
        "note": "Location, service access, or economic exclusion language needs context review.",
        "rewrite": "Offer flexible geographic or remote participation paths; replace restrictive location qualifiers with accessible access points.",
    },
    "Intersectional Microaggressions": {
        "patterns": (
            r"\b(?:aggressive|articulate|so articulate|unprofessional|emotional|polished|"
            r"assertive|bossy|where are you really from|you don't look like|"
            r"traditional university|pedigree|assimilation|backward|"
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
            r"\b(?:naturally suited|born to|people like them)\b",
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
    guardian_signal_index = max(100 - matched_pillar_count * 20, 0)

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
                background: linear-gradient(135deg, #17120e 0%, #251913 55%, #301a16 100%);
                padding: 2rem;
                border-radius: 12px;
                color: #f3f3f8;
                margin-bottom: 2rem;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
                border: 1px solid rgba(212, 175, 55, 0.3);
                text-align: center;
            }
            .marge-icon {
                font-size: 2.5rem;
            }
            .marge-title {
                font-size: 2.5rem;
                font-weight: 800;
                margin-bottom: 0.5rem;
                color: #D4AF37;
                letter-spacing: 0;
            }
            .marge-subtitle {
                font-size: 1.05rem;
                color: #E0D8CF;
                font-weight: 400;
            }
            .marge-subtitle em {
                color: #00C9A7;
                font-style: italic;
                font-weight: 600;
            }
            .guardian-card {
                background: rgba(38, 31, 27, 0.82);
                padding: 1.25rem;
                border-radius: 8px;
                border-left: 4px solid #D9531E;
                margin-bottom: 1rem;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.16);
            }
            .stMarkdown ul {
                list-style: none;
                padding-left: 0;
            }
            .stMarkdown ul li::before {
                content: "🏹 ";
                color: #D4AF37;
                font-weight: bold;
                display: inline-block;
                width: 1.5em;
                margin-left: -1.5em;
            }
        </style>
        <div class="marge-header">
            <div class="marge-icon">🏹</div>
            <h1 class="marge-title">🏹 M.A.R.G.E. 🛡️</h1>
            <div class="marge-subtitle">Multimodal Automated Real-time Guardian Engine — <em>The Equity Guardian</em></div>
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


FIVE_PILLARS = {
    "Pillar 1: Representational Justice": "Evaluates visual, textual, and cultural tokenism to ensure balanced demographic representation and accurate contextual framing.",
    "Pillar 2: Linguistic Equity": "Detects systemic bias against dialectal variations, non-standard syntax, regional phrasing, and socio-economic speech markers.",
    "Pillar 3: Intersectional Safety": "Identifies compounding vulnerabilities where overlapping identities such as race, gender, and socioeconomic status amplify algorithmic microaggressions or harm.",
    "Pillar 4: Empathy & Pro-social Alignment": "Measures whether model or document outputs foster psychological safety, validation, and emotional well-being instead of alienation.",
    "Pillar 5: Autonomous Self-Correction": "Drives remediation by generating equitable alternatives for human review.",
}


def _corrected_draft(original: str, audit_payload) -> str:
	corrected = original
	for evaluation in audit_payload.evaluations:
		if (
			evaluation.bias_detected
			and evaluation.observation
			and evaluation.suggested_rewrite
			and evaluation.observation.casefold() in corrected.casefold()
		):
			corrected = re.sub(
				re.escape(evaluation.observation),
				lambda _match: evaluation.suggested_rewrite,
				corrected,
				count=1,
				flags=re.IGNORECASE,
			)
	return corrected


def _remediate_local_text(original: str) -> str:
    substitutions = (
        (r"\bthose people\b", "people in the specific community"),
        (r"\byou people\b", "members of this community"),
        (r"\bthey always\b", "some people may"),
        (r"\binner city\b", "[specific community context needed]"),
        (r"\bso articulate\b", "communicates clearly"),
        (r"\bwhere are you really from\b", "what places have shaped your experience"),
        (r"\byou don't look like\b", "[reframed without an appearance-based assumption]"),
        (r"\baggressive\b", "direct in communication style"),
        (r"\bbossy\b", "assertive"),
    )
    revised = original
    for pattern, replacement in substitutions:
        revised = re.sub(pattern, replacement, revised, flags=re.IGNORECASE)
    return revised


def main():
    render_header()
    greeting_name = html.escape(visitor_name.strip() or "Traveler")
    if app_section == "📖 About & User Guide":
        st.markdown(f"### Welcome to the M.A.R.G.E. Knowledge Base, {greeting_name}!")
        st.markdown("M.A.R.G.E. reviews text for potential equity and access signals. Findings are heuristic or AI-assisted and require human judgment.")
        return

    tab_scanner, tab_pillars = st.tabs(
        ["🔍 Document & Idea Scanner", "🏛️ Five-Pillar Taxonomy"]
    )

    with tab_scanner:
        st.subheader("Asynchronous Microaggression & Bias Guardian Audit")
        st.markdown("Scan policy text or uploaded documents across the Five Pillars, calculate a Guardian Index, and review proposed neutralizations before using them.")
        input_mode = st.radio(
            "Select Input Source:",
            ["Direct Text Input", "Simulated Document Upload"],
            horizontal=True,
        )

        if input_mode == "Direct Text Input":
            target_input = st.text_area(
                "Enter idea, policy, or text excerpt to scan:",
                value=st.session_state.current_payload or "Some folks from the inner city are just not cut out for tech leadership; they are often too aggressive when speaking up.",
                height=150,
                key="scanner_text_input",
            )
        else:
            uploaded_doc = st.file_uploader(
                "Upload a text or policy document", type=["txt", "md"]
            )
            if uploaded_doc is not None:
                target_input = uploaded_doc.getvalue().decode("utf-8", errors="replace")
                st.text_area("Scanned document preview", value=target_input, height=150, disabled=True)
            else:
                target_input = st.session_state.current_payload or "Sample policy text: Certain groups are always too articulate during reviews, which can disrupt the standard workflow."
                st.info("Upload a `.txt` or `.md` file, or run the sample text shown below.")
                st.text_area("Sample document preview", value=target_input, height=120, disabled=True)
        st.session_state.current_payload = target_input

        if st.button("🏹 Release Guardian Audit", type="primary"):
            if len(target_input.strip()) < 10:
                st.error("Please provide at least 10 characters to run the audit.")
            elif ai_engine_mode and not (
                openai_api_key or os.environ.get("OPENAI_API_KEY") or os.environ.get("LLM_API_KEY")
            ):
                st.error("Enter an OpenAI API key in the sidebar or configure one in the server environment.")
            else:
                with st.spinner("M.A.R.G.E. is auditing the text through the five pillars..."):
                    if ai_engine_mode:
                        audit_payload = asyncio.run(
                            run_async_marge_audit(
                                target_input,
                                "Deep Architectural Scan",
                                api_key=openai_api_key or None,
                            )
                        )
                        assessment = _normalize_ai_results(audit_payload)
                        violations = [
                            {
                                "pillar": item.pillar_name,
                                "issue": " ".join(part for part in (item.observation, item.why_flagged) if part),
                                "remedy": item.suggested_rewrite,
                            }
                            for item in audit_payload.evaluations
                            if item.bias_detected
                        ]
                        remediated = _corrected_draft(target_input, audit_payload)
                        used_fallback = assessment["used_fallback"]
                        guardian_index = audit_payload.overall_guardian_index
                    else:
                        local_result = evaluate_equity_payload(
                            target_input, mode="Deep Intersectional Scan"
                        )
                        assessment = local_result
                        violations = [
                            {
                                "pillar": name,
                                "issue": details["note"],
                                "remedy": details["rewrite"],
                            }
                            for name, details in local_result["assessment"].items()
                            if details["status"] == "Potential signal"
                        ]
                        used_fallback = False
                        guardian_index = local_result["guardian_signal_index"]
                        remediated = _remediate_local_text(target_input)

                    remedies = [item["remedy"] for item in violations if item["remedy"]]
                    if remediated == target_input and remedies:
                        remediated += "\n\nSuggested revisions for human review:\n" + "\n".join(
                            f"- {remedy}" for remedy in remedies
                        )
                    st.session_state.last_results = {
                        "original": target_input,
                        "remediated": remediated,
                        "violations": violations,
                        "guardian_index": guardian_index,
                        "bow_rating": "🏹" * max(1, round(guardian_index / 20)) + f" (Guardian Index: {guardian_index}/100)",
                        "status": "Guardian remediation draft prepared" if violations else "No matching heuristic signals",
                        "assessment": assessment,
                        "used_fallback": used_fallback,
                    }

        result = st.session_state.last_results
        if result and result["original"] == target_input:
            st.markdown("---")
            st.subheader("🛡️ Guardian Index Score & Rating")
            score_col, bow_col = st.columns([1, 2])
            with score_col:
                st.metric("Guardian Index Score", f"{result['guardian_index']}/100")
            with bow_col:
                st.markdown("**Artemis Bow Rating**")
                st.markdown(f"### {result['bow_rating']}")

            if result["used_fallback"]:
                st.warning("Illustrative fallback shown; no live model evaluation was completed.")

            original_col, revised_col = st.columns(2)
            with original_col:
                st.error("Original input / scanned document")
                st.write(result["original"])
            with revised_col:
                st.success(f"🟢 M.A.R.G.E. Guardian-Supported Output ({result['status']})")
                st.write(result["remediated"])
                st.caption("Suggested text is a draft for human review; the source document is unchanged.")

            st.markdown("### 🏛️ Detailed Pillar Flag & Protection Log")
            if result["violations"]:
                for violation in result["violations"]:
                    st.markdown(f"**Pillar flagged:** {violation['pillar']}")
                    st.write(f"Issue identified: {violation['issue']}")
                    if violation["remedy"]:
                        st.write(f"Suggested remedy: {violation['remedy']}")
                    st.divider()
            else:
                st.info("No signals matched the evaluator's rules. This is not proof that the text is equitable.")

    with tab_pillars:
        st.subheader("The Five-Pillar Taxonomy Reference")
        st.caption("Conceptual reference. Automated findings use the evaluator labels shown in the audit log.")
        for pillar, description in FIVE_PILLARS.items():
            st.markdown(
                f"""
                <div class="guardian-card">
                    <strong>{pillar}</strong><br>
                    <span style="color: #E0D8CF;">{description}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
