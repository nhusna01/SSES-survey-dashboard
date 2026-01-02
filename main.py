import streamlit as st
import pandas as pd
import os
import base64
from pathlib import Path
from preprocess import load_data

# 1. SET PAGE CONFIG (Must be the very first Streamlit command)
st.set_page_config(
    page_title="🏠 SSES Survey Dashboard",
    page_icon="📊",
    layout="wide"
)

# 2. DEFINE PAGES (Fixes the NameError)
# Make sure these .py files exist in your "pages" folder
homepage = st.Page("Homepage.py", title="Home", icon="🏠", default=True)
husna = st.Page("pages/husna.py", title="Husna's Analysis", icon="👤")
machine_learning = st.Page("pages/ml.py", title="Machine Learning", icon="🤖")
survey_charts = st.Page("pages/charts.py", title="Survey Charts", icon="📈")
emotion_resilience = st.Page("pages/resilience.py", title="Emotion & Resilience", icon="🧠")

# 3. NAVIGATION MENU DEFINITION
pg = st.navigation({
    "Menu": [
        Homepage,
        husna,
        machine_learning,
        survey_charts,
        emotion_resilience
    ]
})

# 4. LOAD DATA
if "df" not in st.session_state:
    try:
        st.session_state.df = load_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")

# 5. BACKGROUND IMAGE FUNCTIONS
def get_base64_image(image_path):
    """Reads an image file and returns a base64 encoded string."""
    if not os.path.isfile(image_path):
        return None
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def set_background(image_base64):
    """Injects CSS to set the background image."""
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
        /* Makes the content container semi-transparent for readability */
        .block-container {{
            background-color: rgba(255, 255, 255, 0.9);
            padding: 3rem;
            border-radius: 20px;
            margin-top: 2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 6. APPLY BACKGROUND
# Path relative to this file
CURRENT_DIR = Path(__file__).parent
IMAGE_PATH = CURRENT_DIR / "assets" / "background_SES.png"

bg_image_base64 = get_base64_image(str(IMAGE_PATH))

if bg_image_base64:
    set_background(bg_image_base64)
else:
    # Debug message if image is missing (only shows if image isn't found)
    st.sidebar.warning(f"Background image not found at assets/background_SES.png")

# 7. RUN NAVIGATION
pg.run()
