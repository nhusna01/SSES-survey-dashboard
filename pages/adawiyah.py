import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Social & Emotional Impact Analysis", layout="wide")

# 2. Safety Check: Pull data from main.py's session state
if "df" not in st.session_state or st.session_state.df is None:
    st.error("⚠️ Data not found! Please go back to the Homepage to load the dataset.")
    st.stop()

# Use the data already loaded in main.py
df = st.session_state.df

# 3. Title and Introduction
st.title("🌟 Impact of Social Support & Environment on Life Satisfaction")

st.markdown("""
### **Objective**
To analyze how social support from family and friends, along with a safe community environment, influences an individual's ability to manage their emotions and how these factors collectively impact their overall life satisfaction.
---
""")

# 4. Sidebar - Interactive Filters
st.sidebar.header("Explore & Filter Data")

# We wrap the slider in a try/except or a check to ensure the column exists
if 'life_satisfaction' in df.columns:
    min_val = float(df['life_satisfaction'].min())
    max_val = float(df['life_satisfaction'].max())
    
    satisfaction_filter = st.sidebar.slider(
        "Select Life Satisfaction Range", 
        min_val, max_val, (min_val, max_val)
    )

    # Filtering the dataframe
    df_filtered = df[(df['life_satisfaction'] >= satisfaction_filter[0]) & 
                     (df['life_satisfaction'] <= satisfaction_filter[1])]
else:
    st.error("Column 'life_satisfaction' not found in dataset!")
    st.stop()

# 5. Summary Metrics (The "Boxes")
st.subheader("Key Statistics")
col1, col2, col3, col4 = st.columns(4)

# Helper function to handle missing columns safely
def get_avg(column_name):
    return df_filtered[column_name].mean() if column_name in df_filtered.columns else 0.0

col1.metric(label="Avg. Life Satisfaction", value=f"{get_avg('life_satisfaction'):.2f}", border=True)
col2.metric(label="Social Support Score", value=f"{get_avg('social_support_index'):.2f}", border=True)
col3.metric(label="Community Safety", value=f"{get_avg('community_safety_index'):.2f}", border=True)
col4.metric(label="Emotion Management", value=f"{get_avg('emotion_management_index'):.2f}", border=True)

st.write("---")

# 6. VIZ 1: Correlation Heatmap
st.subheader("Visual Analysis")

# Only include columns that actually exist in your CSV
available_cols = [c for c in ['life_satisfaction', 'social_support_index', 'community_safety_index', 'emotion_management_index', 'overall_health'] if c in df_filtered.columns]

if len(available_cols) > 1:
    corr_matrix = df_filtered[available_cols].corr()

    fig1 = px.imshow(
        corr_matrix, 
        text_auto=".2f", 
        color_continuous_scale='RdBu_r', 
        aspect="auto",
        title="<b>Correlation: How Social & Emotional Factors Relate</b>",
        labels=dict(color="Correlation")
    )
    fig1.update_layout(title_x=0.5)
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("Not enough numeric columns found to create a correlation heatmap.")True)

