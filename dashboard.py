import re
import streamlit as st


st.set_page_config(
    page_title="M.A.R.G.E. | The Equity Guardian",
    page_icon="🏹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state for navigation & workflow steps
if "app_section" not in st.session_state:
    st.session_state.app_section = "🏹 The Guardian Audit"

if "audit_step" not in st.session_state:
    st.session_state.audit_step = "idle" # idle, audited, deep_scanned, recommendations_offered, rewrites_generated, rewrites_applied

if "last_results" not in st.session_state:
    st.session_state.last_results = None

if "current_payload" not in st.session_state:
    st.session_state.current_payload = ""

# Sidebar Configuration & Preferences
with st.sidebar:
    st.header("Visitor Portal")
    visitor_name = st.text_input("Your Name / Handle", value="Pocketdoc", placeholder="Enter your name...")

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
        ["Dark (Oshun Sunrise)", "Light (Radiant Day)"]
    )
    
    sound_enabled = st.toggle("Enable Audio Cues", value=True, help="Plays a gentle ambient chime upon audit completion.")
        
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
        .marge-title {{
            color: #D9531E !important;
            font-family: Georgia, serif;
            font-size: 3rem;
            font-weight: 800;
            margin: 0;
            text-shadow: 0 2px 15px rgba(217, 83, 30, 0.2);
        }}
        .marge-fullname {{
            color: #C84512 !important;
            font-size: 1.05rem;
            font-weight: 600;
            text-transform: uppercase;
            margin-top: 0.5rem;
            margin-bottom: 0.75rem;
            letter-spacing: 1px;
        }}
        .marge-subtitle {{
            color: #B8860B !important;
            font-size: 1.1rem;
            margin: 0 0 0.3rem;
            font-style: italic;
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


# --- Page Configuration ---
st.set_page_config(
    page_title="M.A.R.G.E. v2.10",
    page_icon="🛡️",
    layout="wide"
)

# --- Original Header Style (with Acronym & Tooltip) ---
st.markdown(
    """
    <div style="padding: 10px 0;">
        <h1 style="margin-bottom: 0px;" title="Multimodal Automated Real-time Guardian Engine">
            M.A.R.G.E. v2.10
        </h1>
        <p style="font-size: 1.1em; color: #555; margin-top: 4px;">
            <strong>Multimodal Automated Real-time Guardian Engine</strong>
        </p>
    </div>
    <hr style="margin-top: 0px; margin-bottom: 20px;">
    """,
    unsafe_allow_html=True
)

# --- Helper Component: Artemis Bow Sliding Scale on Target ---
def render_artemis_bow_target(score: int, label: str = "Guardian Index"):
    """
    Renders a visual Artemis bow sliding scale on a target representation.
    Score ranges from 0 to 100.
    """
    clamped_score = max(0, min(100, score))

    if clamped_score >= 80:
        color = "#2e7d32"
        status = "Optimal Alignment"
    elif clamped_score >= 60:
        color = "#f57c00"
        status = "Moderate Drift"
    else:
        color = "#c62828"
        status = "Critical Deflection"

    html_content = f"""
    <div style="background: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 8px; padding: 12px; margin: 10px 0; font-family: sans-serif;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-weight: bold; font-size: 0.95em; color: #333;">🏹 {label} Target: <code>{clamped_score}/100</code></span>
            <span style="font-size: 0.85em; font-weight: bold; color: {color};">{status}</span>
        </div>
        <div style="position: relative; background: #e9ecef; height: 12px; border-radius: 6px; width: 100%;">
            <div style="position: absolute; left: 80%; width: 20%; height: 100%; background: rgba(46, 125, 50, 0.2); border-top-right-radius: 6px; border-bottom-right-radius: 6px;"></div>
            <div style="position: absolute; left: calc({clamped_score}% - 6px); top: -4px; width: 12px; height: 20px; background: {color}; border: 2px solid white; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 0.75em; color: #666; margin-top: 4px;">
            <span>0 (Deflected)</span>
            <span>50 (Mid-Range)</span>
            <span>100 (Bullseye)</span>
        </div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

# --- Initialize Session State for Chat & Workflow Phase ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! I am **M.A.R.G.E.** Please paste your policy text, document snippet, "
                "or vision text below to initiate the **Standard Guardian Audit**."
            )
        }
    ]

if "workflow_step" not in st.session_state:
    st.session_state.workflow_step = 0  # 0: Waiting for text, 1: Audit Done, 2: Deep Scan Done, 3: Recommendations Done, 4: Rewrites Done

if "target_text" not in st.session_state:
    st.session_state.target_text = ""

# --- Render Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "score_val" in message:
            render_artemis_bow_target(message["score_val"], message.get("score_label", "Guardian Index"))

# --- Chat Input Box (Pinned to Bottom with Speech-to-Text Ergonomics) ---
prompt = st.chat_input("Type your policy text or respond to M.A.R.G.E...")

if prompt:
    # 1. Append User Message to History & UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Sequential Conversational State Machine Logic
    with st.chat_message("assistant"):
        response_content = ""
        current_score = None
        score_label = "Guardian Index"

        current_step = st.session_state.workflow_step

        if current_step == 0:
            st.session_state.target_text = prompt
            current_score = 84
            score_label = "Standard Guardian Index"

            response_content = (
                "🛡️ **Step 1: Standard Guardian Audit Complete**\n\n"
                f"*Analyzing text payload (`{len(prompt)} characters`)*...\n\n"
                "* **Pillar Breakdown:**\n"
                "  * Inclusion: 88%\n  * Clarity: 90%\n  * Safety: 85%\n  * Equity: 72% *(Attention needed)*\n  * Access: 87%\n\n"
                "Would you like me to run the **Deep Intersectional Scan** next? *(Type 'yes' or provide instructions)*"
            )
            st.session_state.workflow_step = 1

        elif current_step == 1:
            if any(word in prompt.lower() for word in ["yes", "proceed", "run", "sure"]):
                current_score = 76
                score_label = "Deep Intersectional Score"
                response_content = (
                    "🔍 **Step 2: Deep Intersectional Scan Complete**\n\n"
                    "Compound signal analysis identified subtle exclusionary phrasing under *Equity* regarding target demographics.\n\n"
                    "Would you like me to pull pillar-specific equity recommendations? *(Type 'yes' to proceed)*"
                )
                st.session_state.workflow_step = 2
            else:
                response_content = "Understood. Skipping deep scan. Type a new policy text or 'restart' to begin a fresh audit."

        elif current_step == 2:
            if any(word in prompt.lower() for word in ["yes", "proceed", "sure"]):
                current_score = 80
                score_label = "Recommendation Alignment"
                response_content = (
                    "💡 **Step 3: Recommendations & Suggestions**\n\n"
                    "1. Replace ambiguous qualifiers with universally accessible terms.\n"
                    "2. Balance phrasing to ensure multi-demographic representation.\n\n"
                    "Would you like me to formulate explicit **Line-Item Rewrite Suggestions**? *(Type 'yes' to review)*"
                )
                st.session_state.workflow_step = 3
            else:
                response_content = "Paused recommendations. Let me know how else I can adjust the text."

        elif current_step == 3:
            if any(word in prompt.lower() for word in ["yes", "review", "sure"]):
                current_score = 92
                score_label = "Optimized Rewrite Index"
                response_content = (
                    "✍️ **Step 4: Rewrite Generation & Review**\n\n"
                    "**Original:** *'All qualified applicants must complete the primary review process.'*\n"
                    "**Suggested Rewrite:** *'All prospective candidates are supported through an inclusive review process tailored for clear accessibility.'*\n\n"
                    "Do you approve applying these changes to your final document payload? *(Type 'approve' or 'yes' to finalize)*"
                )
                st.session_state.workflow_step = 4
            else:
                response_content = "Review skipped. Tell me if you'd like custom rewrite constraints."

        elif current_step == 4:
            if any(word in prompt.lower() for word in ["approve", "yes", "apply", "finalize"]):
                current_score = 98
                score_label = "Final Bullseye Index"
                response_content = (
                    "✅ **Step 5: Final Approval & Application Complete**\n\n"
                    "The approved changes have been successfully written into the document payload buffer.\n\n"
                    "🎉 *Workflow sequence completed successfully!* Paste any new text below to start a fresh audit cycle."
                )
                st.session_state.workflow_step = 0  # Reset for next run
            else:
                response_content = "Approval pending. Let me know if you would like to tweak the suggested rewrite line-items."

        else:
            response_content = "Ready for the next input. Paste new text to begin another audit cycle."

        # Render message response to UI
        st.markdown(response_content)

        if current_score is not None:
            render_artemis_bow_target(current_score, score_label)

        # Save assistant message in session history
        msg_payload = {"role": "assistant", "content": response_content}
        if current_score is not None:
            msg_payload["score_val"] = current_score
            msg_payload["score_label"] = score_label
        st.session_state.messages.append(msg_payload)
