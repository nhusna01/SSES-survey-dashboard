import streamlit as st
from preprocess import load_data
import plotly.express as px

def show_home():
    df = st.session_state.df  # get the dataset loaded in main.py

    # --- HEADER + LOGO ---
    st.markdown("""
    <style>
    .center-title { text-align: center; }
    .top-right-logo { position: absolute; top: 10px; right: 20px; height: 60px; }
    .css-18e3th9 { padding-top: 1rem; padding-right: 3rem; padding-left: 3rem; padding-bottom: 0rem; }
    </style>

    <div class="center-title">
        <h1 style="color:#4B0082; font-size:48px; font-weight:bold;">
            🏠 SSES Survey Dashboard
        </h1>
        <p style="color:#555; font-size:20px;">
            Interactive dashboard for Emotional Resilience & Personal Development
        </p>
    </div>

    <img class="top-right-logo" src="https://img.icons8.com/color/64/000000/brain.png" alt="Logo">
    """, unsafe_allow_html=True)

    # --- TOP METRICS ---
    st.subheader("📌 Dashboard Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Responses", len(df))
    col2.metric("Total Variables", df.shape[1])
    col3.metric("Missing Values", df.isna().sum().sum())

    # --- DATA PREVIEW ---
    with st.expander("🔍 View Dataset Preview"):
        st.dataframe(df, use_container_width=True)

    with st.expander("📈 View Summary Statistics"):
        st.write(df.describe(include="all"))

    # --- DEMOGRAPHIC ANALYSIS ---
    st.subheader("👥 Demographic Analysis")
    st.markdown("Explore the background and characteristics of the survey respondents.")

    # Choose column for visualization
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

    st.markdown("---")
    st.markdown("""
    ### 📂 Available Analysis Pages
    Use the **sidebar** to navigate between other analysis pages:
    - **Machine Learning**: Predict patterns using trained models.
    - **Survey Charts**: Visualise individual question responses.
    - **Emotion Resilience**: Deep dive into emotional health scores.
    """)

