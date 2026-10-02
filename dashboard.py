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
        /* Force the main app background */
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
        
        /* Ensure blocks and containers pick up the rich dark contrast */
        .marge-header-card {
            background: linear-gradient(135deg, #1A120B 0%, #141414 100%) !important;
            border: 2px solid #D9531E !important;
            padding: 2.5rem 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 15px 40px rgba(217, 83, 30, 0.18);
        }
        .marge-title {
            color: #FFB347 !important;
            font-family: Georgia, serif;
            font-size: 3rem;
            font-weight: 800;
            margin: 0;
            text-shadow: 0 2px 15px rgba(217, 83, 30, 0.4);
        }
        .marge-fullname {
            color: #D9531E !important;
            font-size: 1.05rem;
            font-weight: 600;
            text-transform: uppercase;
            margin-top: 0.5rem;
            margin-bottom: 0.75rem;
            letter-spacing: 1px;
        }
        .marge-subtitle {
            color: #D4AF37 !important;
            font-size: 1.1rem;
            margin: 0 0 0.3rem;
            font-style: italic;
        }
        .chat-input-container {
            background: rgba(26, 18, 14, 0.85) !important;
            border: 1px solid #D9531E !important;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            box-shadow: 0 8px 25px rgba(217, 83, 30, 0.12);
        }
        .about-card {
            background: rgba(26, 18, 14, 0.9) !important;
            border: 1px solid #3d2417 !important;
            border-left: 4px solid #D9531E !important;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.2rem;
            line-height: 1.6;
        }
        [data-testid="stSidebar"] {
            background-color: #140E0A !important;
            border-right: 1px solid #3d2417 !important;
        }
        .stButton > button {
            background: linear-gradient(135deg, #D9531E 0%, #C84512 100%) !important;
            color: #FFFFFF !important;
            font-weight: 600;
            border: none;
            border-radius: 6px;
            padding: 0.5rem 1rem;
            transition: all 0.2s ease;
            box-shadow: 0 4px 12px rgba(217, 83, 30, 0.3);
        }
        .equity-card {
            background-color: #1A120B !important;
            border: 1px solid #3d2417 !important;
            border-left: 4px solid #D4AF37 !important;
            padding: 1.1rem;
            border-radius: 6px;
            margin-bottom: 0.8rem;
        }
        .flagged-card {
            background-color: #1A120B !important;
            border: 1px solid #553333 !important;
            border-left: 4px solid #E57373 !important;
            padding: 1.1rem;
            border-radius: 6px;
            margin-bottom: 0.8rem;
        }
        .intersectional-banner {
            background: rgba(217, 83, 30, 0.12) !important;
            border: 1px solid #D9531E !important;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            color: #E0E0E0 !important;
            line-height: 1.6;
        }
        .recommendation-banner {
            background: rgba(76, 175, 80, 0.1) !important;
            border: 1px solid #81C784 !important;
            padding: 1rem;
            border-radius: 8px;
            margin: 1.5rem 0;
            color: #E0E0E0 !important;
            line-height: 1.6;
        }
        .guardian-scale-container {
            background-color: #1A120B !important;
            border: 1px solid #D9531E !important;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            text-align: center;
            box-shadow: 0 8px 25px rgba(217, 83, 30, 0.1);
        }
        .scale-track {
            position: relative;
            width: 100%;
            height: 16px;
            background: linear-gradient(90deg, #D4AF37 0%, #D9531E 55%, #E57373 100%) !important;
            border-radius: 8px;
            margin: 2rem 0 1rem;
        }
        .guardian-arrow-marker {
            position: absolute;
            top: -28px;
            transform: translateX(-50%);
            font-size: 1.8rem;
            transition: left 0.8s cubic-bezier(0.4, 0, 0.2, 1);
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
            r"relocat\w*|suburban|headquarters|corridor|downtown|commute|"
            r"on[- ]?site|campus hub)\b",
        ),
        "deep_patterns": (r"\b(?:food desert|transit desert|service desert)\b",),
        "note": "Location, service access, or economic exclusion language needs context review.",
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
    },
    "Dialectal Justice": {
        "patterns": (
            r"\b(?:accent|grammar|non[- ]standard dialect|speak properly|"
            r"native speaker|broken english|dialect|vernacular|prose|"
            r"communication rhythms|polished clarity|direct|discourse|cadence)\b",
        ),
        "deep_patterns": (r"\b(?:professional language|clear english|communication style)\b",),
        "note": "Language-variety terms can be used to unfairly judge dialect or fluency; review context.",
    },
}


def evaluate_equity_payload(text: str, mode: str = "Standard Audit") -> dict:
    """Run a Heuristic Equity Evaluation across the five-pillar taxonomy."""
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

        if {
            "Accessibility Justice",
            "Intersectional Microaggressions",
        }.issubset(flagged_pillars):
            explanation_blocks.append(
                "Temporal and descriptor signals co-occur. Review their context, whether requirements are job-related, and whether reasonable alternatives or accommodations exist."
            )
        if {
            "Dialectal Justice",
            "Stereotypical Framing",
        }.issubset(flagged_pillars):
            explanation_blocks.append(
                "Language-related and professional-standard signals co-occur. Review how communication criteria are defined and whether they assess job-relevant skills without privileging a particular dialect or style."
            )
        if {
            "Spatial/Economic Erasure",
            "Accessibility Justice",
        }.issubset(flagged_pillars):
            explanation_blocks.append(
                "Geographic and accessibility-related signals co-occur. Review whether location, commute, or schedule requirements could compound barriers for affected people."
            )
        if len(flagged_pillars) >= 3:
            explanation_blocks.append(
                "Signals appeared in at least three pillars. A coordinated review may help determine whether these requirements interact in practice."
            )

        intersectional_explanation = explanation_blocks
        recommendation_by_pillar = {
            "Spatial/Economic Erasure": "Review whether location, commute, or relocation requirements are essential; consider equivalent access paths where practical.",
            "Intersectional Microaggressions": "Replace subjective culture or presence language with observable, role-related criteria.",
            "Accessibility Justice": "Clarify essential timing or pace, consider structured alternatives, and document available accommodations.",
            "Stereotypical Framing": "Define advancement and performance criteria using consistent, role-related outcomes.",
            "Dialectal Justice": "Assess communication only where relevant to the role; specify the skill and accept equivalent dialects and styles.",
        }
        flagged_list = [
            pillar for pillar in PILLAR_RULES if pillar in flagged_pillars
        ]
        recommendations = [
            f"{pillar}: {recommendation_by_pillar[pillar]}"
            for pillar in flagged_list
        ]
        recommendation_title = "Pillar-Specific Remediation Recommendations"

        if (
            any(term in content for term in ("velocity", "cadence", "huddles", "vanguard innovation lab"))
            and flagged_pillars.intersection(
                {
                    "Accessibility Justice",
                    "Dialectal Justice",
                    "Stereotypical Framing",
                }
            )
        ):
            recommendation_title = "Innovation Lab Participation Review"
            recommendations = [
                f"Potential signals appeared in: {', '.join(flagged_list)}.",
                "If velocity, cadence, or huddles are participation expectations, clarify their purpose and consider outcome-based milestones, scheduled collaboration, and asynchronous ways to contribute.",
            ]
        elif flagged_list:
            recommendations.append(
                "Scale-up review: Pilot the proposed changes with affected participants, assign an accountable owner, and review similar materials before adopting a broader policy."
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

# Sidebar Navigation Panel & Visitor Config
with st.sidebar:
    st.header("Navigation Panel")
    app_section = st.radio(
        "Go to", ["🏹 The Guardian Audit", "📖 About & User Guide"]
    )
    
    st.markdown("---")
    st.header("Visitor Portal")
    visitor_name = st.text_input("Your Name / Handle", value="Traveler", placeholder="Enter your name...")
    
    st.markdown("---")
    st.header("Guardian Controls")
    selected_mode = st.radio(
        "Evaluation Mode", ["Standard Audit", "Deep Intersectional Scan"]
    )
    if selected_mode == "Deep Intersectional Scan":
        st.info("Deep Scan active: compound intersectional signal review enabled.")
    else:
        st.info("Standard Audit active: baseline Heuristic Equity Evaluation.")
    st.caption("Oshun theme active: charcoal, honey-gold, and warm radiance.")
    st.caption("Self-contained mode: no external request needed.")

greeting_name = visitor_name.strip() if visitor_name.strip() else "Traveler"

# View 1: About & User Guide (How to Use M.A.R.G.E.)
if app_section == "📖 About & User Guide":
    st.markdown(f"### Welcome to the M.A.R.G.E. Knowledge Base, {greeting_name}!")
    st.markdown(
        "Much like modern AI assistants (ChatGPT, Gemini, etc.), M.A.R.G.E. is designed to be intuitive, accessible, and interactive. Here is a quick guide on how to navigate and get the most out of your Guardian session:"
    )

    st.markdown(
        """
        <div class="about-card">
            <h3 style="margin-top:0; color: #FFD700;">1. Personalize Your Session</h3>
            <p>In the sidebar under <b>Visitor Portal</b>, enter your name or handle. M.A.R.G.E. greets you personally and tailors the audit context to your workflow.</p>
        </div>
        <div class="about-card">
            <h3 style="margin-top:0; color: #FFD700;">2. Choose Your Evaluation Mode</h3>
            <p><b>Standard Audit:</b> Performs a baseline Heuristic Equity Evaluation across the Five-Pillar Taxonomy to flag potential access barriers.<br>
            <b>Deep Intersectional Scan:</b> Activates compound co-occurrence analysis, evaluating how multiple overlapping terms interact in practice.</p>
        </div>
        <div class="about-card">
            <h3 style="margin-top:0; color: #FFD700;">3. Ask What You're Guarding</h3>
            <p>Use the main input box to paste text payloads—such as job postings, fellowship bylaws, innovation lab expectations, or community development drafts—and click <b>Run Equity Audit</b>.</p>
        </div>
        <div class="about-card">
            <h3 style="margin-top:0; color: #FFD700;">4. Interpret the Guardian Index</h3>
            <p>The resulting <b>Guardian Index (0-100)</b> and arrow marker indicate how many pillar groups triggered pattern rules. Remember: these are prompts for thoughtful human review, not absolute fairness scores or automated certifications.</p>
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

    # Creative Social-Style Prompt Section ("What's on your mind?")
    st.markdown(
        f"""
        <div class="chat-input-container">
            <div style="color: #FFD700; font-weight: 700; font-size: 1.1rem; margin-bottom: 0.4rem;">
                🏹 What text, policy, or vision are we guarding today, {greeting_name}?
            </div>
            <div style="color: #AAAAAA; font-size: 0.9rem; margin-bottom: 0.8rem;">
                Drop your program description, job posting, or community plan below. M.A.R.G.E. will scan it across the Five-Pillar Taxonomy for potential equity signals.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    user_payload = st.text_area(
        "Payload Content Box",
        placeholder="Type or paste text here (e.g., fellowship requirements, community blueprint, team communication norms)...",
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
            with st.spinner(f"M.A.R.G.E. is executing {selected_mode.lower()}..."):
                results = evaluate_equity_payload(user_payload, mode=selected_mode)

            if "error" in results:
                st.warning(results["error"])
            else:
                st.success(f"{selected_mode} complete for {greeting_name}.")
                signal_index = results["guardian_signal_index"]
                arrow_position = min(max(signal_index, 2), 98)
                matched_pillar_count = results["matched_pillar_count"]
                
                st.markdown(
                    f"""
                    <div class="guardian-scale-container">
                        <div style="color: #D4AF37; font-weight: 600; text-transform: uppercase;">
                            Guardian Index
                        </div>
                        <div style="font-size: 1.6rem; font-weight: 700; color: #FFD700; margin-top: 0.5rem;">
                            {signal_index} / 100
                        </div>
                        <div style="color: #CCCCCC;">
                            {matched_pillar_count} of 5 pillar groups matched heuristic rules
                        </div>
                        <div class="scale-track">
                            <div class="guardian-arrow-marker" style="left: {arrow_position}%">🏹</div>
                        </div>
                        <div class="scale-labels">
                            <span>0 groups matched</span>
                            <span>2-3 groups matched</span>
                            <span>5 groups matched</span>
                        </div>
                        <div style="color: #A0A0A0; font-size: 0.85rem; margin-top: 1rem;">
                            Heuristic pattern count only. This is not an equity score or risk probability; no matches do not establish complete safety.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
                intersectional_explanation = results["intersectional_explanation"]
                if intersectional_explanation:
                    explanation_html = "<br><br>".join(intersectional_explanation)
                    st.markdown(
                        f"""
                        <div class="intersectional-banner">
                            <strong>Deep Intersectional Explanatory Breakdown</strong><br><br>
                            {explanation_html}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    
                recommendations = results["recommendations"]
                if recommendations:
                    recommendations_html = "<br><br>".join(recommendations)
                    recommendation_title = results.get("recommendation_title") or "Pillar-Specific Recommendations"
                    st.markdown(
                        f"""
                        <div class="recommendation-banner">
                            <strong>{recommendation_title}</strong><br><br>
                            {recommendations_html}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    
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
                    "This Heuristic Equity Evaluation can miss contextual or implicit harms and can flag benign wording. Have affected people and domain experts review consequential decisions."
                )

st.markdown("---")
st.caption("M.A.R.G.E. Middleware Dashboard • Self-contained Heuristic Equity Evaluation")