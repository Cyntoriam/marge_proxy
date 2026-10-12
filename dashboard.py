import asyncio
import json
import random
from typing import List, Optional
from pydantic import BaseModel, Field
import streamlit as st
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="M.A.R.G.E. | Multimodal Automated Real-time Guardian Engine",
    page_icon="🏹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALIZE SESSION STATE ---
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark Mode"
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "voice_input_text" not in st.session_state:
    st.session_state.voice_input_text = ""

# --- COLOR DEFINITIONS ---
HONEY_GOLD = "#ffb800"

# --- DYNAMIC THEME COLOR PALETTES ---
if st.session_state.theme_mode == "Dark Mode":
    bg_style = "linear-gradient(180deg, #240c03 0%, #120501 60%, #0a0301 100%)"
    text_color = "#fcebe6"
    panel_bg = "#170702"
    panel_border = "rgba(255, 184, 0, 0.6)"
    hr_border = "rgba(255, 184, 0, 0.5)"
    header_bg = "linear-gradient(135deg, #2e1004 0%, #1a0802 100%)"
    header_border = HONEY_GOLD
    title_color = HONEY_GOLD
    text_stroke_val = "none"
    subtitle_color = "#f3d0c7"
    card_bg = "#1c0802"
    card_border = "rgba(255, 184, 0, 0.4)"
    badge_bg = "rgba(224, 86, 36, 0.25)"
    badge_text = HONEY_GOLD
    expander_bg = "#2e1004"
    expander_text = HONEY_GOLD
    input_bg = "#240c03"
    input_text = "#ffffff"
    placeholder_text = "#f3d0c7"
    dropdown_popover_bg = "#1f0902"
    dropdown_popover_text = HONEY_GOLD
    dropdown_hover_bg = "#3d1304"
    btn_bg = "linear-gradient(90deg, #e05624 0%, #d94e1f 100%)"
    sidebar_bg = "#170702"
else:
    # LIGHT MODE: Honey Gold Outlines & Accents
    bg_style = "linear-gradient(180deg, #fdfbf7 0%, #f7f0e6 60%, #efe3d3 100%)"
    text_color = "#2b1105"
    panel_bg = "#f5e9da"
    panel_border = HONEY_GOLD
    hr_border = HONEY_GOLD
    header_bg = "linear-gradient(135deg, #8c2d0d 0%, #5e1c06 100%)"
    header_border = HONEY_GOLD
    title_color = HONEY_GOLD
    text_stroke_val = f"1px {HONEY_GOLD}"
    subtitle_color = HONEY_GOLD
    card_bg = "#f7ebe0"
    card_border = HONEY_GOLD
    badge_bg = "#f2d2c2"
    badge_text = "#8c2d0d"
    expander_bg = "#ebd7c5"
    expander_text = "#8c2d0d"
    input_bg = "#ffffff"
    input_text = "#2b1105"
    placeholder_text = "#6e3b22"
    dropdown_popover_bg = "#ffffff"
    dropdown_popover_text = "#2b1105"
    dropdown_hover_bg = "#f5e9da"
    btn_bg = "linear-gradient(90deg, #d96b27 0%, #b84f18 100%)"
    sidebar_bg = "#f5e9da"

# --- INJECT COMPLETE CSS WITH OVERRIDES ---
css_code = (
    "<style>"
    f".stApp {{ background: {bg_style} !important; color: {text_color} !important; }}"
    f"[data-testid='stSidebar'] {{ background-color: {sidebar_bg} !important; border-right: 2px solid {panel_border} !important; }}"
    ".block-container { max-width: 100% !important; padding-top: 1.2rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }"
    f".control-panel {{ background-color: {panel_bg}; padding: 1.2rem; border-radius: 12px; border: 2px solid {panel_border}; margin-bottom: 1.5rem; }}"
    f".marge-header {{ background: {header_bg}; padding: 1.5rem; border-radius: 12px; color: #ffffff; margin-bottom: 1.2rem; border: 2px solid {header_border}; text-align: center; }}"
    f".marge-title {{ font-size: 2.2rem; font-weight: 800; margin-bottom: 0.4rem; color: {title_color}; -webkit-text-stroke: {text_stroke_val}; }}"
    
    # Subheader Box & Typography Styling
    f".marge-subtitle-box {{ display: inline-block; padding: 0.6rem 1.4rem; border: 2px solid {HONEY_GOLD}; border-radius: 8px; background: rgba(0,0,0,0.3); margin-top: 0.3rem; }}"
    f".marge-subtitle {{ font-size: 0.92rem; color: {subtitle_color}; font-weight: 800; text-transform: uppercase; letter-spacing: 0.6px; -webkit-text-stroke: {text_stroke_val}; }}"
    f".marge-essence {{ font-size: 0.85rem; color: {HONEY_GOLD} !important; font-style: italic; margin-top: 0.25rem; font-weight: 700; -webkit-text-stroke: none !important; }}"
    
    f".guardian-card {{ background-color: {card_bg}; padding: 1rem; border-radius: 8px; border-left: 4px solid {header_border}; margin-bottom: 0.8rem; border:
