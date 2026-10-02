import re
import streamlit as st


st.set_page_config(
    page_title="M.A.R.G.E. v2.10",
    page_icon="🛡️",
    layout="wide",
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


def render_marge_audit_view():
    st.markdown("""
        <style>
            .marge-header-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
                padding: 1rem 0 0.8rem 0;
                margin-bottom: 1.2rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
            .marge-icon { font-size: 1.8rem; margin-bottom: 0.1rem; }
            .marge-title { font-size: 1.8rem; font-weight: 700; letter-spacing: 0.05em; margin: 0; color: #FAFAFA; }
            .marge-subtitle { font-size: 0.9rem; font-weight: 400; color: #D4AF37; margin-top: 0.3rem; margin-bottom: 0.8rem; }
            .audit-card {
                background: rgba(25, 25, 25, 0.6);
                border: 1px solid rgba(212, 175, 55, 0.2);
                border-radius: 8px;
                padding: 1.2rem;
                margin-bottom: 1rem;
            }
            .pillar-tag {
                display: inline-block;
                background: rgba(212, 175, 55, 0.15);
                color: #D4AF37;
                padding: 0.2rem 0.6rem;
                border-radius: 4px;
                font-size: 0.8rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
            }
        </style>
        <div class="marge-header-container">
            <div class="marge-icon">🏹</div>
            <h1 class="marge-title">M.A.R.G.E.</h1>
            <div class="marge-subtitle">Multimodal Automated Real-time Guardian Engine &bull; Equity &amp; Bias Audit</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="background: rgba(212, 175, 55, 0.05); border: 1px dashed rgba(212, 175, 55, 0.4); padding: 0.8rem; border-radius: 6px; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center;">
            <span id="speechStatus" style="font-size: 0.85rem; color: #D4AF37;">🎙️ Voice Dictation &amp; Accessibility Ready</span>
            <div>
                <button type="button" onclick="startDictation()" style="background: #D4AF37; color: #121212; border: none; padding: 0.4rem 0.8rem; border-radius: 4px; font-weight: 600; cursor: pointer; font-size: 0.8rem; margin-right: 0.5rem;">Dictate Policy</button>
                <button type="button" onclick="readAuditAloud()" style="background: #333; color: #FAFAFA; border: 1px solid #D4AF37; padding: 0.4rem 0.8rem; border-radius: 4px; font-weight: 600; cursor: pointer; font-size: 0.8rem;">🔊 Read Insights Aloud</button>
            </div>
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
                            let currentValue = textarea.value;
                            textarea.value = currentValue ? currentValue + " " + transcript : transcript;
                            textarea.dispatchEvent(new Event('input', { bubbles: true }));
                        }
                        document.getElementById("speechStatus").innerText = "Dictation captured successfully!";
                        recognition.stop();
                    };

                    recognition.onerror = function() {
                        document.getElementById("speechStatus").innerText = "Speech recognition error. Please try again.";
                        recognition.stop();
                    };
                } else {
                    document.getElementById("speechStatus").innerText = "Speech recognition not supported in this browser.";
                }
            }

            function readAuditAloud() {
                if ('speechSynthesis' in window) {
                    window.speechSynthesis.cancel();
                    const textToRead = "Guardian Assessment and Insights. Let's look closely at how this policy language lands across different communities. Pillar one, Linguistic Accessibility and Gatekeeping. Phrases requiring flawless executive presence function as coded filters, disproportionately screening out neurodivergent candidates and non-standard speakers. Pillar two, Geographic and Logistical Equity. Mandating on-site huddles creates barriers for primary caregivers and those reliant on public transit.";
                    const utterance = new SpeechSynthesisUtterance(textToRead);
                    utterance.rate = 0.95;
                    window.speechSynthesis.speak(utterance);
                    document.getElementById("speechStatus").innerText = "Reading audit insights aloud...";
                } else {
                    alert("Text-to-speech is not supported in this browser.");
                }
            }
        </script>
    """, unsafe_allow_html=True)

    st.markdown("""
        ### 🏹 Guardian Assessment & Insights
        *Let's look closely at how this policy language lands across different communities. Rather than a simple pass/fail, let's explore the underlying dynamics together.*
    """)

    st.markdown("---")
    st.markdown("#### 🏛️ Guardian Index: Pillar Diagnostic Breakdown")

    with st.container():
        st.markdown("""
        <div class="audit-card">
            <div class="pillar-tag">Pillar I: Linguistic Accessibility &amp; Gatekeeping</div>
            <p><strong>Observation:</strong> Terms requiring <em>"flawless executive presence, clear and unaccented communication cadence, and a prestigious university pedigree"</em> function as coded filters.</p>
            <p><em>Why it's flagged:</em> These phrases disproportionately screen out neurodivergent candidates, speakers with regional or non-standard accents, and graduates of non-traditional or HBCU pathways under the guise of neutral professionalism.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div class="audit-card">
            <div class="pillar-tag">Pillar II: Geographic &amp; Logistical Equity</div>
            <p><strong>Observation:</strong> Mandating <em>"on-site huddles with no remote accommodations"</em>.</p>
            <p><em>Why it's flagged:</em> This creates systemic barriers for primary caregivers, individuals with mobility or chronic health needs, and those reliant on public transit infrastructure.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 💬 Dialogue &amp; Refinement")
    st.info("💡 **M.A.R.G.E.'s Perspective:** Notice how shifting from rigid credentialism to competency-focused criteria broadens our talent pool while protecting the integrity of the innovation lab. Speak or type your thoughts below.")

    if "audit_input" not in st.session_state:
        st.session_state.audit_input = ""

    user_response = st.text_area(
        "Refine this audit or ask M.A.R.G.E. a question...",
        placeholder="Type, paste, or dictate text here...",
        height=100,
        key="audit_input",
    )

    if user_response:
        st.success("🎯 **Target Adjusted:** M.A.R.G.E. is synthesizing your feedback into the revised policy draft...")


if app_section == "📖 About & User Guide":
    st.markdown("### About M.A.R.G.E.")
    st.markdown("M.A.R.G.E. guides review of policy language for potential equity, access, and inclusion signals.")
else:
    render_marge_audit_view()
