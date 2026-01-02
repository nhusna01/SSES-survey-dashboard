import streamlit as st
from preprocess import load_data

# Note: st.set_page_config is NOT needed here if it's already in app.py
# But the title and data loading should live here now.

st.title("🏠 SSES Survey Dashboard")
st.markdown("""
An interactive dashboard for analysing **emotional resilience and personal development** based on the SSES survey responses.
""")

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
