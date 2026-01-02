import streamlit as st
import pandas as pd
import os
import base64
from pathlib import Path
from preprocess import load_data

# Set page config
st.set_page_config(
    page_title="🏠 SSES Survey Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- LOAD DATA ONCE ---
if "df" not in st.session_state:
    st.session_state.df = load_data()

# ======================================
# NAVIGATION MENU DEFINITION
# ======================================
# Ensure these filenames match your actual files in the directory
pg = st.navigation({
    "Menu": [
        homepage,
        husna,
        machine_learning,
        survey_charts,
        emotion_resilience
    ]
})



# ======================================
# BACKGROUND IMAGE FUNCTIONS
# ======================================
def get_base64_image(image_path):
    if not Path(image_path).exists():
        return None
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_background(image_base64):
    if image_base64 is None:
        return
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{image_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.9);
            padding: 2rem;
            border-radius: 14px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply Background
BASE_DIR = Path(os.getcwd())
IMAGE_PATH = BASE_DIR / "assets" / "sses_background.jpg"
bg_image = get_base64_image(str(IMAGE_PATH))
set_background(bg_image)

# ======================================
# RUN NAVIGATION
# ======================================
pg.run() # Added parentheses here to actually execute the function
