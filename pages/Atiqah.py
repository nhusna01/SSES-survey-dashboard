import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="", layout="wide")

# Title and Introduction
st.title("🌟 Impact")

st.markdown("""
### **Objective**
To analyze the highest state vs the lowest state in demaining workplace life.

# Load Dataset
csv_url = "https://raw.githubusercontent.com/nhusna01/SSES-survey-dashboard/refs/heads/main/dataset/Atiqah_SSES_cleaned.csv"
try:
    df = pd.read_csv(csv_url)
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    df = pd.DataFrame()

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

# VISUAL ANALYSIS: State Comparison in Workplace Life
st.subheader("Visual Analysis")

st.markdown("""
### **1. Highest vs Lowest State in Workplace Life**
This visualization compares the average workplace life score across states.  
It highlights regional differences in workplace conditions and helps identify
which states experience better or poorer workplace life outcomes.
""")

# Calculate average workplace life score by state
state_workplace = (
    df_filtered
    .groupby('state')['workplace_life_index']
    .mean()
    .reset_index()
)

# Sort for clear highest vs lowest comparison
state_workplace = state_workplace.sort_values(
    by='workplace_life_index',
    ascending=False
)

fig1 = px.bar(
    state_workplace,
    x='state',
    y='workplace_life_index',
    text=state_workplace['workplace_life_index'].round(2),
    title="<b>Average Workplace Life Index by State</b>"
)

fig1.update_layout(
    title_x=0.5,
    xaxis_title="State",
    yaxis_title="Average Workplace Life Index"
)

fig1.update_traces(textposition='outside')

st.plotly_chart(fig1, use_container_width=True)

