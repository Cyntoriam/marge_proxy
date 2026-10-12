import asyncio
import random
from typing import List, Optional
from pydantic import BaseModel, Field
import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="M.A.R.G.E. | Multimodal Automated Real-time Guardian Engine",
    page_icon="🏹",
    layout="wide",
)

# --- INITIALIZE SESSION STATE FOR SETTINGS ---
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark Mode"

# --- DYNAMIC THEME STYLING ---
if st.session_state.theme_mode == "Dark Mode":
    bg_style = "linear-gradient(180deg, #240c03 0%, #120501 60%, #0a0301 100%)"
    text_color = "#fcebe6"
    panel_bg = "#170702"
    panel_border = "rgba(224, 86, 36, 0.4)"
    header_bg = "linear-gradient(135deg, #2e1004 0%, #1a0802 100%)"
    header_border = "#e05624"
    title_color = "#ffb800"
    subtitle_color = "#f3d0c7"
    card_bg = "#1c0802"
    card_border = "rgba(255, 184, 0, 0.25)"
    badge_bg = "rgba(224, 86, 36, 0.25)"
    badge_text = "#ffb800"
    expander_bg = "#240c03"
    btn_bg = "linear-gradient(90deg, #e05624 0%, #d94e1f 100%)"
else:
    bg_style = "linear-gradient(180deg, #fdfbf7 0%, #f7f0e6 60%, #efe3d3 100%)"
    text_color = "#2b1105"
    panel_bg = "#f5e9da"
    panel_border = "#d96b27"
    header_bg = "linear-gradient(135deg, #8c2d0d 0%, #5e1c06 100%)"
    header_border = "#d96b27"
    title_color = "#ffca3a"
    subtitle_color = "#fbe3d5"
    card_bg = "#f7ebe0"
    card_border = "rgba(217, 107, 39, 0.3)"
    badge_bg = "#f2d2c2"
    badge_text = "#8c2d0d"
    expander_bg = "#ebd7c5"
    btn_bg = "linear-gradient(90deg, #d96b27 0%, #b84f18 100%)"

# --- INJECT CSS IN SINGLE-LINE CONCATENATIONS ---
css_code = (
    "<style>"
    f".stApp {{ background: {bg_style} !important; color: {text_color} !important; }}"
    ".block-container { max-width: 100% !important; padding-top: 1.2rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }"
    f".control-panel {{ background-color: {panel_bg}; padding: 1.2rem; border-radius: 12px; border: 1px solid {panel_border}; margin-bottom: 1.5rem; }}"
    f".marge-header {{ background: {header_bg}; padding: 1.5rem; border-radius: 12px; color: #ffffff; margin-bottom: 1.2rem; border: 2px solid {header_border}; text-align: center; }}"
    f".marge-title {{ font-size: 2.2rem; font-weight: 800; margin-bottom: 0.2rem; color: {title_color}; }}"
    f".marge-subtitle {{ font-size: 0.95rem; color: {subtitle_color}; font-weight: 400; text-transform: uppercase; }}"
    f".marge-essence {{ font-size: 0.85rem; color: {title_color}; font-style: italic; margin-top: 0.3rem; }}"
    f".guardian-card {{ background-color: {card_bg}; padding: 1rem; border-radius: 8px; border-left: 4px solid {header_border}; margin-bottom: 0.8rem; border: 1px solid {card_border}; color: {text_color}; }}"
    f".degradation-badge {{ display: inline-block; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.75rem; font-weight: bold; background-color: {badge_bg}; border: 1px solid {header_border}; color: {badge_text}; margin-top: 0.4rem; }}"
    f".streamlit-expanderHeader {{ background-color: {expander_bg} !important; color: {badge_text} !important; font-weight: 700 !important; border-radius: 6px !important; border: 1px solid {panel_border} !important; }}"
    f"div.stButton > button {{ background: {btn_bg} !important; color: #ffffff !important; border-radius: 8px !important; border: none !important; font-weight: bold !important; width: 100% !important; padding: 0.75rem !important; }}"
    "</style>"
)

header_html = (
    '<div class="marge-header">'
    '<div class="marge-title">🏹 M.A.R.G.E.</div>'
    '<div class="marge-subtitle">Multimodal Automated Real-time Guardian Engine</div>'
    '<div class="marge-essence">✨ The Equity Guardian — Thought Guidance & Algorithmic Protection ✨</div>'
    '</div>'
)

st.markdown(css_code + header_html, unsafe_allow_html=True)

# --- PYDANTIC VALIDATION MODELS ---
class PillarEvaluation(BaseModel):
    pillar_name: str
    severity_score: float = Field(..., ge=0.0, le=1.0)
    issue_identified: str
    detailed_explanation: str
    collaborative_rationale: str
    active_remedy: str

class MARGEEvaluationPayload(BaseModel):
    original_text: str
    remediated_text: str
    guardian_index: int = Field(..., ge=0, le=100)
    degradation_tier: str = Field(default="Tier 1: Full Deep Inspection")
    violations: List[PillarEvaluation] = Field(default_factory=list)

# --- IN-PAGE CONTROL PANEL WITH SETTINGS GEAR ---
st.markdown("<div class='control-panel'>", unsafe_allow_html=True)
st.markdown(f"<h4 style='color: {title_color}; margin-top: 0;'>🏹 Guardian Portal & Controls</h4>", unsafe_allow_html=True)

col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1, 1, 1])

with col_ctrl1:
    raw_handle = st.text_input("Your Name / Handle", value="Pocketdoc")
    formatted_handle = raw_handle.strip() if raw_handle.strip() else "Guardian"
    display_name = f"Dr. {formatted_handle}" if not formatted_handle.startswith("Dr.") and "pocketdoc" in formatted_handle.lower() else formatted_handle

with col_ctrl2:
    page_selection = st.selectbox("Navigation View", ["🔍 Audit Console", "🏛️ Five-Pillar Taxonomy", "📖 System Guide"])

with col_ctrl3:
    enable_ai_to_ai = st.toggle("AI-to-AI Interceptor", value=True)

# Expander for Settings (⚙️)
with st.expander("⚙️ System Settings & Visual Preferences", expanded=False):
    col_set1, col_set2 = st.columns(2)
    with col_set1:
        selected_theme = st.radio(
            "Theme Style",
            ["Dark Mode", "Light Mode"],
            index=0 if st.session_state.theme_mode == "Dark Mode" else 1,
            horizontal=True
        )
        if selected_theme != st.session_state.theme_mode:
            st.session_state.theme_mode = selected_theme
            st.rerun()
    with col_set2:
        st.markdown("<span style='font-size: 0.85rem;'><strong>System Health:</strong> Operational<br><strong>Latency:</strong> 42ms (Async)</span>", unsafe_allow_html=True)

scan_mode = "Initial Scan"
input_preset = "Custom Text Entry"

if page_selection == "🔍 Audit Console":
    st.markdown("---")
    col_