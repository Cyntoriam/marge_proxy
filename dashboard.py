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
        .intersectional-banner {
            background: rgba(212, 175, 55, 0.08);
            border: 1px solid #D4AF37;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            color: #E0E0E0;
            line-height: 1.6;
        }
        .recommendation-banner {
            background: rgba(76, 175, 80, 0.08);
            border: 1px solid #81C784;
            padding: 1rem;
            border-radius: 8px;
            margin: 1.5rem 0;
            color: #E0E0E0;
            line-height: 1.6;
        }
        .artemis-scale-container {
            background-color: #1A1A1A;
            border: 1px solid #D4AF37;
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        .scale-track {
            position: relative;
            width: 100%;
            height: 16px;
            background: linear-gradient(90deg, #D4AF37 0%, #E89B50 55%, #E57373 100%);
            border-radius: 8px;
            margin: 2rem 0 1rem;
        }
        .artemis-arrow-marker {
            position: absolute;
            top: -28px;
            transform: translateX(-50%);
            font-size: 1.8rem;
            transition: left 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .scale-labels {
            display: flex;
            justify-content: space-between;
            gap: 0.5rem;
            color: #999999;
            font-size: 0.8rem;
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
            r"on[- ]?site)\b",
        ),
        "deep_patterns": (r"\b(?:food desert|transit desert|service desert)\b",),
        "note": "Location, service access, or economic exclusion language needs context review.",
    },
    "Intersectional Microaggressions": {
        "patterns": (
            r"\b(?:aggressive|articulate|unprofessional|emotional|polished|"
            r"assertive|traditional university|pedigree|assimilation|backward|"
            r"culture|prestige|executive presence|institutional culture)\b",
        ),
        "deep_patterns": (r"\b(?:angry woman|angry black|culture fit)\b",),
        "note": "Potentially subjective descriptors can carry different implications across identities.",
    },
    "Accessibility Justice": {
        "patterns": (
            r"\b(?:without accommodations|no accommodations|inaccessible|"
            r"wheelchair|screen reader|captions|disability|disabled|hour\w*|"
            r"on[- ]site|schedule|subtitles|transcript|fast[- ]paced|rhythm|"
            r"impromptu|rapid[- ]fire|residency)\b",
        ),
        "deep_patterns": (r"\b(?:cognitive access|assistive technology|accessible format)\b",),
        "note": "Accessibility-related language was found; review whether the described needs are supported.",
    },
    "Stereotypical Framing": {
        "patterns": (
            r"\b(?:all women|all men|women are naturally|men are naturally|"
            r"older workers|young and energetic|professional appearance|"
            r"leadership roles|standard|traditional|align naturally|"
            r"high[- ]potential)\b",
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
            r"communication rhythms|polished clarity|direct)\b",
        ),
        "deep_patterns": (r"\b(?:professional language|clear english|communication style)\b",),
        "note": "Language-variety terms can be used to unfairly judge dialect or fluency; review context.",
    },
}


def evaluate_equity_payload(text: str, mode: str = "Standard Audit") -> dict:
    """Run a lightweight keyword screen; this is not a semantic fairness audit."""
    if len(text.strip()) < 10:
        return {"error": "Please provide at least 10 characters for a useful keyword screen."}

    content = text.lower()
    deep_scan = mode == "Deep Intersectional Scan"
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

    matched_pillar_count = sum(
        details["status"] == "Potential signal" for details in assessment.values()
    )
    keyword_signal_index = matched_pillar_count * 20

    intersectional_explanation = None
    recommendations = None
    if deep_scan:
        flagged_pillars = {
            pillar
            for pillar, details in assessment.items()
            if details["status"] == "Potential signal"
        }
        explanation_blocks = [
            f"Analytical overview: The keyword screen marked {len(flagged_pillars)} of 5 pillars for potential signals. These phrase matches are prompts for contextual review, not confirmed barriers or findings of bias."
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
            any(term in content for term in ("fellowship", "residency", "pedigree"))
            and flagged_pillars.intersection(
                {
                    "Spatial/Economic Erasure",
                    "Accessibility Justice",
                    "Intersectional Microaggressions",
                }
            )
        ):
            recommendation_title = "Fellowship Participation Review"
            recommendations = [
                f"Potential signals appeared in: {', '.join(flagged_list)}.",
                "Clarify whether residency or proximity requirements are essential, and make selection criteria transparent and relevant to program outcomes.",
                "Example rewrite: Fellowship requirements, including any in-person participation, are stated explicitly. Applicants are assessed using transparent criteria tied to the program's goals.",
            ]
        elif (
            any(term in content for term in ("accelerator", "networking", "mentorship"))
            and flagged_pillars.intersection(
                {
                    "Intersectional Microaggressions",
                    "Accessibility Justice",
                    "Dialectal Justice",
                }
            )
        ):
            recommendation_title = "Program Participation Reframing"
            recommendations = [
                f"Potential signals appeared in: {', '.join(flagged_list)}.",
                "If these terms describe participation criteria, consider structured mentoring, published milestones, and multiple communication formats.",
                "Example rewrite: The program offers structured mentoring, published milestones, and multiple ways to participate. Participants are assessed using transparent criteria tied to program goals.",
            ]
        elif (
            any(term in content for term in ("executive search", "candidate", "headquarters"))
            and flagged_pillars.intersection(
                {
                    "Spatial/Economic Erasure",
                    "Accessibility Justice",
                    "Intersectional Microaggressions",
                }
            )
        ):
            recommendation_title = "Executive Hiring Reframing"
            recommendations = [
                f"Potential signals appeared in: {', '.join(flagged_list)}.",
                "State location and schedule expectations separately, clarify which are essential, and apply consistent role-related selection criteria.",
                "Example rewrite: The role's location and schedule expectations are stated explicitly. Candidates are assessed against documented outcomes and consistent, role-related criteria.",
            ]
        elif (
            any(term in content for term in ("innovation district", "community", "downtown corridor"))
            and flagged_pillars.intersection(
                {
                    "Spatial/Economic Erasure",
                    "Accessibility Justice",
                    "Dialectal Justice",
                }
            )
        ):
            recommendation_title = "Community Planning Reframing"
            recommendations = [
                f"Potential signals appeared in: {', '.join(flagged_list)}.",
                "Involve affected residents in planning, provide accessible participation formats, and explain how community input informs decisions.",
                "Example rewrite: The planning process includes neighborhood consultation, accessible materials, and a published account of how community feedback informs decisions.",
            ]

        if not recommendations:
            recommendations.append(
                "No keyword rules triggered, so no automatic rewrite is suggested. This does not replace contextual human review."
            )

    return {
        "mode": mode,
        "payload_length": len(text),
        "matched_pillar_count": matched_pillar_count,
        "keyword_signal_index": keyword_signal_index,
        "assessment": assessment,
        "intersectional_explanation": intersectional_explanation,
        "recommendations": recommendations,
        "recommendation_title": recommendation_title if deep_scan else None,
    }


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
    if selected_mode == "Deep Intersectional Scan":
        st.info("Deep Scan active: compound keyword-signal review enabled.")
    else:
        st.info("Standard Audit active: baseline single-pass keyword screen.")
    st.caption("Oshun theme active: charcoal and honey-gold.")
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
        with st.spinner(f"M.A.R.G.E. is executing {selected_mode.lower()}..."):
            results = evaluate_equity_payload(user_payload, mode=selected_mode)

        if "error" in results:
            st.warning(results["error"])
        else:
            st.success(f"{selected_mode} complete.")
            signal_index = results["keyword_signal_index"]
            arrow_position = min(max(signal_index, 2), 98)
            matched_pillar_count = results["matched_pillar_count"]
            st.markdown(
                f"""
                <div class="artemis-scale-container">
                    <div style="color: #D4AF37; font-weight: 600; text-transform: uppercase;">
                        Artemis Keyword Signal Index
                    </div>
                    <div style="font-size: 1.6rem; font-weight: 700; color: #FFD700; margin-top: 0.5rem;">
                        {signal_index} / 100
                    </div>
                    <div style="color: #CCCCCC;">
                        {matched_pillar_count} of 5 pillar groups matched keyword rules
                    </div>
                    <div class="scale-track">
                        <div class="artemis-arrow-marker" style="left: {arrow_position}%">🏹</div>
                    </div>
                    <div class="scale-labels">
                        <span>0 groups matched</span>
                        <span>2-3 groups matched</span>
                        <span>5 groups matched</span>
                    </div>
                    <div style="color: #A0A0A0; font-size: 0.85rem; margin-top: 1rem;">
                        Heuristic keyword count only. This is not an equity score, risk probability, or fairness certification; no matches do not establish safety.
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
                recommendation_title = results["recommendation_title"]
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
                "This local keyword screen can miss contextual or implicit harms and can flag benign wording. Have affected people and domain experts review consequential decisions."
            )

st.markdown("---")
st.caption("M.A.R.G.E. Middleware Dashboard • Self-contained keyword screening")