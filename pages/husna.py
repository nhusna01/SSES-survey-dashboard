import streamlit as st
import plotly.express as px

df = st.session_state.df

st.title("👥 Employment Status Analysis")

demo_col = st.selectbox(
    "Select Demographic Variable",
    df.columns
)

fig = px.pie(df, names=demo_col)
st.plotly_chart(fig, use_container_width=True)
