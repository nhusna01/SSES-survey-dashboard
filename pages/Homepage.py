import streamlit as st
import plotly.express as px

df = st.session_state.df
st.error("🚨 HOMEPAGE UPDATED 🚨")


# Header + logo
st.markdown("""
<style>
.center-title { text-align: center; }
.top-right-logo { position: absolute; top: 10px; right: 20px; height: 60px; }
</style>

<div class="center-title">
    <h1 style="color:#4B0082; font-size:48px; font-weight:bold;">
        🏠 SSES Survey Dashboard
    </h1>
    <p style="color:#555; font-size:20px;">
        Interactive dashboard for Emotional Resilience & Personal Development
    </p>
</div>

<img class="top-right-logo" src="https://img.icons8.com/color/64/000000/brain.png">
""", unsafe_allow_html=True)


# Metrics and data preview
st.subheader("📌 Dashboard Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">📋 Total Responses</div>
        <div class="metric-value">{len(df)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🧩 Total Variables</div>
        <div class="metric-value">{df.shape[1]}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">⚠️ Missing Values</div>
        <div class="metric-value">{df.isna().sum().sum()}</div>
    </div>
    """, unsafe_allow_html=True)

with st.expander("🔍 View Dataset Preview"):
    st.dataframe(df, use_container_width=True)
    
with st.expander("📈 View Summary Statistics"):
    st.write(df.describe(include="all"))

# Demographics
st.subheader("👥 Demographic Analysis")
demo_col = st.selectbox(
    "Select Demographic Variable to Visualize",
    options=['gender', 'age', 'location', 'education_level'] if 'gender' in df.columns else df.columns
)
col1, col2 = st.columns([2, 1])
with col1:
    fig = px.pie(df, names=demo_col, hole=0.4,
                title=f"Distribution of {demo_col.replace('_',' ').title()}",
                color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.dataframe(df[demo_col].value_counts(), use_container_width=True)



    
