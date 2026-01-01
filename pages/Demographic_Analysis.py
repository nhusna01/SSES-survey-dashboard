import streamlit as st
import plotly.express as px
from preprocess import load_data

st.set_page_config(
    page_title="Demographic Analysis",
    layout="wide"
)

df = load_data()

st.title("Demographic Analysis")

st.markdown("""
This page presents the demographic distribution of respondents
based on selected background variables.
""")

# Select demographic column
demo_col = st.selectbox(
    "Select Demographic Variable",
    options=df.columns
)

# Pie chart
fig = px.pie(
    df,
    names=demo_col,
    title=f"Distribution of {demo_col}"
)

st.plotly_chart(fig, use_container_width=True)

