import streamlit as st
import plotly.express as px
from preprocess import load_data

st.set_page_config(
    page_title="Survey Charts",
    layout="wide"
)

df = load_data()

st.title("Survey Question Analysis")

st.markdown("""
This page allows exploration of individual survey questions
to understand response patterns.
""")

question_col = st.selectbox(
    "Select Survey Question",
    options=df.columns
)

value_counts = df[question_col].value_counts().reset_index()
value_counts.columns = ["Response", "Count"]

fig = px.bar(
    value_counts,
    x="Response",
    y="Count",
    text="Count",
    title=f"Response Distribution for {question_col}"
)

st.plotly_chart(fig, use_container_width=True)

