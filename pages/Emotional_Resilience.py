import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ======================================
# PAGE CONFIG
# ======================================
st.set_page_config(
    page_title="Emotional Resilience Analysis",
    layout="wide"
)

st.title("Emotional Resilience and Personal Development")
st.markdown("""
**Objective:**  
To investigate the relationship between emotional resilience and personal development attributes,
including motivation, adaptability, emotional control, task persistence, and teamwork skills.
""")

# ======================================
# LOAD DATA (CSV from Google Drive or GitHub)
# ======================================
# Use Google Drive path locally OR GitHub raw CSV for Streamlit Cloud
DATA_URL = "https://raw.githubusercontent.com/nhusna01/SSES-survey-dashboard/main/SSES%20Survey%20Responses.csv"
df = pd.read_csv(DATA_URL, encoding='latin-1')

# ======================================
# CLEAN & RENAME COLUMNS (Same as Colab)
# ======================================
df = df.rename(columns={
    'Timestamp': 'timestamp',
    'Username': 'username',
    'Age (Years)': 'age',
    'Gender': 'gender',
    'Marital Status': 'marital_status',
    'Highest Level of Education': 'education_level',
    'Employment Status': 'employment_status',
    'State': 'state',
    'Main Language Spoken at Home': 'home_language',
    'I can stay calm even when under pressure.  ': 'calm_under_pressure',
    'I can control my emotions when I feel angry or upset.  ': 'emotional_control',
    'I find it easy to work well with others.  ': 'teamwork',
    'I finish tasks even when they are difficult.  ': 'task_persistence',
    'I can adapt easily to new or unexpected situations. ': 'adaptability',
    'I am motivated to improve my skills and knowledge. ': 'self_motivation'
})

# Ensure numeric
likert_cols = [
    'calm_under_pressure', 'emotional_control', 'adaptability',
    'task_persistence', 'self_motivation', 'teamwork'
]
df[likert_cols] = df[likert_cols].apply(pd.to_numeric, errors='coerce')
df[likert_cols] = df[likert_cols].fillna(df[likert_cols].median())

# ======================================
# 1️⃣ Likert Distribution (Bar Chart)
# ======================================
st.subheader("1. Distribution of Emotional Resilience Attributes")
selected_attr = st.selectbox("Select Attribute", options=likert_cols)

value_counts = df[selected_attr].value_counts().reset_index()
value_counts.columns = ["Response", "Count"]
fig1 = px.bar(
    value_counts,
    x="Response",
    y="Count",
    text="Count",
    title=f"Response Distribution: {selected_attr}",
    color="Response"
)
st.plotly_chart(fig1, use_container_width=True)

# ======================================
# 2️⃣ Radar Chart (Average Profile)
# ======================================
st.subheader("2. Average Emotional Resilience Profile")
mean_scores = df[likert_cols].mean()

fig2 = go.Figure()
fig2.add_trace(go.Scatterpolar(
    r=mean_scores.values.tolist() + [mean_scores.values[0]],
    theta=likert_cols + [likert_cols[0]],
    fill='toself',
    name='Average Score'
))
fig2.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0,5])),
    showlegend=False,
    title="Average Emotional Resilience and Personal Development Profile"
)
st.plotly_chart(fig2, use_container_width=True)

# ======================================
# 3️⃣ Correlation Heatmap
# ======================================
st.subheader("3. Correlation Between Attributes")
corr = df[likert_cols].corr()
fig3 = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale='RdBu',
    title="Correlation Heatmap"
)
st.plotly_chart(fig3, use_container_width=True)

# ======================================
# 4️⃣ Box Plot (Variability)
# ======================================
st.subheader("4. Distribution and Variability")
melted = df[likert_cols].melt(var_name="Attribute", value_name="Score")
fig4 = px.box(
    melted,
    x="Attribute",
    y="Score",
    title="Distribution and Variability of Emotional Resilience Attributes",
    color="Attribute"
)
st.plotly_chart(fig4, use_container_width=True)

# ======================================
# 5️⃣ Group Comparison (Gender)
# ======================================
st.subheader("5. Comparison by Gender")
if 'gender' in df.columns:
    grouped_means = df.groupby('gender')[likert_cols].mean().reset_index()
    fig5 = px.bar(
        grouped_means,
        x="gender",
        y=likert_cols,
        barmode='group',
        title="Comparison of Emotional Resilience Attributes by Gender"
    )
    st.plotly_chart(fig5, use_container_width=True)
else:
    st.info("Gender variable not available for group comparison.")
