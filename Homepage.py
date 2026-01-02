import streamlit as st
from preprocess import load_data

# Note: st.set_page_config is NOT needed here if it's already in app.py
# But the title and data loading should live here now.

# Set page config
st.set_page_config(
    page_title="🏠 SSES Survey Dashboard",
    page_icon="📊",
    layout="wide"
)


# Title and description
st.title("🏠 SSES Survey Dashboard")
# CSS to make the page background white and remove padding
st.markdown("""
<style>
/* Remove default padding for a cleaner look */
.css-18e3th9 {
    padding-top: 1rem;
    padding-right: 3rem;
    padding-left: 3rem;
    padding-bottom: 0rem;
}

/* Center the title and subtitle */
.center-title {
    text-align: center;
}

/* Logo at top-right corner */
.top-right-logo {
    position: absolute;
    top: 10px;
    right: 20px;
    height: 60px;
}
</style>
""", unsafe_allow_html=True)

# HTML for centered title and subtitle + top-right logo
st.markdown("""
<div class="center-title">
    <h1 style="color:#4B0082; font-size:48px; font-weight:bold;">
        🏠 SSES Survey Dashboard
    </h1>
    <p style="color:#555; font-size:20px;">
        Interactive dashboard for Emotional Resilience & Personal Development
    </p>
</div>

<!-- Logo top-right -->
<img class="top-right-logo" src="https://img.icons8.com/color/64/000000/brain.png" alt="Logo">
""", unsafe_allow_html=True)

st.markdown("""
<div style="
    text-align: center; 
    font-family: 'Arial'; 
    font-size: 50px; 
    font-weight: bold; 
    color: white; 
    background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
    padding: 20px; 
    border-radius: 10px;">
    🏠 SSES Survey Dashboard
</div>
<p style="text-align:center; color:#555; font-size:18px;">
Interactive dashboard for Emotional Resilience & Personal Development
</p>
""", unsafe_allow_html=True)

# Add top metrics using columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Respondents", value="1,250", delta="5% ⬆")
with col2:
    st.metric(label="Average Resilience Score", value="78.6", delta="-2% ⬇")
with col3:
    st.metric(label="Average Development Score", value="82.3", delta="3% ⬆")

st.markdown("---")  # horizontal divider

# Optional: add a sidebar description
st.sidebar.header("Dashboard Controls")
st.sidebar.markdown(
    "Filter the survey data, select metrics, or visualize trends interactively."
)


# Load Data
df = load_data()

# ======================================
# OVERVIEW SECTION
# ======================================
st.subheader("📌 Dashboard Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Total Responses", len(df))
col2.metric("Total Variables", df.shape[1])
col3.metric("Missing Values", df.isna().sum().sum())

# ======================================
# DATA PREVIEW
# ======================================
with st.expander("🔍 View Dataset Preview"):
    st.dataframe(df, use_container_width=True)

with st.expander("📈 View Summary Statistics"):
    st.write(df.describe(include="all"))

import streamlit as st
import plotly.express as px
from preprocess import load_data

st.title("👥 Demographic Analysis")
st.markdown("Explore the background and characteristics of the survey respondents.")

df = load_data()

# Selection for distribution
demo_col = st.selectbox(
    "Select Demographic Variable to Visualize",
    options=['gender', 'age', 'location', 'education_level'] if 'gender' in df.columns else df.columns
)

col1, col2 = st.columns([2, 1])

with col1:
    fig = px.pie(
        df, 
        names=demo_col, 
        hole=0.4,
        title=f"Distribution of {demo_col.replace('_', ' ').title()}",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.write("### Quick Stats")
    stats = df[demo_col].value_counts()
    st.dataframe(stats, use_container_width=True)

st.markdown("""
### 📂 Available Analysis Pages
Use the **sidebar** to navigate between analysis pages:
- **Demographic Analysis**: Break down results by age, gender, and location.
- **Machine Learning**: Predict patterns using trained models.
- **Survey Charts**: Visualise individual question responses.
- **Emotion Resilience**: Deep dive into emotional health scores.
""")
