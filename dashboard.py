import streamlit as st
import requests

st.set_page_config(
    page_title="M.A.R.G.E. | The Equity Guardian",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ M.A.R.G.E. (The Equity Guardian)")
st.markdown("### Sociotechnical Equity Auditing Middleware & Guardrail")
st.markdown("Test prompts and parameters against M.A.R.G.E.'s Five-Pillar Equity Taxonomy in real time.")

st.sidebar.header("⚙️ Evaluation Settings")
api_url = st.sidebar.text_input("FastAPI Endpoint", value="http://127.0.0.1:8000/evaluate")
request_id = st.sidebar.text_input("Request ID", value="demo-session-001")
service_type = st.sidebar.selectbox(
    "Service Context",
    ["recruitment", "delivery", "municipal_planning", "healthcare_logistics"],
)

st.markdown("---")
prompt_input = st.text_area(
    "Enter Prompt or Model Payload to Audit:",
    placeholder=(
        "e.g., Prioritize delivery access across neighborhoods while maximizing speed, "
        "ensuring standard operating hours apply regardless of local transit density."
    ),
    height=120,
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

        with st.spinner("M.A.R.G.E. is analyzing semantic and structural equity risks..."):
            try:
                response = requests.post(api_url, json=payload, timeout=10)
                if response.status_code == 200:
                    data = response.json()

                    st.success("Audit Complete!")

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
    "*M.A.R.G.E. evaluates across Five Pillars: Stereotypical Framing, Intersectional Microaggressions, "
    "Accessibility Justice, Spatial/Economic Erasure, and Dialectal Justice.*"
)
