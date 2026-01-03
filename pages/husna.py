import streamlit as st
import pandas as pd
import plotly.express as px

# ===============================
# 🌟 PAGE CONFIG (MUST BE FIRST)
# ===============================
st.set_page_config(
    page_title="🧩 HUSNA Analysis",
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
# 🧩 PAGE HEADER
# ===============================
st.markdown(
    """
    <div style="text-align:center; margin-bottom: 1.5rem;">
        <h1 style="color:#FF4500; font-size:42px;">🧩 HUSNA Analysis</h1>
        <p style="color:#555; font-size:18px;">
            Examining demographic characteristics, wellbeing, behavioral traits,
            and community participation across employment status groups
        </p>
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

# ===============================
# 📄 DATASET PREVIEW (OPTIONAL)
# ===============================
with st.expander("📄 View Dataset Preview"):
    st.dataframe(df, use_container_width=True)
