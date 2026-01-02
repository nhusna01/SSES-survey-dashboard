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
    # Check if the file exists before trying to open it
    if not os.path.isfile(image_path):
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
            background-image: url("data:image/png;base64,{image_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        /* This makes the main content area slightly transparent so you can see the background */
        .block-container {{
            background-color: rgba(255, 255, 255, 0.9);
            padding: 3rem;
            border-radius: 20px;
            margin-top: 2rem;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- Apply Background ---
# Use the directory where main.py lives to find the assets folder
CURRENT_DIR = Path(__file__).parent
IMAGE_PATH = CURRENT_DIR / "assets" / "background_SES.png"

bg_image = get_base64_image(str(IMAGE_PATH))
set_background(bg_image)

# ======================================
# RUN NAVIGATION
# ======================================
pg.run() # Added parentheses here to actually execute the function
