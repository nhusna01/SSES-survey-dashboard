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
To compare factors that affect working sector between highest and lowest state of respondents, focusing on healthcare and working style.
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
    st.stop()
    
# ===============================
# DATA PREVIEW
# ===============================
st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

# ===============================
# FILTER STATES (SAFE COPY)
# ===============================
df_state = df[df['state'].isin(['Selangor', 'Pahang'])].copy()

# ===============================
# 📊 KEY PERFORMANCE INDICATORS
# ===============================
st.subheader("📊 Key Performance Indicators")

# ---- Respondent count (SEPARATE, not combined)
sel_count = df_state[df_state['state'] == 'Selangor'].shape[0]
pah_count = df_state[df_state['state'] == 'Pahang'].shape[0]

col1, col2 = st.columns(2)
col1.metric("👥 Selangor Respondents", sel_count)
col2.metric("👥 Pahang Respondents", pah_count)

st.divider()

# ---- Mean score KPIs
summary_vars = {
    "Calm Under Pressure": "calm_under_pressure",
    "Emotional Control": "emotional_control",
    "Task Persistence": "task_persistence",
    "Teamwork": "teamwork",
    "Overall Health": "overall_health"
}

state_means = (
    df_state
    .groupby('state')[list(summary_vars.values())]
    .mean()
    .round(2)
)

for label, var in summary_vars.items():
    col1, col2 = st.columns(2)

    col1.metric(
        label=f"📌 {label} (Selangor)",
        value=state_means.loc['Selangor', var]
    )

    col2.metric(
        label=f"📌 {label} (Pahang)",
        value=state_means.loc['Pahang', var]
    )

st.caption("Mean scores range from 1 (Low) to 5 (High).")
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
**Analysis:**  
Selangor shows slightly higher average emotional regulation scores, suggesting greater
adaptability to demanding environments.

**Interpretation:**  
This may indicate that respondents in Selangor are more accustomed to regulating
emotions in demanding environments.
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
**Analysis:**  
Selangor respondents are more concentrated in the *High* calmness category,
while Pahang respondents are more evenly distributed.

**Interpretation:**  
This pattern suggests that individuals in Selangor may have stronger stress
management capabilities, potentially influenced by workplace demands, lifestyle,
and access to coping resources.
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
    title='Task Persistence'
)
col1.plotly_chart(fig_tp, use_container_width=True)

fig_tw = px.violin(
    df_state,
    x='state',
    y='teamwork',
    color='state',
    box=True,
    points='all',
    title='Teamwork'
)
col2.plotly_chart(fig_tw, use_container_width=True)

st.markdown("""
**Analysis:**  
Selangor exhibits higher medians and greater variability in task persistence and teamwork,
indicating stronger engagement and collaboration.

**Interpretation:**  
This implies stronger work engagement and collaborative behaviour among Selangor
respondents.
""")

st.divider()

# ===============================
# 4️⃣ OVERALL HEALTH (DONUT)
# ===============================
st.subheader("4️⃣ Overall Health Distribution")

def health_category(x):
    if x <= 2:
        return 'Poor'
    elif x == 3:
        return 'Moderate'
    else:
        return 'Good'

df_state['overall_health_cat'] = df_state['overall_health'].apply(health_category)

health_counts = (
    df_state.groupby(['state', 'overall_health_cat'])
    .size()
    .reset_index(name='count')
)

sel = health_counts[health_counts['state'] == 'Selangor']
pah = health_counts[health_counts['state'] == 'Pahang']

fig4 = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'domain'}, {'type': 'domain'}]],
    subplot_titles=['Selangor', 'Pahang']
)

fig4.add_trace(go.Pie(labels=sel['overall_health_cat'], values=sel['count'], hole=0.4), 1, 1)
fig4.add_trace(go.Pie(labels=pah['overall_health_cat'], values=pah['count'], hole=0.4), 1, 2)

fig4.update_layout(title_text="Overall Health Comparison")
st.plotly_chart(fig4, use_container_width=True)

st.markdown("""
**Analysis:**  
Selangor shows a higher proportion of respondents reporting *Good* health compared to Pahang.

**Interpretation:**    
This visualization highlights differences in perceived health status across states 
and supports the findings observed in emotional and work functioning indicators.
""")

st.divider()

# ===============================
# 5️⃣ RADAR CHART
# ===============================
st.subheader("5️⃣ Radar Chart: Overall Wellbeing")

variables = list(summary_vars.values())
state_means_radar = df_state.groupby('state')[variables].mean().reset_index()

fig5 = go.Figure()
for state in ['Selangor', 'Pahang']:
    fig5.add_trace(go.Scatterpolar(
        r=state_means_radar[state_means_radar['state'] == state][variables].values.flatten(),
        theta=variables,
        fill='toself',
        name=state
    ))

fig5.update_layout(
    polar=dict(radialaxis=dict(range=[1, 5])),
    title="Radar Comparison of Wellbeing Indicators"
)
st.plotly_chart(fig5, use_container_width=True)

st.markdown("""
**Analysis:**  
The radar chart highlights consistently higher wellbeing scores for Selangor,
particularly in emotional control and work-related indicators.

**Interpretation:**    
This suggests that Selangor respondents score higher across multiple aspects of wellbeing simultaneously. 
The radar chart effectively summarizes complex, multivariate data in a single visualization, reinforcing the 
overall comparison between states.
""")

st.divider()

# ===============================
# 6️⃣ HEATMAP
# ===============================
st.subheader("6️⃣ Heatmap of Mean Wellbeing Scores")

fig6 = px.imshow(
    state_means_radar[variables],
    x=variables,
    y=state_means_radar['state'],
    text_auto=".2f",
    color_continuous_scale='RdBu',
    title="Heatmap of Mean Wellbeing Scores by State"
)
st.plotly_chart(fig6, use_container_width=True)

st.markdown("""
**Final Conclusion:**  
Across emotional wellbeing, work functioning, and health indicators, Selangor respondents
consistently report higher average scores than Pahang respondents. These findings suggest
state-level differences in emotional resilience and work-related wellbeing.
""")
