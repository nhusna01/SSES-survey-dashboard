import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="Social & Emotional Impact Analysis", layout="wide")

# Title and Introduction
st.title("🌟 Impact of Social Support & Environment on Life Satisfaction")

st.markdown("""
### **Objective**
To analyze how social support from family and friends, along with a safe community environment, influences an individual's ability to manage their emotions and how these factors collectively impact their overall life satisfaction.

### **Problem Statement**
Understanding the intersection between external environmental safety and internal emotional regulation is critical. This analysis seeks to quantify how much of our life satisfaction is driven by our surroundings versus our personal social networks.
---
""")

# Load Dataset
# Replace 'your_data.csv' with your actual file path on GitHub
@st.cache_data
def load_data():
    # df = pd.read_csv("your_cleaned_data.csv")
    
    return data

df = load_data()

# Sidebar - Interactive Filters
st.sidebar.header("Explore & Filter Data")
st.sidebar.write("Adjust the parameters to update the visualizations.")

# Example Slider for Life Satisfaction
satisfaction_filter = st.sidebar.slider(
    "Select Life Satisfaction Range", 
    float(df['life_satisfaction'].min()), 
    float(df['life_satisfaction'].max()), 
    (0.0, 1.0)
)

# Filtering the dataframe based on selection
df_filtered = df[(df['life_satisfaction'] >= satisfaction_filter[0]) & 
                 (df['life_satisfaction'] <= satisfaction_filter[1])]

# Summary Metrics (The "Boxes")
st.subheader("Key Statistics")
col1, col2, col3, col4 = st.columns(4)

col1.metric(label="Avg. Life Satisfaction", value=f"{df_filtered['life_satisfaction'].mean():.2f}", border=True)
col2.metric(label="Social Support Score", value=f"{df_filtered['social_support_index'].mean():.2f}", border=True)
col3.metric(label="Community Safety", value=f"{df_filtered['community_safety_index'].mean():.2f}", border=True)
col4.metric(label="Emotion Management", value=f"{df_filtered['emotion_management_index'].mean():.2f}", border=True)

st.write("---")

# VIZ 1: Correlation Heatmap
st.subheader("Visual Analysis")

corr_cols = ['life_satisfaction', 'social_support_index', 'community_safety_index', 'emotion_management_index', 'overall_health']
corr_matrix = df_filtered[corr_cols].corr()

fig1 = px.imshow(
    corr_matrix, 
    text_auto=".2f", 
    color_continuous_scale='RdBu_r', 
    aspect="auto",
    title="<b>1. Correlation: How Social & Emotional Factors Relate</b>",
    labels=dict(color="Correlation")
)

# Updating layout for better look on web
fig1.update_layout(title_x=0.5)

st.plotly_chart(fig1, use_container_width=True)

