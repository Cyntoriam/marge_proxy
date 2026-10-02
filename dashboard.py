import re
import streamlit as st


st.set_page_config(
    page_title="M.A.R.G.E. | The Equity Guardian",
    page_icon="🏹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state for navigation if not set
if "app_section" not in st.session_state:
    st.session_state.app_section = "🏹 The Guardian Audit"

# Sidebar Configuration & Preferences
with st.sidebar:
    st.header("Visitor Portal")
    visitor_name = st.text_input("Your Name / Handle", value="Pocketdoc", placeholder="Enter your name...")

    st.markdown("---")
    st.header("Navigation Panel")

    # Clean list navigation using clickable buttons styled as list items
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

    sound_enabled = st.toggle("Enable Audio Cues", value=True, help="Plays a gentle ambient chime upon audit completion.")

    selected_mode = st.radio(
        "Evaluation Mode", ["Standard Audit", "Deep Intersectional Scan"]
    )

    if selected_mode == "Deep Intersectional Scan":
        st.info("Deep Scan active: compound intersectional signal review enabled.")
    else:
        st.info("Standard Audit active: baseline Heuristic Equity Evaluation.")

    st.caption("M.A.R.G.E. v2.7 • Multi-sensory equity middleware.")

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
        .about-card, .equity-card, .flagged-card, .guardian-scale-container {
            background-color: #1A120B !important;
            border: 1px solid #3d2417 !important;
            color: #E0E0E0 !important;
        }
        [data-testid="stSidebar"] {
            background-color: #140E0A !important;
            border-right: 1px solid #3d2417 !important;
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
        .about-card, .equity-card, .flagged-card, .guardian-scale-container {
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
            f"Analytical overview: The Heuristic Equity Evaluation marked {len(flagged_pillars)} of 5 pillars for potential signals. These pattern matches serve as prompts for contextual review, not confirmed barriers or findings of bias."
        ]

        if {"Accessibility Justice", "Intersectional Microaggressions"}.issubset(flagged_pillars):
            explanation_blocks.append(
                "Temporal and descriptor signals co-occur. Review their context, whether requirements are job-related, and whether reasonable alternatives or accommodations exist."
            )
        if {"Dialectal Justice", "Stereotypical Framing"}.issubset(flagged_pillars):
            explanation_blocks.append(
                "Language-related and professional-standard signals co-occur. Review how communication criteria are defined and whether they assess job-relevant skills without privileging a particular dialect or style."
            )
        if {"Spatial/Economic Erasure", "Accessibility Justice"}.issubset(flagged_pillars):
            explanation_blocks.append(
                "Geographic and accessibility-related signals co-occur. Review whether location, commute, or schedule requirements could compound barriers for affected people."
            )
        if len(flagged_pillars) >= 3:
            explanation_blocks.append(
                "Signals appeared in at least three pillars. A coordinated review may help determine whether these requirements interact in practice."
            )

        intersectional_explanation = explanation_blocks

        recommendations = [
            f"**{pillar} Rewrite Suggestion:** {PILLAR_RULES[pillar]['rewrite']}"
            for pillar in PILLAR_RULES if pillar in flagged_pillars
        ]
        recommendation_title = "Actionable Pillar Rewrite Suggestions"

        if (
            any(term in content for term in ("velocity", "cadence", "huddles", "vanguard innovation lab"))
            and flagged_pillars.intersection({"Accessibility Justice", "Dialectal Justice", "Stereotypical Framing"})
        ):
            recommendation_title = "Innovation Lab Comprehensive Rewrite Plan"
            lab_specific_note = "<strong>Suggested Inclusive Revision:</strong> 'Seeking collaborative participants for our innovation fellowship. Contributions may be submitted through scheduled syncs or structured asynchronous milestones, supporting diverse communication styles and flexible access.'"
            recommendations.insert(0, lab_specific_note)
        elif flagged_list := [p for p in PILLAR_RULES if p in flagged_pillars]:
            recommendations.append(
                "**Next Step:** Pilot these rewritten guidelines with your review committee before broader publication."
            )

        if not recommendations:
            recommendations.append(
                "No heuristic rules triggered, so no automatic rewrite is suggested. This does not replace contextual human review."
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


# Header
st.markdown(
    """
    <div class="marge-header-card">
        <h1 class="marge-title">M.A.R.G.E. 🏹</h1>
        <div class="marge-fullname">Multimodal Automated Real-time Guardian Engine</div>
        <div class="marge-subtitle">The Equity Guardian</div>
    </div>
    """,
    unsafe_allow_html=True,
)

greeting_name = visitor_name.strip() if visitor_name.strip() else "Traveler"

# View 1: About & User Guide
if app_section == "📖 About & User Guide":
    st.markdown(f"### Welcome to the M.A.R.G.E. Knowledge Base, {greeting_name}!")
    st.markdown(
        "M.A.R.G.E. is designed to be intuitive, accessible, and interactive. Here is how to navigate your session:"
    )

    st.markdown(
        """
        <div class="about-card" style="padding: 1.5rem; border-radius: 8px; margin-bottom: 1.2rem;">
            <h3 style="margin-top:0; color: #D9531E;">1. Personalize Your Session</h3>
            <p>In the sidebar under <b>Visitor Portal</b>, enter your name or handle. M.A.R.G.E. greets you personally and tailors the audit context.</p>
        </div>
        <div class="about-card" style="padding: 1.5rem; border-radius: 8px; margin-bottom: 1.2rem;">
            <h3 style="margin-top:0; color: #D9531E;">2. Choose Theme & Accessibility Cues</h3>
            <p>Toggle between <b>Dark (Oshun Sunrise)</b> and <b>Light (Radiant Day)</b> themes, and enable/disable ambient audio feedback in the sidebar controls.</p>
        </div>
        <div class="about-card" style="padding: 1.5rem; border-radius: 8px; margin-bottom: 1.2rem;">
            <h3 style="margin-top:0; color: #D9531E;">3. Select Evaluation Mode & Use Voice Features</h3>
            <p>Use the <b>🎤 Speak-to-Text</b> button inside the payload box to dictate text, and use the <b>🔊 Read Results Aloud</b> feature for screen-reading support.</p>
        </div>
        <div class="about-card" style="padding: 1.5rem; border-radius: 8px; margin-bottom: 1.2rem;">
            <h3 style="margin-top:0; color: #D9531E;">4. Run the Guardian Audit & Rewrites</h3>
            <p>Paste or dictate text payloads to check for access barriers and receive specific, actionable rewrite suggestions.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# View 2: The Main Guardian Audit Dashboard
else:
    st.markdown(f"### Hello, {greeting_name}! Welcome to M.A.R.G.E.")
    st.markdown(
        "M.A.R.G.E. stands ready as your equity guardian. Results serve as prompts for human review, not absolute certifications of fairness."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="chat-input-container">
            <div style="color: #D9531E; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.4rem;">
                🏹 What text, policy, or vision are we guarding today, {greeting_name}?
            </div>
            <div style="font-size: 0.9rem; margin-bottom: 0.8rem; opacity: 0.8;">
                Drop your program description, job posting, or community plan below (or use speech-to-text). M.A.R.G.E. will scan it across the Five-Pillar Taxonomy and provide rewrite suggestions.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Speech-to-Text & Text Area HTML Integration
    st.markdown(
        """
        <div style="margin-bottom: 0.5rem;">
            <button onclick="startDictation()" style="background: linear-gradient(135deg, #D9531E 0%, #C84512 100%); color: white; border: none; padding: 0.5rem 1rem; border-radius: 6px; font-weight: 600; cursor: pointer; box-shadow: 0 4px 12px rgba(217, 83, 30, 0.3);">
                🎤 Click to Speak / Dictate Text
            </button>
            <span id="speechStatus" style="margin-left: 1rem; font-size: 0.9rem; font-style: italic; opacity: 0.8;"></span>
        </div>
        <script>
            function startDictation() {
                if (window.hasOwnProperty('webkitSpeechRecognition')) {
                    var recognition = new webkitSpeechRecognition();
                    recognition.continuous = false;
                    recognition.interimResults = false;
                    recognition.lang = "en-US";
                    recognition.start();
                    document.getElementById("speechStatus").innerText = "Listening... Speak now.";

                    recognition.onresult = function(e) {
                        var transcript = e.results[0][0].transcript;
                        const textarea = document.querySelector('textarea');
                        if (textarea) {
                            textarea.value = textarea.value ? textarea.value + " " + transcript : transcript;
                            textarea.dispatchEvent(new Event('input', { bubbles: true }));
                        }
                        document.getElementById("speechStatus").innerText = "Dictation captured successfully!";
                        recognition.stop();
                    };

                    recognition.onerror = function(e) {
                        document.getElementById("speechStatus").innerText = "Speech recognition error. Please try again.";
                        recognition.stop();
                    }
                } else {
                    document.getElementById("speechStatus").innerText = "Speech recognition not supported in this browser.";
                }
            }
        </script>
        """,
        unsafe_allow_html=True,
    )

    user_payload = st.text_area(
        "Payload Content Box",
        placeholder="Type, paste, or dictate text here...",
        height=160,
        label_visibility="collapsed",
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        run_audit = st.button("Run Equity Audit", type="primary")

    if run_audit:
        if not user_payload.strip():
            st.error("Please enter some text before running the audit.")
        else:
            if sound_enabled:
                st.markdown(
                    """
                    <audio autoplay style="display:none;">
                        <source src="https://actions.google.com/sounds/v1/ambiences/morning_birds.ogg" type="audio/ogg">
                    </audio>
                    """,
                    unsafe_allow_html=True,
                )

            with st.spinner(f"M.A.R.G.E. is executing {selected_mode.lower()}..."):
                results = evaluate_equity_payload(user_payload, mode=selected_mode)

            if "error" in results:
                st.warning(results["error"])
            else:
                st.success(f"{selected_mode} complete for {greeting_name}.")
                signal_index = results["guardian_signal_index"]
                arrow_position = min(max(signal_index, 2), 98)
                matched_pillar_count = results["matched_pillar_count"]

                # Prepare summary text for the screen reader
                summary_speech_text = f"Audit complete for {greeting_name}. Guardian Index is {signal_index} out of 100, with {matched_pillar_count} of 5 pillar groups matching heuristic rules."

                st.markdown(
                    f"""
                    <div class="guardian-scale-container" style="padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; text-align: center;">
                        <div style="color: #D9531E; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
                            Guardian Index
                        </div>
                        <div style="font-size: 1.6rem; font-weight: 700; margin-top: 0.5rem;">
                            {signal_index} / 100
                        </div>
                        <div style="opacity: 0.8;">
                            {matched_pillar_count} of 5 pillar groups matched heuristic rules
                        </div>
                        <div class="scale-track">
                            <div class="guardian-arrow-marker" style="left: {arrow_position}%">🏹</div>
                        </div>
                        <div class="scale-labels" style="display: flex; justify-content: space-between; font-size: 0.8rem; opacity: 0.8;">
                            <span>0 groups matched</span>
                            <span>2-3 groups matched</span>
                            <span>5 groups matched</span>
                        </div>
                        <div style="font-size: 0.85rem; margin-top: 1rem; opacity: 0.7;">
                            Heuristic pattern count only. This is not an equity score or risk probability.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Text-to-Speech / Screen Reader Button Widget
                full_results_text = f"Guardian Index {signal_index} out of 100. {matched_pillar_count} pillar groups matched. "
                for pillar, details in results["assessment"].items():
                    full_results_text += f"{pillar}: {details['status']}. "
                    if details['rewrite']:
                        full_results_text += f"Suggested rewrite: {details['rewrite']} "

                safe_speech_string = full_results_text.replace('"', '\\"').replace("'", "\\'")
                st.markdown(
                    f"""
                    <div style="margin-bottom: 1.5rem; text-align: center;">
                        <button onclick="speakResults('{safe_speech_string}')" style="background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%); color: #0D0D0D; border: none; padding: 0.6rem 1.2rem; border-radius: 6px; font-weight: 700; cursor: pointer; box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3);">
                            🔊 Read Results Aloud (Screen Reader)
                        </button>
                        <button onclick="window.speechSynthesis.cancel()" style="background: transparent; color: inherit; border: 1px solid #D9531E; padding: 0.6rem 1rem; border-radius: 6px; font-weight: 600; cursor: pointer; margin-left: 0.5rem;">
                            ⏹ Stop Speech
                        </button>
                    </div>
                    <script>
                        function speakResults(textToSpeak) {{
                            if ('speechSynthesis' in window) {{
                                window.speechSynthesis.cancel();
                                var utterance = new SpeechSynthesisUtterance(textToSpeak);
                                utterance.rate = 1.0;
                                window.speechSynthesis.speak(utterance);
                            }} else {{
                                alert('Text-to-speech is not supported by your browser.');
                            }}
                        }}
                    </script>
                    """,
                    unsafe_allow_html=True,
                )

                intersectional_explanation = results["intersectional_explanation"]
                if intersectional_explanation:
                    explanation_html = "<br><br>".join(intersectional_explanation)
                    st.markdown(
                        f"""
                        <div class="intersectional-banner" style="background: rgba(217, 83, 30, 0.08);">
                            <strong>Deep Intersectional Explanatory Breakdown</strong><br><br>
                            {explanation_html}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                recommendations = results["recommendations"]
                if recommendations:
                    recommendations_html = "<br><br>".join(recommendations)
                    recommendation_title = results.get("recommendation_title") or "Pillar-Specific Rewrite Suggestions"
                    st.markdown(
                        f"""
                        <div class="recommendation-banner" style="background: rgba(76, 175, 80, 0.08);">
                            <strong>{recommendation_title}</strong><br><br>
                            {recommendations_html}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown("### Five-Pillar Evaluation Results & Rewrites")
                st.caption(
                    f"Mode: {selected_mode} | Payload length: {results['payload_length']} characters"
                )
                for pillar, details in results["assessment"].items():
                    is_flagged = details["status"] == "Potential signal"
                    card_class = "flagged-card" if is_flagged else "equity-card"
                    status_color = "#E57373" if is_flagged else "#D9531E"

                    rewrite_html = f"<br><span style='color: #81C784; font-size: 0.9rem;'><strong>Suggested Rewrite:</strong> {details['rewrite']}</span>" if is_flagged else ""

                    st.markdown(
                        f"""
                        <div class="{card_class}" style="padding: 1.1rem; border-radius: 6px; margin-bottom: 0.8rem; border-left: 4px solid {status_color};">
                            <strong>{pillar}</strong><br>
                            <span style="color: {status_color};">Status: {details['status']}</span><br>
                            <span style="font-size: 0.9rem; opacity: 0.85;">{details['note']}</span>
                            {rewrite_html}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                st.warning(
                    "This Heuristic Equity Evaluation can miss contextual or implicit harms and can flag benign wording. Have affected people and domain experts review consequential decisions."
                )

st.markdown("---")
st.caption("M.A.R.G.E. Middleware Dashboard • Multi-sensory Equity Guardian Engine")
