# adawiyah's page
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(page_title="Social & Emotional Impact Analysis", layout="wide")

# Main Title Section
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #2C3E50;
        padding-top: 10px;
        padding-bottom: 20px;
        font-weight: 700;
    }
    </style>
    <h1 class="main-title">✦ Social & Emotional Impact Analysis</h1>
""", unsafe_allow_html=True)

st.markdown("---")

# Custom CSS for Soft Pink Boxes 
st.markdown("""
    <style>
    .pink-box {
        background-color: #FFF0F5;
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #FFB6C1;
        margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .pink-box h4 { color: #D02090; margin-top: 0; }
    .pink-box p { color: #333333; font-size: 16px; line-height: 1.6; }
    </style>
""", unsafe_allow_html=True)

# Interactive Section 
with st.expander("View Research Objective", expanded=True):
    st.markdown(f"""
        <div class="pink-box">
            <h4>Objective Statement</h4>
            <p>To analyze how <b>social support</b> from family and friends, along with a <b>safe community environment</b>, 
            influences an individual's ability to manage their emotions and how these factors collectively impact 
            their overall <b>life satisfaction</b>.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# DATA FETCHING AND INDEXING LOGIC
csv_url = "https://raw.githubusercontent.com/nhusna01/SSES-survey-dashboard/refs/heads/main/dataset/Adawiyah_SSES_cleaned.csv"

@st.cache_data  
def fetch_data(url):
    data = pd.read_csv(url)
    # CORE INDEXING LOGIC (Must happen here so all charts see these columns)
    data['social_support_index'] = data[['social_support', 'social_time', 'community_care']].mean(axis=1)
    data['emotion_management_index'] = data[['calm_under_pressure', 'emotional_control']].mean(axis=1)
    data['community_safety_index'] = data[['neighborhood_safety', 'community_care']].mean(axis=1)
    return data

# Attempt to load data
df = pd.DataFrame()
try:
    df = fetch_data(csv_url)
except Exception as e:
    st.error(f"Connection Error: {e}")

# INTERACTIVE EXPLORATION SECTION 
if not df.empty:
    head_col, method_col = st.columns([3, 1])
    with head_col:
        st.markdown("### Data Exploration")
    with method_col:
        with st.popover("View Methodology"):
            st.markdown("#### Indexing Logic")
            st.markdown("""
            - **Social Support Index:** `social_support`, `social_time`, `community_care`
            - **Emotion Management:** `calm_under_pressure`, `emotional_control`
            - **Community Safety:** `neighborhood_safety`, `community_care`
            """)
            st.caption("Calculation: Arithmetic Mean of grouped variables.")

    with st.expander("🔍 Preview & Filter Raw Dataset", expanded=True):
        st.markdown("""
            <div style="background-color: #FFF0F5; padding: 15px; border-radius: 10px; border-left: 5px solid #FFB6C1; margin-bottom: 20px;">
                <p style="margin: 0; color: #333; font-size: 15px;">
                    <b>About this Dataset:</b> This cleaned dataset captures how individuals perceive their social networks, environmental safety, and internal ability to manage emotions.
                </p>
            </div>
        """, unsafe_allow_html=True)

        search_query = st.text_input("Search data by any value:", placeholder="Search by state, education level, or scores...")
        if search_query:
            df_display = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
            st.info(f"Showing {len(df_display)} matching results:")
        else:
            df_display = df.head(10)
            st.caption("Showing first 10 rows. Use the search bar above to filter all records.")

        st.dataframe(df_display, use_container_width=True)

st.markdown("---")

# INTERACTIVE METRICS SECTION 
if not df.empty:
    st.sidebar.header("Filters")
    if 'overall_health' in df.columns:
        min_h, max_h = float(df['overall_health'].min()), float(df['overall_health'].max())
        h_range = st.sidebar.slider("Filter by Overall Health Score", min_h, max_h, (min_h, max_h))
        df_filtered = df[(df['overall_health'] >= h_range[0]) & (df['overall_health'] <= h_range[1])]
    else:
        df_filtered = df

    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)

    m1 = df_filtered['life_satisfaction'].mean()
    m2 = df_filtered['social_support_index'].mean()
    m3 = df_filtered['community_safety_index'].mean()
    m4 = df_filtered['emotion_management_index'].mean()

    col1.metric("✦ Avg. Life Sat.", f"{m1:.2f}", border=True)
    col2.metric("⚭ Social Support", f"{m2:.2f}", border=True)
    col3.metric("◈ Community Safety", f"{m3:.2f}", border=True)
    col4.metric("◉ Emotion Mgmt", f"{m4:.2f}", border=True)

st.markdown("---")
st.markdown("### Research Visualizations")

# VISUALIZATION 1: HEATMAP
with st.expander("Visualization 1: Correlation Heatmap", expanded=True):
    viz1_cols = ['life_satisfaction', 'social_support_index', 'community_safety_index', 'emotion_management_index', 'overall_health']
    available_cols = [c for c in viz1_cols if c in df.columns]
    
    if len(available_cols) > 1:
        corr = df[available_cols].corr()
        fig1 = px.imshow(corr, text_auto=".2f", color_continuous_scale='Reds', zmin=0, zmax=1)
        fig1.update_layout(title="<b>Variable Correlation Analysis</b>", title_x=0.5)
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("""<div style="background-color:#FFF0F5; padding:15px; border-radius:10px; border-left:5px solid #FFB6C1;">
        <b>Interpretation:</b> Safety and support have a strong 0.68 correlation, setting the basis for happiness.</div>""", unsafe_allow_html=True)

# VISUALIZATION 2: SCATTER
with st.expander("Visualization 2: Social & Community Impact", expanded=False):
    fig2 = px.scatter(df, x='social_support_index', y='life_satisfaction', color='community_safety_index', color_continuous_scale='Reds')
    st.plotly_chart(fig2, use_container_width=True)

# VISUALIZATION 3: HISTOGRAM
with st.expander("Visualization 3: Distribution of Scores", expanded=True):
    selected_dist = st.selectbox("Select Index:", ['life_satisfaction', 'social_support_index', 'emotion_management_index'])
    
    if selected_dist == 'emotion_management_index':
        text = "The majority have a 'neutral' capacity to control emotions (Score 3)."
    else:
        text = "Data shows a right-skewed distribution, meaning high overall scores."

    fig3 = px.histogram(df, x=selected_dist, nbins=20, marginal="rug", color_discrete_sequence=['#D32F2F'])
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown(f"""<div style="background-color:#FFF5F5; padding:15px; border-radius:10px; border-left:5px solid #D32F2F;">
    <b>Interpretation:</b> {text}</div>""", unsafe_allow_html=True)

# VISUALIZATION 4: RADAR
with st.expander("Visualization 4: Group Psychological Profile", expanded=False):
    vals = [df['life_satisfaction'].mean(), df['social_support_index'].mean(), df['community_safety_index'].mean(), df['emotion_management_index'].mean()]
    cats = ['Life Sat.', 'Social Support', 'Safety', 'Emotion Mgmt.']
    fig4 = go.Figure(data=go.Scatterpolar(r=vals + [vals[0]], theta=cats + [cats[0]], fill='toself', line=dict(color='#B22222', width=5)))
    st.plotly_chart(fig4, use_container_width=True)

# VISUALIZATION 5: BAR
with st.expander("Visualization 5: Community Safety Impact", expanded=False):
    safety_avg = df.groupby('community_safety_index')['life_satisfaction'].mean().reset_index()
    fig5 = px.bar(safety_avg, x='community_safety_index', y='life_satisfaction', color='life_satisfaction', color_continuous_scale='Reds')
    st.plotly_chart(fig5, use_container_width=True)

# VISUALIZATION 6: VIOLIN
with st.expander("Visualization 6: Emotional Stability", expanded=False):
    fig6 = px.violin(df, x='overall_health', y='emotion_management_index', color='overall_health', box=True, color_discrete_sequence=px.colors.sequential.Reds)
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")
