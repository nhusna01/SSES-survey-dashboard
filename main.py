import streamlit as st
import pandas as pd
import os
import base64
from pathlib import Path

# ------------------------------
# Load dataset into session_state w
# ------------------------------


GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1_7nl2F8Vfd90h8ce2TreDW5D_m3WHr6vEFtg10xz3BI/export?format=csv&gid=1821075619"

@st.cache_data(ttl=15)   # refresh every 15 seconds
def load_data():
    df = pd.read_csv(GOOGLE_SHEET_URL)
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

# RUN NAVIGATION
pg.run()
