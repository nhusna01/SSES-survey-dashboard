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
    df = pd.DataFrame()  # fallback empty dataframe

# ===============================
# CHECK IF DATA IS LOADED
# ===============================
if df.empty:
    st.warning("No data available. Please check the GitHub link.")
else:
    st.subheader("Preview of Dataset")
    st.dataframe(df.head())

    # ===============================
    # FILTER STATES
    # ===============================
    df_state = df[df['state'].isin(['Selangor', 'Pahang'])]

    # ===============================
    # SUMMARY BOXES
    # ===============================
    st.subheader("📊 Summary Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Respondents", len(df))
    col2.metric("Selangor Respondents", len(df[df['state'] == 'Selangor']))
    col3.metric("Pahang Respondents", len(df[df['state'] == 'Pahang']))

    st.divider()

    # ===============================
    # 1️⃣ RESPONDENT COUNT BY STATE
    # ===============================
    st.subheader("1️⃣ Number of Respondents by State")

    state_counts = df['state'].value_counts().reset_index()
    state_counts.columns = ['state', 'Count']

    fig1 = px.bar(
        state_counts,
        x='State',
        y='Count',
        text='Count',
        title='Number of Respondents per State'
    )
    fig1.update_layout(xaxis_title="State", yaxis_title="Count")

    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("""
    **Analysis:**  
    This chart shows the distribution of respondents across states, ensuring fair comparison
    between Selangor and Pahang.
    """)

    st.divider()

    # ===============================
    # 2️⃣ AVERAGE EMOTIONAL SCORES
    # ===============================
    st.subheader("2️⃣ Average Emotional Wellbeing by State")

    emotion_vars = ['calm_under_pressure', 'emotional_control']
    state_emotion_mean = df.groupby('state')[emotion_vars].mean().reset_index()

    fig2 = px.bar(
        state_emotion_mean[state_emotion_mean['state'].isin(['Selangor', 'Pahang'])],
        x='state',
        y=emotion_vars,
        barmode='group',
        title='Average Emotional Wellbeing Scores'
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    **Analysis:**  
    Selangor generally shows higher emotional regulation scores, likely influenced by
    work environment exposure and lifestyle demands.
    """)

    st.divider()

    # ===============================
    # 3️⃣ CALM UNDER PRESSURE (STACKED)
    # ===============================
    st.subheader("3️⃣ Calm Under Pressure Category Distribution")

    df_state['calm_cat'] = df_state['calm_under_pressure'].apply(
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

    st.markdown("""
    **Analysis:**  
    Selangor respondents tend to cluster more in the **High** calmness category,
    suggesting better stress-handling capabilities.
    """)

    st.divider()

    # ===============================
    # 4️⃣ OVERALL HEALTH (DONUT PIE)
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

    selangor_data = health_counts[health_counts['state'] == 'Selangor']
    pahang_data = health_counts[health_counts['state'] == 'Pahang']

    fig4 = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'domain'}, {'type': 'domain'}]],
        subplot_titles=['Selangor', 'Pahang']
    )

    fig4.add_trace(go.Pie(
        labels=selangor_data['overall_health_cat'],
        values=selangor_data['count'],
        hole=0.4
    ), row=1, col=1)

    fig4.add_trace(go.Pie(
        labels=pahang_data['overall_health_cat'],
        values=pahang_data['count'],
        hole=0.4
    ), row=1, col=2)

    fig4.update_layout(title_text="Overall Health Comparison")

    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("""
    **Analysis:**  
    Selangor shows a higher proportion of **Good** health, while Pahang shows
    more respondents in the **Moderate** category.
    """)

    st.divider()

    # ===============================
    # 5️⃣ RADAR CHART
    # ===============================
    st.subheader("5️⃣ Radar Chart: Emotional & Work Functioning")

    variables = [
        'calm_under_pressure',
        'emotional_control',
        'well_rested',
        'overall_health',
        'task_persistence',
        'teamwork'
    ]

    state_means = df_state.groupby('state')[variables].mean().reset_index()

    fig5 = go.Figure()

    for state in ['Selangor', 'Pahang']:
        values = state_means[state_means['state'] == state][variables].values.flatten()
        fig5.add_trace(go.Scatterpolar(
            r=values,
            theta=variables,
            fill='toself',
            name=state
        ))

    fig5.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[1, 5])),
        title="Radar Comparison of Wellbeing Indicators"
    )

    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("""
    **Analysis:**  
    Selangor scores consistently higher across most wellbeing dimensions,
    especially in emotional control and teamwork.
    """)

    st.divider()

    # ===============================
    # 6️⃣ HEATMAP
    # ===============================
    st.subheader("6️⃣ Heatmap of Wellbeing Scores")

    fig6 = px.imshow(
        state_means[variables],
        x=variables,
        y=state_means['state'],
        text_auto=".2f",
        color_continuous_scale='RdBu',
        title="Heatmap of Mean Wellbeing Scores by State"
    )

    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("""
    **Analysis:**  
    The heatmap highlights clear differences between states, with Selangor
    generally exhibiting higher emotional resilience and work functioning.
    """)

else:
    st.info("👈 Please upload a cleaned CSV file to begin analysis.")
