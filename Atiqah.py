import streamlit as st
import pandas as pd
import plotly.express as px

# Count number of respondents per state
state_counts = df['state'].value_counts().reset_index()
state_counts.columns = ['State', 'Count']

# Create Plotly bar chart
fig = px.bar(
    state_counts,
    x='State',
    y='Count',
    title='Number of Respondents per State',
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)
