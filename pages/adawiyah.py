# adawiyah.py
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Page Configuration
st.set_page_config(page_title="Social & Emotional Impact Analysis", layout="wide")

# Custom Header following the template
st.markdown("""
    <h2 style='text-decoration: underline;'>
        Assignment JIE42303: Scientific Visualization
    </h2>
""", unsafe_allow_html=True)
st.title("🤝❤️ Social & Emotional Impact Analysis")
st.markdown("---")

# Objective and Problem Statement
st.markdown(
    "**Objective Statement:** To analyze how social support from family and friends, along with a safe community environment, influences an individual's ability to manage their emotions and how these factors collectively impact their overall life satisfaction."
)
st.info("**Problem Statement:** Understanding the intersection between external environmental safety and internal emotional regulation is critical to quantifying life satisfaction.")

st.markdown("---")

# Load Dataset
csv_url = "https://raw.githubusercontent.com/nhusna01/SSES-survey-dashboard/refs/heads/main/dataset/Adawiyah_SSES_cleaned.csv"
try:
    df = pd.read_csv(csv_url)
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    df = pd.DataFrame()

# Summary metrics (Summary Boxes)
if not df.empty:
    col1, col2, col3, col4 = st.columns(4)

    # Calculations
    avg_life_sat = df['life_satisfaction'].mean() if 'life_satisfaction' in df else 0
    avg_social = df['social_support_index'].mean() if 'social_support_index' in df else 0
    avg_safety = df['community_safety_index'].mean() if 'community_safety_index' in df else 0
    avg_emotion = df['emotion_management_index'].mean() if 'emotion_management_index' in df else 0

    col1.metric(label="🎓 Avg. Life Satisfaction", value=f"{avg_life_sat:.2f}",
                help="Average overall life satisfaction score", border=True)
    col2.metric(label="🤝 Social Support Index", value=f"{avg_social:.2f}",
                help="Average score for social support from family/friends", border=True)
    col3.metric(label="🛡️ Community Safety", value=f"{avg_safety:.2f}",
                help="Average perceived safety of the environment", border=True)
    col4.metric(label="🧠 Emotion Management", value=f"{avg_emotion:.2f}",
                help="Average ability to regulate and manage emotions", border=True)

st.markdown("---")

# Display cleaned dataset preview
st.subheader("Dataset: Social & Emotional Metrics")
st.dataframe(df)

st.markdown("---")

