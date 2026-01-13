import streamlit as st
import pandas as pd
import plotly.express as px

# ===============================
# 🧠 PAGE TITLE CONFIGURATION
# ===============================
import streamlit as st

# --------------------
# Streamlit UI - Enhanced Title
# --------------------
st.markdown(
    '<div class="center-title">📌 Comparative Analysis Across Employment Status Groups</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Exploring social and emotional skills, well-being outcome, and community engagement</div>',
    unsafe_allow_html=True
)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ---------- Enhanced Custom CSS ----------
st.markdown("""
<style>

/* ---------- Main Title ---------- */
.center-title {
    text-align: center;
    font-size: 2.6rem;
    font-weight: 900;
    margin-bottom: 0.4rem;
    background: linear-gradient(90deg, #2563EB, #7C3AED);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    transition: transform 0.3s ease;
}

.center-title:hover {
    transform: scale(1.02);
}

/* ---------- Subtitle ---------- */
.subtitle {
    text-align: center;
    font-size: 1.15rem;
    color: #64748B;
    margin-bottom: 1.6rem;
    letter-spacing: 0.3px;
}

/* ---------- Animated Divider ---------- */
.divider {
    height: 1.5px;
    width: 100%;
    background: linear-gradient(
        90deg,
        #2563EB,
        #22C55E,
        #F97316,
        #7C3AED
    );
    background-size: 300% 100%;
    border-radius: 8px;
    animation: gradientMove 6s ease infinite;
    margin: 1.4rem 0 2.2rem 0;
}

/* Divider animation */
@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

</style>
""", unsafe_allow_html=True)


# -------------------------------
# Load dataset from GitHub
# -------------------------------
DATA_URL = "https://raw.githubusercontent.com/nhusna01/SSES-survey-dashboard/refs/heads/main/dataset/Husna_SSES_cleaned.csv"

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data(DATA_URL)
    
