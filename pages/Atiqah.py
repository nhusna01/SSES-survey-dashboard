import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Wellbeing & Emotional Comparison",
    layout="wide"
)

# ===============================
# TITLE & OBJECTIVE
# ===============================
st.title("🌟 Emotional Wellbeing & Work Functioning Comparison")
st.markdown("""
### *Main Objective*
To compare emotional wellbeing, health, and work functioning between *Selangor* and *Pahang*,  
focusing on emotional regulation, calmness under pressure, and overall health outcomes.
""")

# ===============================
# LOAD DATA FROM GITHUB
# ===============================
csv_url = "https://raw.githubusercontent.com/nhusna01/SSES-survey-dashboard/refs/heads/main/dataset/Atiqah_SSES_Cleaned.csv"

try:
    df = pd.read_csv(csv_url)
    st.success("Dataset loaded successfully from GitHub!")
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    df = pd.DataFrame()

if df.empty:
    st.warning("No data available. Please check the GitHub CSV link.")
    st.stop()

# ===============================
# FILTER STATES (SAFE COPY)
# ===============================
df_state = df[df['state'].isin(['Selangor', 'Pahang'])].copy()

# ===============================
# 📊 SUMMARY OVERVIEW (IMPROVED)
# ===============================
st.subheader("📊 Overall Summary Overview")

# ---- ONE BOX: TOTAL RESPONDENTS ----
total_respondents = len(df_state)
sel_count = len(df_state[df_state['state'] == 'Selangor'])
pah_count = len(df_state[df_state['state'] == 'Pahang'])

st.metric(
    label="Total Respondents (Selangor + Pahang)",
    value=total_respondents,
    delta=f"Selangor: {sel_count} | Pahang: {pah_count}"
)

st.caption("Scores range from 1 (Low) to 5 (High)")
st.divider()

# ---- MEAN SCORE SUMMARY ----
summary_vars = [
    'calm_under_pressure',
    'emotional_control',
    'task_persistence',
    'teamwork',
    'overall_health'
]

mean_summary = (
    df_state.groupby('state')[summary_vars]
    .mean()
    .round(2)
)

st.subheader("📌 Mean Score Comparison by State")

for var in summary_vars:
    st.markdown(f"### {var.replace('_', ' ').title()}")

    col1, col2, col3 = st.columns(3)

    sel_mean = mean_summary.loc['Selangor', var]
    pah_mean = mean_summary.loc['Pahang', var]
    diff = sel_mean - pah_mean

    col1.metric("Selangor", sel_mean)
    col2.metric("Pahang", pah_mean)
    col3.metric("Difference", f"{diff:.2f}")

    if diff > 0:
        st.success("Selangor shows a higher average score.")
    else:
        st.info("Pahang shows a higher average score.")

    st.divider()

# ===============================
# 1️⃣ AVERAGE EMOTIONAL WELLBEING
# ===============================
st.subheader("1️⃣ Average Emotional Wellbeing by State")

emotion_vars = ['calm_under_pressure', 'emotional_control']
state_emotion_mean = df_state.groupby('state')[emotion_vars].mean().reset_index()

fig1 = px.bar(
    state_emotion_mean,
    x='state',
    y=emotion_vars,
    barmode='group',
    title='Average Emotional Wellbeing Scores'
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("""
*Analysis:*  
Selangor demonstrates slightly higher average emotional regulation scores,
suggesting stronger coping abilities under work-related pressure.
""")

st.divider()

# ===============================
# 2️⃣ CALM UNDER PRESSURE (STACKED)
# ===============================
st.subheader("2️⃣ Calm Under Pressure Category Distribution")

df_state['calm_cat'] = df_state['calm_under_pressure'].apply(
    lambda x: 'Low' if x <= 2 else 'Medium' if x == 3 else 'High'
)

fig2 = px.histogram(
    df_state,
    x='state',
    color='calm_cat',
    barmode='stack',
    title='Calm Under Pressure Categories by State'
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
*Analysis:*  
Selangor respondents are more concentrated in the *High* calmness category,
while Pahang shows a stronger presence in the *Medium* category.
""")

st.divider()

# ===============================
# 3️⃣ VIOLIN PLOTS
# ===============================
st.subheader("3️⃣ Distribution of Work Functioning by State")

col1, col2 = st.columns(2)

fig_tp = px.violin(
    df_state,
    x='state',
    y='task_persistence',
    color='state',
    box=True,
    points='all',
    title='Task Persistence Distribution'
)
col1.plotly_chart(fig_tp, use_container_width=True)

fig_tw = px.violin(
    df_state,
    x='state',
    y='teamwork',
    color='state',
    box=True,
    points='all',
    title='Teamwork Distribution'
)
col2.plotly_chart(fig_tw, use_container_width=True)

st.markdown("""
*Analysis:*  
Selangor shows higher medians and wider score distributions, indicating stronger
engagement and collaborative tendencies compared to Pahang.
""")

st.divider()

# ===============================
# 4️⃣ OVERALL HEALTH (DONUT)
# ===============================
st.subheader("4️⃣ Overall Health Distribution")

df_state['overall_health_cat'] = df_state['overall_health'].apply(
    lambda x: 'Poor' if x <= 2 else 'Moderate' if x == 3 else 'Good'
)

health_counts = (
    df_state.groupby(['state', 'overall_health_cat'])
    .size()
    .reset_index(name='count')
)

fig4 = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'domain'}, {'type': 'domain'}]],
    subplot_titles=['Selangor', 'Pahang']
)

for i, state in enumerate(['Selangor', 'Pahang'], start=1):
    data = health_counts[health_counts['state'] == state]
    fig4.add_trace(
        go.Pie(labels=data['overall_health_cat'], values=data['count'], hole=0.4),
        1, i
    )

fig4.update_layout(title_text="Overall Health Comparison")
st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ===============================
# 5️⃣ RADAR CHART
# ===============================
st.subheader("5️⃣ Radar Chart: Overall Wellbeing Profile")

variables = summary_vars + ['well_rested']
state_means = df_state.groupby('state')[variables].mean().reset_index()

fig5 = go.Figure()
for state in ['Selangor', 'Pahang']:
    fig5.add_trace(go.Scatterpolar(
        r=state_means[state_means['state'] == state][variables].values.flatten(),
        theta=variables,
        fill='toself',
        name=state
    ))

fig5.update_layout(
    polar=dict(radialaxis=dict(range=[1, 5])),
    title="Radar Comparison of Wellbeing Indicators"
)
st.plotly_chart(fig5, use_container_width=True)

st.divider()

# ===============================
# 6️⃣ HEATMAP
# ===============================
st.subheader("6️⃣ Heatmap of Mean Wellbeing Scores")

fig6 = px.imshow(
    state_means[variables],
    x=variables,
    y=state_means['state'],
    text_auto=".2f",
    color_continuous_scale='RdBu',
    title="Heatmap of Mean Scores by State"
)
st.plotly_chart(fig6, use_container_width=True)
