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
        margin-bottom: 3.5rem;   /* Original spacing below */
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

st.subheader("📊 Performance Metrics")

import streamlit as st
import pandas as pd

# -------------------- DATA --------------------
# df assumed already loaded

employment_mapping = {
    0: "Employed",
    1: "Student",
    2: "Unemployed"
}

attribute_cols = [
    "calm_under_pressure", "cheerful", "task_persistence",
    "social_support", "helping_others",
    "community_participation", "community_impact",
    "life_satisfaction", "overall_health"
]

# -------------------- METRICS --------------------
employment_groups = df["employment_status"].map(employment_mapping).nunique()
avg_overall_health = round(df["overall_health"].mean(), 2)
avg_community_participation = round(
    df[["community_participation", "community_impact"]].mean().mean(), 2
)
total_attributes = len(attribute_cols)

# -------------------- STYLING --------------------
st.markdown("""
<style>
.summary-card {
    font-family: 'Inter', sans-serif;
    height: 150px;
    border-radius: 18px;
    padding: 1.2rem;
    background: linear-gradient(145deg, #f6f1ff, #ede3ff);
    border: 1px solid #c7b2ff;
    box-shadow: 0 10px 24px rgba(106,13,173,0.25);
    display: flex;
    flex-direction: column;
    justify-content: center;     /* CENTER vertically */
    align-items: center;         /* CENTER horizontally */
    text-align: center;
}

.icon-row {
    display: flex;
    gap: 6px;
    align-items: center;
    justify-content: center;     /* CENTER icons */
    margin-bottom: 6px;
}

.summary-value {
    font-size: 28px;
    font-weight: 700;
    color: #2E0854;
    margin: 4px 0;
}

.summary-title {
    font-size: 15px;
    font-weight: 600;
    color: #4B0082;
}

.info-icon {
    font-size: 15px;
    cursor: help;
}
</style>


# -------------------- LAYOUT --------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="summary-card">
        <div class="icon-row">
            <span>👥</span>
            <span class="info-icon" title="Employment categories include: Student, Employed, and Unemployed">❓</span>
        </div>
        <div class="summary-value">{employment_groups}</div>
        <div class="summary-title">Employment Groups</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="summary-card">
        <div class="icon-row">
            <span>🧩</span>
            <span class="info-icon" title="Total number of key attributes analysed, including social, emotional, and wellbeing indicators">❓</span>
        </div>
        <div class="summary-value">{total_attributes}</div>
        <div class="summary-title">Total Attributes</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="summary-card">
        <div class="icon-row">
            <span>❤️</span>
            <span class="info-icon" title="Average score representing respondents’ overall perceived health status">❓</span>
        </div>
        <div class="summary-value">{avg_overall_health}</div>
        <div class="summary-title">Average Overall Health</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="summary-card">
        <div class="icon-row">
            <span>🏘️</span>
            <span class="info-icon" title="Average level of participation and impact within community-related activities">❓</span>
        </div>
        <div class="summary-value">{avg_community_participation}</div>
        <div class="summary-title">Avg Community Participation</div>
    </div>
    """, unsafe_allow_html=True)


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
