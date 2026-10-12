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

st.markdown(
    f"""
    <style>
    .stApp {{ background: {bg_style} !important; color: {text_color} !important; }}
    .block-container {{ max-width: 100% !important; padding-top: 1.2rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }}
    .control-panel {{ background-color: {panel_bg}; padding: 1.2rem; border-radius: 12px; border: 1px solid {panel_border}; margin-bottom: 1.5rem; }}
    .marge-header {{ background: {header_bg}; padding: 1.5rem; border-radius: 12px; color: #ffffff; margin-bottom: 1.2rem; border: 2px solid {header_border}; text-align: center; }}
    .marge-title {{ font-size: 2.2rem; font-weight: 800; margin-bottom: 0.2rem; color: {title_color}; }}
    .marge-subtitle {{ font-size: 0.95rem; color: {subtitle_color}; font-weight: 400; text-transform: uppercase; }}
    .marge-essence {{ font-size: 0.85rem; color: {title_color}; font-style: italic; margin-top: 0.3rem; }}
    .guardian-card {{ background-color: {card_bg}; padding: 1rem; border-radius: 8px; border-left: 4px solid {header_border}; margin-bottom: 0.8