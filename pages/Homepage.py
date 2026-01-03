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


# ===============================
# 📌 Dashboard Overview (Summary Box)
# ===============================

st.subheader("📌 Dashboard Overview")

# --- Summary box styles ---
st.markdown(
    """
    <style>
    .summary-box {
        background-color: #f5f7fb;
        border-left: 6px solid #6a5acd;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        box-shadow: 0 6px 16px rgba(0,0,0,0.08);
        margin-top: 1rem;
    }
    .summary-title {
        font-size: 22px;
        font-weight: 700;
        color: #4B0082;
        margin-bottom: 1rem;
    }
    .summary-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
    }
    .summary-item {
        text-align: center;
    }
    .summary-value {
        font-size: 36px;
        font-weight: bold;
        color: #2c2c54;
    }
    .summary-label {
        font-size: 15px;
        color: #666;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Summary box content ---
st.markdown(
    f"""
    <div class="summary-box">
        <div class="summary-title">📌 Dashboard Overview</div>
        <div class="summary-grid">
            <div class="summary-item">
                <div class="summary-value">{len(df)}</div>
                <div class="summary-label">Total Responses</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">{df.shape[1]}</div>
                <div class="summary-label">Total Variables</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">{df.isna().sum().sum()}</div>
                <div class="summary-label">Missing Values</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)



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



    
