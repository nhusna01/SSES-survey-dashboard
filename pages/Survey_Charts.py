import streamlit as st
import plotly.express as px
from preprocess import load_data

st.title("📊 Individual Survey Questions")
st.markdown("Select any question below to see the frequency of responses.")

df = load_data()

# Column Selection
target_col = st.selectbox("Choose a Question", options=df.columns)

# Charting
counts = df[target_col].value_counts().reset_index()
counts.columns = ["Response", "Count"]

fig = px.bar(
    counts, x="Response", y="Count", 
    color="Response", 
    text="Count",
    title=f"Results: {target_col}"
)
st.plotly_chart(fig, use_container_width=True)
