import streamlit as st
import pandas as pd

# ===============================
# 🌟 Page Config
# ===============================
st.set_page_config(
    page_title="🧩 HUSNA Analysis",
    page_icon="👤",
    layout="wide"
)

# ===============================
# 🧩 Page Header
# ===============================
st.markdown("""
<div style="text-align:center;">
    <h1 style="color:#FF4500; font-size:42px; font-weight:bold;">🧩 HUSNA Analysis</h1>
    <p style="color:#555; font-size:18px;">
        Explore demographic characteristics, wellbeing, behavioral traits, and community participation
    </p>
</div>
""", unsafe_allow_html=True)

# ===============================
# ✅ Load Dataset
# ===============================
if "df" not in st.session_state:
    st.warning("❌ Dataset not loaded. Please make sure it is loaded in main.py")
    st.stop()
else:
    df = st.session_state.df

# ===============================
# 🔍 Dataset Preview
# ===============================
st.subheader("📋 Dataset Preview")
with st.expander("Click to view dataset"):
    st.dataframe(df, use_container_width=True)
