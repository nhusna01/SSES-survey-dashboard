# adawiyah.py
import streamlit as st
import pandas as pd
import plotly.express as px


# Page Configuration
st.set_page_config(page_title="Social & Emotional Impact Analysis", layout="wide")

# Main Title 
st.title("🤝❤️ Social & Emotional Impact Analysis")
st.markdown("---")

# --- Custom CSS for Soft Pink Boxes ---
st.markdown("""
    <style>
    .pink-box {
        background-color: #FFF0F5; /* Soft Lavender Blush/Pink */
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #FFB6C1; /* Accent Pink border */
        margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .pink-box h4 {
        color: #D02090; /* Darker pink for the header */
        margin-top: 0;
    }
    .pink-box p {
        color: #333333;
        font-size: 16px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# --- Interactive Section ---
# We use an expander so the user can "interact" by opening/closing the goals of the study
with st.expander("🎯 View Research Objective & Problem Statement", expanded=True):
    
    # Objective Box
    st.markdown(f"""
        <div class="pink-box">
            <h4>📍 Objective Statement</h4>
            <p>To analyze how <b>social support</b> from family and friends, along with a <b>safe community environment</b>, 
            influences an individual's ability to manage their emotions and how these factors collectively impact 
            their overall <b>life satisfaction</b>.</p>
        </div>
    """, unsafe_allow_html=True)

    # Problem Statement Box
    st.markdown(f"""
        <div class="pink-box" style="background-color: #FFE4E1;"> <h4>⚠️ Problem Statement</h4>
            <p>Understanding the intersection between <b>external environmental safety</b> and <b>internal emotional regulation</b> 
            is critical. This analysis seeks to quantify how much of our life satisfaction is driven by our surroundings 
            versus our personal social networks.</p>
        </div>
    """, unsafe_allow_html=True)

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

