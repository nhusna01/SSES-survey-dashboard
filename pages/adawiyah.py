# adawiyah's page
import streamlit as st
import pandas as pd
import plotly.express as px


# Page Configuration
st.set_page_config(page_title="Social & Emotional Impact Analysis", layout="wide")

# Main Title Section
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #2C3E50; /* Deep charcoal for a neat look */
        padding-top: 10px;
        padding-bottom: 20px;
        font-weight: 700;
    }
    </style>
    <h1 class="main-title">✦ Social & Emotional Impact Analysis</h1>
""", unsafe_allow_html=True)

st.markdown("---")

# Custom CSS for Soft Pink Boxes 
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

# Interactive Section 
# Expander
with st.expander("View Research Objective", expanded=True):
    
    # Objective Box
    st.markdown(f"""
        <div class="pink-box">
            <h4>Objective Statement</h4>
            <p>To analyze how <b>social support</b> from family and friends, along with a <b>safe community environment</b>, 
            influences an individual's ability to manage their emotions and how these factors collectively impact 
            their overall <b>life satisfaction</b>.</p>
        </div>
    """, unsafe_allow_html=True)

    

st.markdown("---")

# DATA LOADING & INTERACTIVE EXPLORATION 

csv_url = "https://raw.githubusercontent.com/nhusna01/SSES-survey-dashboard/refs/heads/main/dataset/Adawiyah_SSES_cleaned.csv"

# 1. Subtle Loading Interactivity
with st.status("Syncing Research Data...", expanded=False) as status:
    try:
        df = pd.read_csv(csv_url)
        status.update(label="Data Loaded Successfully!", state="complete", expanded=False)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        df = pd.DataFrame()
        status.update(label="Connection Failed", state="error")

# 2. Neat Interactive Data Section
if not df.empty:
    st.markdown("### Data Exploration")
    
    # Using an expander to keep the layout tidy
    with st.expander("Click to Preview & Filter Raw Dataset"):
        
        # Row 1: Search & Download
        search_col, download_col = st.columns([3, 1])
        
        with search_col:
            search_query = st.text_input("🔍 Search data by any value:", placeholder="Type to filter...")
        

        # Apply search filter if text is entered
        if search_query:
            df_display = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
            st.write(f"Showing {len(df_display)} matching results:")
        else:
            df_display = df.head(10) # Show first 10 rows by default
            st.caption("Showing first 10 rows. Use the search bar above to find specific records.")

        # Display the interactive table
        st.dataframe(df_display, use_container_width=True)

st.markdown("---")

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

