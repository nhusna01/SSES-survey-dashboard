import streamlit as st
import pandas as pd
import plotly.express as px

# ===============================
# 🌟 Page Config
# ===============================
st.set_page_config(
    page_title="🧩 HUSNA Analysis",
    page_icon="👤",
    layout="wide"
)

# ===============================
# ✅ Load data
# ===============================
if "df" not in st.session_state:
    st.warning("❌ Dataset not loaded. Please check main.py")
    st.stop()
else:
    df = st.session_state.df

# ===============================
# 🧩 Page Header
# ===============================
st.markdown("""
<div style="text-align:center;">
    <h1 style="color:#FF4500; font-size:42px;">🧩 HUSNA Analysis</h1>
    <p style="color:#555; font-size:18px;">
        Explore demographic, wellbeing, behavioral traits, and community participation by employment status
    </p>
</div>
""", unsafe_allow_html=True)

# ===============================
# 🎯 Main Objectives as Clickable Cards
# ===============================
st.subheader("🎯 Main Objectives")

# Define main objectives and icons
main_objectives = [
    {"title": "Demographics", "icon": "👥", "key": "demographics"},
    {"title": "Wellbeing & Life Satisfaction", "icon": "😊", "key": "wellbeing"},
    {"title": "Behavioral Traits", "icon": "🧩", "key": "behavior"},
    {"title": "Community Participation", "icon": "🏘️", "key": "community"}
]

# CSS for summary boxes
st.markdown("""
<style>
.objectives-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
    margin-bottom: 2rem;
}
.objective-card {
    border: 2px solid #FF4500;
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
    transition: all 0.2s ease-in-out;
    background-color: #ffffff;
    cursor: pointer;
}
.objective-card:hover {
    border-color: #FF6347;
    box-shadow: 0 6px 16px rgba(255,99,71,0.25);
    transform: translateY(-3px);
}
.objective-icon {
    font-size: 36px;
    margin-bottom: 0.5rem;
}
.objective-title {
    font-size: 20px;
    font-weight: bold;
    color: #FF4500;
    margin-bottom: 0.3rem;
}
</style>
""", unsafe_allow_html=True)

# Render clickable cards as Streamlit buttons
st.write("Click a card to explore the analysis:")
cols = st.columns(4)
selected_objective = None
for idx, obj in enumerate(main_objectives):
    with cols[idx]:
        if st.button(f"{obj['icon']}\n{obj['title']}", key=obj['key']):
            selected_objective = obj['key']

# ===============================
# 🔽 Filtered Analysis Based on Selected Objective
# ===============================
if selected_objective is None:
    st.info("Select a main objective above to view its analysis")
else:
    st.subheader(f"📊 {selected_objective.replace('_',' ').title()} Analysis")

    if selected_objective == "demographics":
        demo_cols = ['gender', 'age', 'location', 'education_level']
        for col in demo_cols:
            if col in df.columns:
                st.markdown(f"### {col.title()}")
                fig = px.pie(df, names=col, hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(df[col].value_counts(), use_container_width=True)

    elif selected_objective == "wellbeing":
        wellbeing_cols = [c for c in df.columns if 'wellbeing' in c.lower() or 'satisfaction' in c.lower()]
        if wellbeing_cols:
            for col in wellbeing_cols:
                st.markdown(f"### {col.replace('_',' ').title()}")
                st.bar_chart(df[col])
        else:
            st.info("No wellbeing/life satisfaction columns found in dataset.")

    elif selected_objective == "behavior":
        behavior_cols = [c for c in df.columns if 'behavior' in c.lower()]
        if behavior_cols:
            for col in behavior_cols:
                st.markdown(f"### {col.replace('_',' ').title()}")
                st.bar_chart(df[col])
        else:
            st.info("No behavioral trait columns found in dataset.")

    elif selected_objective == "community":
        community_cols = [c for c in df.columns if 'community' in c.lower() or 'participation' in c.lower()]
        if community_cols:
            for col in community_cols:
                st.markdown(f"### {col.replace('_',' ').title()}")
                st.bar_chart(df[col])
        else:
            st.info("No community participation columns found in dataset.")
