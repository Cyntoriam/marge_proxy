import asyncio
import random
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
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

# --- DYNAMIC THEME STYLING (DARK vs LIGHT MODE) ---
if st.session_state.theme_mode == "Dark Mode":
    theme_css = """
    <style>
    .stApp {
        background: linear-gradient(180deg, #240c03 0%, #120501 60%, #0a0301 100%) !important;
        color: #fcebe6 !important;
    }
    .control-panel {
        background-color: #170702;
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid rgba(224, 86, 36, 0.4);
        margin-bottom: 1.5rem;
    }
    .marge-header {
        background: linear-gradient(135deg, #2e1004 0%, #1a0802 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: #ffffff;
        margin-bottom: 1.2rem;
        box-shadow: 0 6px 20px rgba(224, 86, 36, 0.3);
        border: 2px solid #e05624;
        text-align: center;
    }
    .marge-title { font-size: 2.2rem; font-weight: 800; margin-bottom: 0.2rem; color: #ffb800; }
    .marge-subtitle { font-size: 0.95rem; color: #f3d0c7; font-weight: 400; text-transform: uppercase; }
    .marge-essence { font-size: 0.85rem; color: #ffb800; font-style: italic; margin-top: 0.3rem; }
    .guardian-card {
        background-color: #1c0802;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffb800;
        margin-bottom: 0.8rem;
        border: 1px solid rgba(255, 184, 0, 0.25);
        color: #fcebe6;
    }
    .degradation-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: bold;
        background-color: rgba(224, 86, 36, 0.25);
        border: 1px solid #e05624;
        color: #ffb800;
        margin-top: 0.4rem;
    }
    .streamlit-expanderHeader {
        background-color: #240c03 !important;
        color: #ffb800 !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        border: 1px solid rgba(224, 86, 36, 0.3) !important;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #e05624 0%, #d94e1f 100%) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
        box-shadow: 0 4px 12px rgba(224, 86, 36, 0.3) !important;
        width: 100% !important;
        padding: 0.75rem !important;
    }
    </style>
    """
else:
    theme_css = """
    <style>
    .stApp {
        background: linear-gradient(180deg, #fdf