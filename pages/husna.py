import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data (assume it's already loaded in session_state)
df = st.session_state.df

# ===============================
# 🧩 HUSNA Analysis Header
# ===============================
st.markdown("""
<style>
.center-title { text-align: center; }
.top-right-logo { position: absolute; top: 10px; right: 20px; height: 60px; }
</style>

<div class="center-title">
    <h1 style="color:#FF4500; font-size:42px; font-weight:bold;">
        🧩 HUSNA Analysis
    </h1>
    <p style="color:#555; font-size:18px;">
        Summary of objectives and demographic insights
    </p>
</div>

<img class="top-right-logo" src="https://img.icons8.com/color/64/000000/analytics.png">
""", unsafe_allow_html=True)

# ===============================
# 🎯 Main Objectives
# ===============================
st.subheader("🎯 Main Objectives")
st.markdown("""
1. Understand demographic distribution of participants  
2. Analyze emotional resilience indicators  
3. Identify gaps in personal development areas  
4. Provide visual insights for each survey variable
""")

# ===============================
# 🔽 Sub-Objectives (Expandable)
# ===============================
st.subheader("🔽 Sub-Objectives")
objectives = {
    "Understand demographic distribution": [
        "Analyze gender distribution",
        "Analyze age distribution",
        "Analyze location distribution",
        "Analyze education level distribution"
    ],
    "Analyze emotional resilience indicators": [
        "Calculate average resilience score",
        "Identify low and high resilience groups",
        "Visualize resilience trends by demographics"
    ],
    "Identify gaps in personal development areas": [
        "Check missing data in key variables",
        "Identify areas with low engagement",
        "Compare variable correlations"
    ],
    "Provide visual insights for each survey variable": [
        "Pie charts for categorical variables",
        "Histograms for numerical variables",
        "Summary statistics tables"
    ]
}

for main_obj, subs in objectives.items():
    with st.expander(main_obj):
        for sub in subs:
            st.write(f"- {sub}")

# ===============================
# 📌 HUSNA Dashboard Overview (Summary Box)
# ===============================
st.subheader("📌 HUSNA Dashboard Overview")

st.markdown("""
<style>
.husna-container {
    border: 2px solid #FF4500;
    border-radius: 16px;
    padding: 1.5rem;
    background-color: #ffffff;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
}
.husna-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
}
.husna-card {
    border: 1px solid #ddd;
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
    transition: all 0.2s ease-in-out;
}
.husna-card:hover {
    border-color: #FF4500;
    box-shadow: 0 6px 16px rgba(255,69,0,0.25);
    transform: translateY(-3px);
}
.husna-icon {
    font-size: 34px;
    margin-bottom: 0.5rem;
}
.husna-value {
    font-size: 36px;
    font-weight: 700;
    color: #2c2c54;
}
.husna-label {
    font-size: 15px;
    color: #555;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="husna-container">
    <div class="husna-grid">
        <div class="husna-card">
            <div class="husna-icon">📋</div>
            <div class="husna-value">{len(df)}</div>
            <div class="husna-label">Total Responses</div>
        </div>
        <div class="husna-card">
            <div class="husna-icon">🧩</div>
            <div class="husna-value">{df.shape[1]}</div>
            <div class="husna-label">Total Variables</div>
        </div>
        <div class="husna-card">
            <div class="husna-icon">⚠️</div>
            <div class="husna-value">{df.isna().sum().sum()}</div>
            <div class="husna-label">Missing Values</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===============================
# 🔗 Streamlit Interactivity
# ===============================
st.subheader("🔗 Explore HUSNA Data")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 View Dataset"):
        st.info("Showing dataset preview")
        st.dataframe(df, use_container_width=True)

with col2:
    if st.button("🧩 Explore Variables"):
        st.info("List of variables")
        st.write(df.columns.tolist())

with col3:
    if st.button("⚠️ Inspect Missing Data"):
        st.info("Missing values summary")
        st.write(df.isna().sum())

# ===============================
# 👥 Demographic Analysis
# ===============================
st.subheader("👥 Demographic Analysis")
demo_col = st.selectbox(
    "Select Demographic Variable",
    options=['gender', 'age', 'location', 'education_level'] if 'gender' in df.columns else df.columns
)

col1, col2 = st.columns([2,1])
with col1:
    fig = px.pie(df, names=demo_col, hole=0.4,
                 title=f"Distribution of {demo_col.replace('_',' ').title()}",
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.dataframe(df[demo_col].value_counts(), use_container_width=True)
