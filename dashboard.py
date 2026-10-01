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
    .guardian-quote {
        background-color: #1E1B18;
        border-left: 4px solid #D4AF37;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 20px;
        font-style: italic;
        color: #E2DDD5;
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

st.sidebar.header("⚙️ Evaluation Settings")
api_url = st.sidebar.text_input("FastAPI Endpoint", value="http://127.0.0.1:8000/evaluate")
request_id = st.sidebar.text_input("Request ID", value="session-oshun-001")
service_type = st.sidebar.selectbox(
    "Service Context",
    ["recruitment", "delivery", "municipal_planning", "healthcare_logistics"],
)

st.markdown("---")
prompt_input = st.text_area(
    "Enter Prompt or Model Payload to Audit:",
    placeholder=(
        "e.g., Prioritize distribution channels while ensuring equitable access across "
        "historical transit and demographic boundaries."
    ),
    height=140,
)

if st.button("🚀 Run Equity Audit", type="primary"):
    if not prompt_input.strip():
        st.warning("Please enter a prompt to evaluate.")
    else:
        payload = {
            "request_id": request_id,
            "prompt": prompt_input,
            "parameters": {"service": service_type},
        }

        with st.spinner(
            "M.A.R.G.E. is analyzing semantic and structural equity risks with care..."
        ):
            try:
                response = requests.post(api_url, json=payload, timeout=15)
                if response.status_code == 200:
                    data = response.json()

                    st.success("Audit Complete.")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Path Type", data.get("path_type", "Unknown"))
                    with col2:
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
                                st.write(f"Confidence: {item.get('confidence_score')}")
                                st.write(item.get("reasoning", "No reasoning provided."))

                    suggested_correction = data.get("suggested_correction")
                    if suggested_correction:
                        st.markdown("### Suggested Correction")
                        st.info(suggested_correction)
                else:
                    st.error(f"API Error: Status code {response.status_code}")
                    st.text(response.text)
            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to the FastAPI backend. Ensure your Uvicorn server is running "
                    "(`uvicorn app.main:app --reload`)."
                )
            except Exception as exc:
                st.error(f"An error occurred: {exc}")

st.markdown("---")
st.markdown(
    "<small>M.A.R.G.E. evaluates across Five Pillars: Stereotypical Framing, "
    "Intersectional Microaggressions, Accessibility Justice, Spatial/Economic Erasure, "
    "and Dialectal Justice.</small>",
    unsafe_allow_html=True,
)
