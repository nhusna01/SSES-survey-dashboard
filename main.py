import streamlit as st
import pandas as pd
import os
import base64
from pathlib import Path
from preprocess import load_data

# Path to your local dataset
DATA_PATH = Path("/content/cleaned_group_survey_data.csv")

@st.cache_data(ttl=15)   # refresh every 15 seconds
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df


# SET PAGE CONFIG 
st.set_page_config(
    page_title="🏠 SSES Survey Dashboard",
    page_icon="📊",
    layout="wide"
)

# LOAD DATA
if "df" not in st.session_state:
    try:
        st.session_state.df = load_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        
# DEFINE PAGES 
homepage = st.Page("pages/Homepage.py", title="Home", icon="🏠", default=True)
husna = st.Page("pages/husna.py", title="Husna's Analysis", icon="👤")
adawiyah = st.Page("pages/adawiyah.py", title="Adawiyah's Analysis", icon="👪")
atiqah = st.Page("pages/Atiqah.py", title="Atiqah's Analysis", icon="📈")
hafizah = st.Page("pages/Hafizah.py", title="Hafizah's Analysis", icon="🧠")

# NAVIGATION MENU DEFINITION
pg = st.navigation({
    "Menu": [
        homepage,
        husna,
        adawiyah,
        atiqah,
        hafizah
    ]
})


# BACKGROUND IMAGE 
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

# APPLY BACKGROUND
# Path relative to this file
CURRENT_DIR = Path(__file__).parent
IMAGE_PATH = CURRENT_DIR / "assets" / "background_SES.png"

bg_image_base64 = get_base64_image(str(IMAGE_PATH))

if bg_image_base64:
    set_background(bg_image_base64)
else:
    # Debug message if image is missing (only shows if image isn't found)
    st.sidebar.warning(f"Background image not found at assets/background_SES.png")

# RUN NAVIGATION
pg.run()
