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
### **Main Objective**
To compare emotional wellbeing, health, and work functioning between **Selangor** and **Pahang**,  
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
# DATA PREVIEW
# ===============================
st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

# ===============================
# FILTER STATES (SAFE COPY)
# ===============================
df_state = df[df['state'].isin(['Selangor', 'Pahang'])].copy()

# ===============================
# SUMMARY METRICS
# ===============================
st.subheader("📊 Summary Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Respondents", len(df))
col2.metric("Selangor Respondents", len(df[df['state'] == 'Selangor']))
col3.metric("Pahang Respondents", len(df[df['state'] == 'Pahang']))
st.divider()


# ===============================
# 1️⃣ RESPONDENT COUNT
# ===============================
st.subheader("1️⃣ Number of Respondents by State")

state_counts = df['state'].value_counts().reset_index()
state_counts.columns = ['State', 'Count']

fig1 = px.bar(
    state_counts,
    x='State',
    y='Count',
    text='Count',
    title='Number of Respondents per State'
)
st.plotly_chart(fig1, use_container_width=True)
st.divider()

st.markdown("""
**Analysis:**  
The bar chart illustrates the distribution of respondents across Selangor and Pahang.
A relatively balanced number of respondents ensures that comparisons between states
are fair and not overly influenced by sample size differences.
""")


# ===============================
# 2️⃣ AVERAGE EMOTIONAL WELLBEING
# ===============================
st.subheader("2️⃣ Average Emotional Wellbeing by State")

emotion_vars = ['calm_under_pressure', 'emotional_control']
state_emotion_mean = df_state.groupby('state')[emotion_vars].mean().reset_index()

fig2 = px.bar(
    state_emotion_mean,
    x='state',
    y=emotion_vars,
    barmode='group',
    title='Average Emotional Wellbeing Scores'
)
st.plotly_chart(fig2, use_container_width=True)
st.divider()

st.markdown("""
**Analysis:**  
Selangor demonstrates slightly higher average scores for calmness under pressure and
emotional control. This may reflect greater exposure to demanding work environments,
which can strengthen emotional regulation skills over time.
""")


# ===============================
# 3️⃣ CALM UNDER PRESSURE (STACKED)
# ===============================
st.subheader("3️⃣ Calm Under Pressure Category Distribution")

df_state.loc[:, 'calm_cat'] = df_state['calm_under_pressure'].apply(
    lambda x: 'Low' if x <= 2 else 'Medium' if x == 3 else 'High'
)

fig3 = px.histogram(
    df_state,
    x='state',
    color='calm_cat',
    barmode='stack',
    title='Calm Under Pressure Categories by State'
)
st.plotly_chart(fig3, use_container_width=True)
st.divider()

st.markdown("""
**Analysis:**  
A higher proportion of Selangor respondents fall within the **High** calmness category,
while Pahang shows a larger concentration in the **Medium** category. This suggests
differences in stress management and coping mechanisms between the two states.
""")


# ===============================
# 4️⃣ VIOLIN PLOTS
# ===============================
st.subheader("4️⃣ Distribution of Work Functioning by State")

col1, col2 = st.columns(2)

fig_tp = px.violin(
    df_state,
    x='state',
    y='task_persistence',
    color='state',
    box=True,
    points='all',
    title='Distribution of Task Persistence by State'
)
col1.plotly_chart(fig_tp, use_container_width=True)

fig_tw = px.violin(
    df_state,
    x='state',
    y='teamwork',
    color='state',
    box=True,
    points='all',
    title='Distribution of Teamwork by State'
)
col2.plotly_chart(fig_tw, use_container_width=True)

st.divider()

st.markdown("""
**Analysis:**  
The violin plots reveal both the distribution and variability of task persistence and
teamwork scores. Selangor shows a wider distribution with higher median values,
indicating stronger work engagement and collaborative behaviour compared to Pahang.
""")


# ===============================
# 5️⃣ OVERALL HEALTH (DONUT)
# ===============================
st.subheader("5️⃣ Overall Health Distribution")

def health_category(x):
    if x <= 2:
        return 'Poor'
    elif x == 3:
        return 'Moderate'
    else:
        return 'Good'

df_state.loc[:, 'overall_health_cat'] = df_state['overall_health'].apply(health_category)

health_counts = (
    df_state.groupby(['state', 'overall_health_cat'])
    .size()
    .reset_index(name='count')
)

sel = health_counts[health_counts['state'] == 'Selangor']
pah = health_counts[health_counts['state'] == 'Pahang']

fig5 = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'domain'}, {'type': 'domain'}]],
    subplot_titles=['Selangor', 'Pahang']
)

fig5.add_trace(go.Pie(labels=sel['overall_health_cat'], values=sel['count'], hole=0.4), 1, 1)
fig5.add_trace(go.Pie(labels=pah['overall_health_cat'], values=pah['count'], hole=0.4), 1, 2)

fig5.update_layout(title_text="Overall Health Comparison")
st.plotly_chart(fig5, use_container_width=True)
st.divider()

st.markdown("""
**Analysis:**  
Selangor exhibits a higher proportion of respondents reporting **Good** health,
whereas Pahang has more respondents in the **Moderate** category. This may be influenced
by lifestyle, access to healthcare, and working conditions.
""")


# ===============================
# 6️⃣ RADAR CHART
# ===============================
st.subheader("6️⃣ Radar Chart: Emotional & Work Functioning")

variables = [
    'calm_under_pressure',
    'emotional_control',
    'well_rested',
    'overall_health',
    'task_persistence',
    'teamwork'
]

state_means = df_state.groupby('state')[variables].mean().reset_index()

fig6 = go.Figure()
for state in ['Selangor', 'Pahang']:
    fig6.add_trace(go.Scatterpolar(
        r=state_means[state_means['state'] == state][variables].values.flatten(),
        theta=variables,
        fill='toself',
        name=state
    ))

fig6.update_layout(
    polar=dict(radialaxis=dict(range=[1, 5])),
    title="Radar Comparison of Wellbeing Indicators"
)
st.plotly_chart(fig6, use_container_width=True)
st.divider()

st.markdown("""
**Analysis:**  
The radar chart highlights consistent performance differences across multiple wellbeing
dimensions. Selangor scores higher in emotional control, teamwork, and task persistence,
suggesting stronger overall work functioning and emotional resilience.
""")


# ===============================
# 7️⃣ HEATMAP
# ===============================
st.subheader("7️⃣ Heatmap of Wellbeing Scores")

fig7 = px.imshow(
    state_means[variables],
    x=variables,
    y=state_means['state'],
    text_auto=".2f",
    color_continuous_scale='RdBu',
    title="Heatmap of Mean Wellbeing Scores by State"
)
st.plotly_chart(fig7, use_container_width=True)

st.markdown("""
**Analysis:**  
The heatmap provides a clear visual comparison of mean wellbeing scores across states.
Darker shades for Selangor across most indicators reinforce earlier findings that
Selangor respondents generally report higher wellbeing and work functioning.
""")

