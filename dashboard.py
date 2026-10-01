import re

import streamlit as st


st.set_page_config(
    page_title="M.A.R.G.E. | The Equity Guardian",
    page_icon="🏹",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .stApp {
            background-color: #121212;
            color: #E0E0E0;
        }
        .marge-header-card {
            background: linear-gradient(135deg, #1A1A1A 0%, #161616 100%);
            border: 2px solid #D4AF37;
            padding: 2.5rem 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(212, 175, 55, 0.15);
        }
        .marge-title {
            color: #FFD700 !important;
            font-family: Georgia, serif;
            font-size: 3rem;
            font-weight: 800;
            margin: 0;
            text-shadow: 0 2px 10px rgba(212, 175, 55, 0.3);
        }
        .marge-fullname {
            color: #D4AF37;
            font-size: 1.05rem;
            font-weight: 600;
            text-transform: uppercase;
            margin-top: 0.5rem;
            margin-bottom: 0.75rem;
        }
        .marge-subtitle {
            color: #CCCCCC;
            font-size: 1.1rem;
            margin: 0 0 0.3rem;
            font-style: italic;
        }
        .marge-tagline {
            color: #999999;
            font-size: 0.95rem;
            margin: 0;
        }
        @media (max-width: 640px) {
            .marge-header-card {
                padding: 1.75rem 1rem;
            }
            .marge-title {
                font-size: 2.1rem;
            }
            .marge-fullname {
                font-size: 0.85rem;
            }
        }
        h2, h3 {
            color: #D4AF37 !important;
            font-weight: 600;
        }
        [data-testid="stSidebar"] {
            background-color: #1A1A1A;
            border-right: 1px solid #333333;
        }
        .stButton > button {
            background-color: #D4AF37;
            color: #121212;
            font-weight: 600;
            border: none;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            transition: background-color 0.2s ease;
        }
        .stButton > button:hover {
            background-color: #C5A028;
            color: #000000;
        }
        .equity-card {
            background-color: #1E1E1E;
            border: 1px solid #333333;
            border-left: 4px solid #D4AF37;
            padding: 1.1rem;
            border-radius: 6px;
            margin-bottom: 0.8rem;
        }
        .flagged-card {
            background-color: #1E1E1E;
            border: 1px solid #553333;
            border-left: 4px solid #E57373;
            padding: 1.1rem;
            border-radius: 6px;
            margin-bottom: 0.8rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


PILLAR_RULES = {
    "Spatial/Economic Erasure": {
        "patterns": (
            r"\b(?:bypass|exclude|exclusion|peripheral|low[- ]density|"
            r"underserved|redlin\w*|low[- ]income|order volume is low|"
            r"relocat\w*|suburban|headquarters|corridor|downtown|commute)\b",
        ),
        "deep_patterns": (r"\b(?:food desert|transit desert|service desert)\b",),
        "note": "Location, service access, or economic exclusion language needs context review.",
    },
    "Intersectional Microaggressions": {
        "patterns": (
            r"\b(?:aggressive|articulate|unprofessional|emotional|polished|"
            r"assertive|traditional university|pedigree|assimilation|backward|"
            r"culture|prestige)\b",
        ),
        "deep_patterns": (r"\b(?:angry woman|angry black|culture fit)\b",),
        "note": "Potentially subjective descriptors can carry different implications across identities.",
    },
    "Accessibility Justice": {
        "patterns": (
            r"\b(?:without accommodations|no accommodations|inaccessible|"
            r"wheelchair|screen reader|captions|disability|disabled|hour\w*|"
            r"on[- ]site|schedule|subtitles|transcript|fast[- ]paced)\b",
        ),
        "deep_patterns": (r"\b(?:cognitive access|assistive technology|accessible format)\b",),
        "note": "Accessibility-related language was found; review whether the described needs are supported.",
    },
    "Stereotypical Framing": {
        "patterns": (
            r"\b(?:all women|all men|women are naturally|men are naturally|"
            r"older workers|young and energetic|professional appearance|"
            r"leadership roles|standard|traditional)\b",
        ),
        "deep_patterns": (
            r"\b(?:naturally suited|born to|people like them|aggressive)\b",
        ),
        "note": "Generalizations or appearance criteria may encode assumptions about a group.",
    },
    "Dialectal Justice": {
        "patterns": (
            r"\b(?:accent|grammar|non[- ]standard dialect|speak properly|"
            r"native speaker|broken english|dialect|vernacular|prose|"
            r"communication rhythms)\b",
        ),
        "deep_patterns": (r"\b(?:professional language|clear english|communication style)\b",),
        "note": "Language-variety terms can be used to unfairly judge dialect or fluency; review context.",
    },
}


def evaluate_equity_payload(text: str, deep_scan: bool = False) -> dict:
    """Run a lightweight keyword screen; this is not a semantic fairness audit."""
    if len(text.strip()) < 10:
        return {"error": "Please provide at least 10 characters for a useful keyword screen."}

    content = text.lower()
    assessment = {}
    for pillar, rules in PILLAR_RULES.items():
        patterns = rules["patterns"]
        if deep_scan:
            patterns += rules["deep_patterns"]
        detected = any(re.search(pattern, content) for pattern in patterns)
        assessment[pillar] = {
            "status": "Potential signal" if detected else "No keyword signal detected",
            "note": rules["note"] if detected else "No matching terms found; this is not evidence that the content is equitable.",
        }

    return {"payload_length": len(text), "assessment": assessment}


st.markdown(
    """
    <div class="marge-header-card">
        <h1 class="marge-title">M.A.R.G.E. 🏹</h1>
        <div class="marge-fullname">Multimodal Automated Real-time Guardian Engine</div>
        <div class="marge-subtitle">The Equity Guardian</div>
        <div class="marge-tagline">Sociotechnical Middleware</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    "Welcome, Dr. C. M.A.R.G.E. is running a local keyword screen. Results are prompts for human review, not a certification of fairness."
)

with st.sidebar:
    st.header("Guardian Controls")
    st.markdown("---")
    selected_mode = st.radio(
        "Evaluation Mode", ["Standard Audit", "Deep Intersectional Scan"]
    )
    st.info("Oshun theme active: charcoal and honey-gold.")
    st.caption("Self-contained mode: no API request or external service is used.")

user_payload = st.text_area(
    "Enter text payload for equity audit:",
    placeholder="Paste text here to screen against the Five-Pillar Taxonomy...",
    height=160,
)

if st.button("Run Equity Audit", type="primary"):
    if not user_payload.strip():
        st.error("Please enter some text before running the audit.")
    else:
        with st.spinner("M.A.R.G.E. is screening the payload..."):
            results = evaluate_equity_payload(
                user_payload,
                deep_scan=selected_mode == "Deep Intersectional Scan",
            )

        if "error" in results:
            st.warning(results["error"])
        else:
            st.success("Keyword screen complete.")
            st.markdown("### Five-Pillar Evaluation Results")
            st.caption(
                f"Mode: {selected_mode} | Payload length: {results['payload_length']} characters"
            )
            for pillar, details in results["assessment"].items():
                is_flagged = details["status"] == "Potential signal"
                card_class = "flagged-card" if is_flagged else "equity-card"
                status_color = "#E57373" if is_flagged else "#D4AF37"
                note_color = "#DDDDDD" if is_flagged else "#A0A0A0"
                st.markdown(
                    f"""
                    <div class="{card_class}">
                        <strong>{pillar}</strong><br>
                        <span style="color: {status_color};">Status: {details['status']}</span><br>
                        <span style="color: {note_color}; font-size: 0.9rem;">{details['note']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            st.warning(
                "This local keyword screen can miss contextual or implicit harms and can flag benign wording. Have affected people and domain experts review consequential decisions."
            )

st.markdown("---")
st.caption("M.A.R.G.E. Middleware Dashboard • Self-contained keyword screening")