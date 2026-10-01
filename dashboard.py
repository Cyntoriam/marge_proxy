import streamlit as st
import requests

st.set_page_config(
    page_title="M.A.R.G.E. | The Equity Guardian",
    page_icon="🛡️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #121212;
        color: #F5F2EB;
    }
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        color: #D4AF37;
        font-weight: 600;
    }
    .guardian-card {
        background-color: #1E1B18;
        border: 1px solid #D4AF37;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .guardian-quote {
        background-color: #1E1B18;
        border-left: 4px solid #D4AF37;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 20px;
        font-style: italic;
        color: #E2DDD5;
    }
    .pillar-tag {
        background-color: #2D2620;
        color: #D4AF37;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 0.85em;
        font-weight: 600;
        margin-right: 6px;
        display: inline-block;
        margin-bottom: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<h1 class="main-header">🛡️ M.A.R.G.E. (The Equity Guardian)</h1>',
    unsafe_allow_html=True,
)
st.markdown("### Sociotechnical Equity Auditing Middleware & Protective Guardrail")
st.markdown(
    """
    <div class="guardian-quote">
    "Designed with the spirit of radical care and protection, guarding technological
    systems against erasure, bias, and microaggressions across the Five Pillars."
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.header("⚙️ Guardian Parameters")
api_url = st.sidebar.text_input("FastAPI Endpoint", value="http://127.0.0.1:8000/evaluate")
request_id = st.sidebar.text_input("Request ID", value="session-oshun-001")
service_domains = {
    "Recruitment & Hiring": "recruitment",
    "Automated Delivery Routing": "delivery",
    "Municipal Planning": "municipal_planning",
    "Healthcare Logistics": "healthcare_logistics",
}
service_context = st.sidebar.selectbox("Service Domain", list(service_domains))
strictness_level = st.sidebar.slider(
    "Remediation Strictness",
    min_value=1,
    max_value=5,
    value=3,
    help="Passed to the API; the current backend does not yet apply this setting.",
)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("#### Input Prompt / Payload")
    prompt_input = st.text_area(
        "Enter text to audit for equity risks:",
        placeholder=(
            "e.g., Optimize distribution routes across the metropolitan sector to "
            "maximize efficiency, bypassing peripheral residential zones where "
            "order volume is low."
        ),
        height=150,
    )

    if st.button("✨ Run Equity Audit", type="primary"):
        if not prompt_input.strip():
            st.warning("Please provide a prompt or payload to evaluate.")
        else:
            payload = {
                "request_id": request_id,
                "prompt": prompt_input,
                "parameters": {
                    "service": service_domains[service_context],
                    "strictness": strictness_level,
                },
            }

            with st.spinner(
                "M.A.R.G.E. is analyzing structural and semantic equity risks with care..."
            ):
                try:
                    response = requests.post(api_url, json=payload, timeout=15)
                    if response.status_code == 200:
                        data = response.json()

                        st.success("Audit complete. Guardian protection protocol applied.")

                        result_col1, result_col2 = st.columns(2)
                        with result_col1:
                            st.metric("Path Type", data.get("path_type", "Unknown"))
                        with result_col2:
                            st.metric(
                                "Overall Approved",
                                "Yes" if data.get("overall_approved") else "No",
                            )

                        st.markdown("### 📋 Structured Audit Output")
                        st.json(data)

                        evaluations = data.get("evaluations", [])
                        if evaluations:
                            st.markdown("### Evaluation Breakdown")
                            for item in evaluations:
                                with st.expander(item.get("pillar", "Unknown pillar")):
                                    st.write(f"Flagged: {item.get('flagged')}")
                                    st.write(f"Severity: {item.get('severity')}")
                                    st.write(
                                        f"Confidence: {item.get('confidence_score')}"
                                    )
                                    st.write(
                                        item.get("reasoning", "No reasoning provided.")
                                    )

                        suggested_correction = data.get("suggested_correction")
                        if suggested_correction:
                            st.markdown("### Suggested Correction")
                            st.info(suggested_correction)
                    else:
                        st.error(f"API Error: Status code {response.status_code}")
                        st.text(response.text)
                except requests.exceptions.ConnectionError:
                    st.error(
                        "Could not connect to the FastAPI backend. Ensure your Uvicorn "
                        "server is running (`uvicorn app.main:app --reload`)."
                    )
                except requests.exceptions.Timeout:
                    st.error("The FastAPI backend did not respond within 15 seconds.")
                except requests.exceptions.RequestException as exc:
                    st.error(f"The audit request failed: {exc}")
                except ValueError as exc:
                    st.error(f"The API returned an invalid JSON response: {exc}")

with col2:
    st.markdown("#### 🌟 Five-Pillar Framework")
    st.markdown(
        """
        <div class="guardian-card">
            <p style="color: #F5F2EB; font-size: 0.9em; margin-bottom: 12px;">
            M.A.R.G.E. actively guards against systemic bias across five core dimensions of care:
            </p>
            <div>
                <span class="pillar-tag">Stereotypical Framing</span>
                <span class="pillar-tag">Intersectional Microaggressions</span>
                <span class="pillar-tag">Accessibility Justice</span>
                <span class="pillar-tag">Spatial &amp; Economic Erasure</span>
                <span class="pillar-tag">Dialectal Justice</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown(
    "<small style='color: #888;'>M.A.R.G.E. Middleware Dashboard • Powered by Python &amp; Streamlit</small>",
    unsafe_allow_html=True,
)
