import streamlit as st
import pandas as pd
import plotly.express as px

# ===============================
# 🌟 PAGE CONFIG (MUST BE FIRST)
# ===============================
st.set_page_config(
    page_title="🧩 Analysis of SSES",
    page_icon="👤",
    layout="wide"
)

# ===============================
# ✅ LOAD DATA FROM SESSION STATE
# ===============================
if "df" not in st.session_state:
    st.error("❌ Dataset not loaded. Please check main.py")
    st.stop()

df = st.session_state.df

# ===============================
# 📄 DATASET PREVIEW (OPTIONAL)
# ===============================
with st.expander("📄 View Dataset Preview"):
    st.dataframe(df, use_container_width=True)
    
# ===============================
# 🧩 PAGE HEADER
# ===============================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    .main-objectives-box {
        font-family: 'Inter', sans-serif;
        border-left: 6px solid #6A0DAD;
        background-color: #f6f1fb;
        padding: 1.6rem 2.2rem;
        border-radius: 14px;
        margin-bottom: 2rem;
    }
    .main-objectives-title {
        font-size: 26px;
        font-weight: 700;
        color: #4B0082;
        margin-bottom: 0.8rem;
    }
    .main-objectives-text {
        font-size: 17px;
        font-weight: 400;
        color: #2f2f2f;
        line-height: 1.7;
    }
    </style>

    <div class="main-objectives-box">
        <div class="main-objectives-title">🎯 Main Objective</div>
        <div class="main-objectives-text">
            To examine how demographic characteristics, wellbeing and life satisfaction,
            behavioral traits, and community participation vary across employment status
            groups, namely students, employed, and unemployed individuals.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ===============================
# 🎯 MAIN OBJECTIVES (CARDS)
# ===============================
st.subheader("🎯 Main Objectives")

# Initialize session state
if "selected_objective" not in st.session_state:
    st.session_state.selected_objective = None

objectives = [
    {"key": "demographics", "title": "Demographics", "icon": "👥"},
    {"key": "wellbeing", "title": "Wellbeing & Life Satisfaction", "icon": "😊"},
    {"key": "behavior", "title": "Behavioral Traits", "icon": "🧩"},
    {"key": "community", "title": "Community Participation", "icon": "🏘️"},
]

cols = st.columns(4)
for i, obj in enumerate(objectives):
    with cols[i]:
        if st.button(f"{obj['icon']}  {obj['title']}", key=obj["key"]):
            st.session_state.selected_objective = obj["key"]

# Reset button
if st.session_state.selected_objective:
    if st.button("🔄 Reset selection"):
        st.session_state.selected_objective = None
        st.rerun()

# ===============================
# 🔽 OBJECTIVE-BASED ANALYSIS
# ===============================
selected = st.session_state.selected_objective

if selected is None:
    st.info("⬆️ Select a main objective above to view its analysis")

# ---------- DEMOGRAPHICS ----------
elif selected == "demographics":
    st.subheader("👥 Demographic Analysis")

    demo_cols = ["gender", "age", "location", "education_level"]

    for col in demo_cols:
        if col in df.columns:
            st.markdown(f"### {col.replace('_',' ').title()}")
            fig = px.pie(
                df,
                names=col,
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df[col].value_counts(), use_container_width=True)

# ---------- WELLBEING ----------
elif selected == "wellbeing":
    st.subheader("😊 Wellbeing & Life Satisfaction")

    cols = [c for c in df.columns if "wellbeing" in c.lower() or "satisfaction" in c.lower()]

    if not cols:
        st.warning("No wellbeing or life satisfaction variables found.")
    else:
        for col in cols:
            st.markdown(f"### {col.replace('_',' ').title()}")
            st.bar_chart(df[col])

# ---------- BEHAVIOR ----------
elif selected == "behavior":
    st.subheader("🧩 Behavioral Traits")

    cols = [c for c in df.columns if "behavior" in c.lower()]

    if not cols:
        st.warning("No behavioral trait variables found.")
    else:
        for col in cols:
            st.markdown(f"### {col.replace('_',' ').title()}")
            st.bar_chart(df[col])

# ---------- COMMUNITY ----------
elif selected == "community":
    st.subheader("🏘️ Community Participation")

    cols = [c for c in df.columns if "community" in c.lower() or "participation" in c.lower()]

    if not cols:
        st.warning("No community participation variables found.")
    else:
        for col in cols:
            st.markdown(f"### {col.replace('_',' ').title()}")
            st.bar_chart(df[col])