# ===============================
# 🧩 MAIN OBJECTIVE
# ===============================
import streamlit as st

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    .main-objectives-box {
        font-family: 'Inter', sans-serif;
        border-left: 6px solid #6A0DAD;
        background-color: #f6f1fb;
        padding: 1.5rem 2rem;   /* Original padding */
        border-radius: 15px;     /* Original rounded corners */
        margin-bottom: 8rem;   /* Original spacing below */
        max-width: 1000px;         /* Original width */
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
        <div class="main-objectives-title">📌 Main Objective</div>
        <div class="main-objectives-text">
            To examine how social and emotional skills, well-being, and life satisfaction,
            and community engagement differ across employment status groups, namely students,
            employed and unemployed individuals.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ===============================
# 📋 DATA SUMMARY
# ===============================
st.subheader("📋 Data Summary")

summary_option = st.selectbox(
    "Select summary type:",
    [
        "Overall Dataset Overview",
        "Categorical Variables Summary",
        "Numerical Variables Summary",
        "Missing Values Summary"
    ]
)

# ---------- OVERALL SUMMARY ----------
if summary_option == "Overall Dataset Overview":
    st.markdown("**Dataset Structure and Basic Information**")

    summary_df = pd.DataFrame({
        "Metric": [
            "Number of Observations",
            "Number of Variables",
            "Number of Numerical Variables",
            "Number of Categorical Variables"
        ],
        "Value": [
            df.shape[0],
            df.shape[1],
            df.select_dtypes(include='number').shape[1],
            df.select_dtypes(exclude='number').shape[1]
        ]
    })

    st.dataframe(summary_df, use_container_width=True)

# ---------- DATASET SUMMARY ----------
st.markdown("**Full Dataset Summary**")
st.dataframe(df, use_container_width=True)

# ---------- CATEGORICAL SUMMARY ----------
elif summary_option == "Categorical Variables Summary":
    st.markdown("**Frequency Distribution of Categorical Variables**")

    categorical_cols = df.select_dtypes(exclude='number').columns

    selected_cat = st.selectbox(
        "Select a categorical variable:",
        categorical_cols
    )

    st.write(df[selected_cat].value_counts())
    st.bar_chart(df[selected_cat].value_counts())

# ---------- NUMERICAL SUMMARY ----------
elif summary_option == "Numerical Variables Summary":
    st.markdown("**Descriptive Statistics for Numerical Variables**")

    numerical_cols = df.select_dtypes(include='number').columns

    selected_num = st.selectbox(
        "Select a numerical variable:",
        numerical_cols
    )

    st.dataframe(df[selected_num].describe().to_frame(name="Value"))

    st.markdown("**Distribution**")
    st.bar_chart(df[selected_num])

# ---------- MISSING VALUES ----------
elif summary_option == "Missing Values Summary":
    st.markdown("**Missing Data Overview**")

    missing_df = pd.DataFrame({
        "Variable": df.columns,
        "Missing Count": df.isnull().sum(),
        "Missing Percentage (%)": (df.isnull().mean() * 100).round(2)
    })

    missing_df = missing_df[missing_df["Missing Count"] > 0]

    if missing_df.empty:
        st.success("No missing values detected in the dataset.")
    else:
        st.dataframe(missing_df, use_container_width=True)

# ===============================
#  SUMMARY BOXES
# ===============================

st.subheader("📊 Dataset Summary")

# Ensure routing state exists
if "selected_objective" not in st.session_state:
    st.session_state.selected_objective = None

# --- Custom purple card styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

div.stButton > button {
    height: 140px;
    width: 100%;
    font-family: 'Inter', sans-serif;
    font-size: 16px;
    font-weight: 600;
    color: #4B0082;
    background: linear-gradient(145deg, #f6f1ff, #ede3ff);
    border: 1px solid #c7b2ff;
    border-radius: 18px;
    box-shadow: 0 8px 22px rgba(106,13,173,0.18);
    transition: all 0.25s ease-in-out;
    white-space: pre-line;
}
div.stButton > button:hover {
    transform: translateY(-5px);
    box-shadow: 0 14px 30px rgba(106,13,173,0.35);
    background: linear-gradient(145deg, #ede3ff, #e0d3ff);
}
</style>
""", unsafe_allow_html=True)

# --- Metrics ---
total_participants = len(df)

employment_col = next(
    (c for c in df.columns if "employment" in c.lower() or "status" in c.lower()),
    None
)
employment_groups = df[employment_col].nunique() if employment_col else "N/A"

wellbeing_cols = [c for c in df.columns if "wellbeing" in c.lower() or "satisfaction" in c.lower()]
avg_wellbeing = round(df[wellbeing_cols].mean().mean(), 2) if wellbeing_cols else "N/A"

community_cols = [c for c in df.columns if "community" in c.lower() or "participation" in c.lower()]
community_rate = (
    f"{round(df[community_cols].notna().mean().mean() * 100, 1)}%"
    if community_cols else "N/A"
)

# --- Render clickable cards ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button(f"👥\n{total_participants}\nTotal Participants"):
        st.session_state.selected_objective = "demographics"
        st.rerun()

with col2:
    if st.button(f"🎓\n{employment_groups}\nEmployment Groups"):
        st.session_state.selected_objective = "demographics"
        st.rerun()

with col3:
    if st.button(f"😊\n{avg_wellbeing}\nAvg Wellbeing"):
        st.session_state.selected_objective = "wellbeing"
        st.rerun()

with col4:
    if st.button(f"🏘️\n{community_rate}\nCommunity Participation"):
        st.session_state.selected_objective = "community"
        st.rerun()

selected_group = st.segmented_control(
    "Employment Status",
    options=["Students", "Employed", "Unemployed"]
)

status_mapping = {
    "Students": 1,
    "Employed": 0,
    "Unemployed": 2
}

if selected_group:
    filtered_df = df[df["employment_status"] == status_mapping[selected_group]]
    st.caption(f"Currently viewing data for: **{selected_group}**")



# ===============================
# 🔹 Sub-Objectives Dropdown
# ===============================
subobjectives = {
    "Demographics": "① Visualization: Demographic Distribution by Employment Status",
    "Wellbeing & Life Satisfaction": "② Visualization: Wellbeing Across Employment Status",
    "Behavioral Traits": "③ Visualization: Behavioral Traits Across Employment Status",
    "Community Participation": "④ Visualization: Community Participation Across Employment Status"
}

selected_sub = st.selectbox(
    "Select a sub-objective to explore:",
    list(subobjectives.keys())
)

st.markdown(f"### {selected_sub}")
st.markdown(f"**{subobjectives[selected_sub]}**")

# ===============================
# 🔹 Filter and plot visualizations per sub-objective
# ===============================

if selected_sub == "Demographics":
    demo_cols = ["gender", "age", "education_level", "location"]
    selected_demo = st.selectbox("Select demographic variable:", [c for c in demo_cols if c in df.columns])
    
    fig = px.pie(
        df,
        names=selected_demo,
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected_sub == "Wellbeing & Life Satisfaction":
    wellbeing_cols = [c for c in df.columns if "wellbeing" in c.lower() or "satisfaction" in c.lower()]
    selected_wellbeing = st.selectbox("Select wellbeing variable:", wellbeing_cols)
    
    fig = px.bar(
        df,
        x="employment_status",
        y=selected_wellbeing,
        color="employment_status",
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected_sub == "Behavioral Traits":
    behavior_cols = [c for c in df.columns if any(k in c.lower() for k in ["task", "adapt", "belief", "persistence", "learning"])]
    selected_behavior = st.selectbox("Select behavioral trait:", behavior_cols)
    
    fig = px.bar(
        df,
        x="employment_status",
        y=selected_behavior,
        color="employment_status",
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig, use_container_width=True)

elif selected_sub == "Community Participation":
    community_cols = [c for c in df.columns if "community" in c.lower() or "participation" in c.lower()]
    selected_community = st.selectbox("Select community variable:", community_cols)
    
    fig = px.bar(
        df,
        x="employment_status",
        y=selected_community,
        color="employment_status",
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig, use_container_width=True)
