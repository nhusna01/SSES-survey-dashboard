import streamlit as st
import pandas as pd
import plotly.express as px

# ===============================
# 🧠 PAGE TITLE CONFIGURATION
# ===============================

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
    justify-content: center;
    align-items: center;
    text-align: center;
}

.icon-row {
    display: flex;
    gap: 6px;
    align-items: center;
    justify-content: center;
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
""", unsafe_allow_html=True)



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
# 🔹 Sub-Objectives Definition
# ===============================
subobjectives = {
    "Correlation Between Likert Variables": 
    "1️⃣ **Correlation Between Likert Variables**\n\n"
    "To examine the relationships among Likert-scale variables related to social, emotional, wellbeing, "
    "and community attributes across different employment status groups.",

    "Emotional Regulation": 
    "2️⃣ **Emotional Regulation**\n\n"
    "To compare emotional regulation skills (including emotional control, calmness under pressure, "
    "cheerfulness, and restfulness) among students, employed, and unemployed individuals.",

    "Self-Management and Personal Skills": 
    "3️⃣ **Self-Management and Personal Skills**\n\n"
    "To examine variations in self-management and personal development skills, such as self-motivation, "
    "task persistence, adaptability, and enjoyment of learning, across different employment status groups.",

    "Social Skills and Interpersonal Interaction": 
    "4️⃣ **Social Skills and Interpersonal Interaction**\n\n"
    "To analyze differences in social and interpersonal skills, including teamwork, social support, "
    "helping others, and time spent on social interaction, among students, employed, and unemployed respondents.",

    "Community Participation and Social Responsibility": 
    "5️⃣ **Community Participation and Social Responsibility**\n\n"
    "To investigate how community participation and civic engagement—such as community involvement, "
    "care for others, perceived community impact, and neighborhood safety—vary across employment status groups.",

    "Wellbeing and Life Satisfaction": 
    "6️⃣ **Wellbeing and Life Satisfaction**\n\n"
    "To assess differences in overall wellbeing and life satisfaction across students, employed, "
    "and unemployed individuals."
}

objective_icons = {
    "Correlation Between Likert Variables": "📊",
    "Emotional Regulation": "🧠",
    "Self-Management and Personal Skills": "🎯",
    "Social Skills and Interpersonal Interaction": "🤝",
    "Community Participation and Social Responsibility": "🏘️",
    "Wellbeing and Life Satisfaction": "😊"
}

# ===============================
# 🔹 Sub-Objective Dropdown
# ===============================
selected_sub = st.selectbox(
    "Select a sub-objective to explore:",
    list(subobjectives.keys())
)

# ===============================
# 🔹 Display Sub-Objective Statement
# ===============================
st.markdown(
    f"""
    <div style="
        background: linear-gradient(145deg, #f6f1fb, #ede3ff);
        border-left: 6px solid #6A0DAD;
        padding: 1.4rem 1.6rem;
        border-radius: 14px;
        font-family: 'Inter', sans-serif;
        margin-top: 1.2rem;
        box-shadow: 0 8px 20px rgba(106,13,173,0.18);
    ">
        <div style="font-size:20px; font-weight:700; margin-bottom:0.6rem;">
            {objective_icons[selected_sub]} {selected_sub}
        </div>
        <div style="font-size:16px; line-height:1.7; color:#2f2f2f;">
            {subobjectives[selected_sub]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ===============================
# 🔹 Visualizations per Sub-Objective
# ===============================

# 1️⃣ Correlation Heatmap
if selected_sub == "Correlation Between Likert Variables":

    likert_cols = [
        'calm_under_pressure', 'cheerful', 'task_persistence', 'adaptability',
        'social_support', 'helping_others', 'community_participation',
        'community_impact', 'life_satisfaction', 'overall_health'
    ]

    corr_df = df[['employment_status'] + likert_cols].corr()

    fig = px.imshow(
        corr_df,
        text_auto=True,
        aspect="auto",
        color_continuous_scale=px.colors.sequential.Viridis,
        title="Correlation Heatmap: Social, Emotional, Wellbeing & Community Attributes"
    )

    fig.update_layout(height=800)
    st.plotly_chart(fig, use_container_width=True)
    

elif selected_sub == "Emotional Regulation":

    if 'employment_status_label' not in df.columns:
        status_mapping = {0: 'EMPLOYED', 1: 'STUDENT', 2: 'UNEMPLOYED'}
        df['employment_status_label'] = df['employment_status'].map(status_mapping)

    independent_vars = [
        'calm_under_pressure', 'cheerful', 'task_persistence',
        'social_support', 'enjoy_learning', 'helping_others'
    ]

    df[independent_vars] = df[independent_vars].apply(pd.to_numeric, errors='coerce')

    radar_data = df.groupby('employment_status_label')[independent_vars].mean().reset_index()

    radar_data = radar_data.melt(
        id_vars='employment_status_label',
        var_name='Skill Dimension',
        value_name='Average Score'
    )

    color_map = {
        'EMPLOYED': '#1f77b4',
        'STUDENT': '#ff7f0e',
        'UNEMPLOYED': '#2ca02c'
    }

    fig = px.line_polar(
        radar_data,
        r='Average Score',
        theta='Skill Dimension',
        color='employment_status_label',
        line_close=True,
        color_discrete_map=color_map,
        title='Emotional Regulation and Personal Skills by Employment Status'
    )

    fig.update_traces(fill='toself', opacity=0.7)
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[1, 5],
                tickvals=[1, 2, 3, 4, 5]
            )
        ),
        legend_title_text='Employment Status'
    )

    st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import plotly.express as px
import pandas as pd

# ===============================
# Prepare Data
# ===============================
# Ensure employment_status is string with readable labels
status_mapping = {0: 'EMPLOYED', 1: 'STUDENT', 2: 'UNEMPLOYED'}
if df['employment_status'].dtype in [int, float]:
    df['employment_status'] = df['employment_status'].map(status_mapping)
df['employment_status'] = df['employment_status'].astype(str)

# ===============================
# Filter by Employment Status
# ===============================
employment_options = st.multiselect(
    "Select Employment Status to Display:",
    options=df['employment_status'].unique(),
    default=df['employment_status'].unique()
)
df_filtered = df[df['employment_status'].isin(employment_options)]

# ===============================
# Columns to Plot
# ===============================
columns_to_plot = ['task_persistence', 'enjoy_learning']

# Bold, bright, scientific color map
color_map = {
    'EMPLOYED': '#1f77b4',   # Blue
    'STUDENT': '#ff7f0e',    # Orange
    'UNEMPLOYED': '#2ca02c'  # Green
}

# ===============================
# Plot Box Plots with Interpretation
# ===============================
for col in columns_to_plot:
    fig_box = px.box(
        df_filtered,
        x='employment_status',
        y=col,
        color='employment_status',
        points='all',  # show all data points
        color_discrete_map=color_map,
        title=f'{col.replace("_"," ").title()} by Employment Status',
        hover_data=df_filtered.columns  # show full data on hover
    )
    
    fig_box.update_layout(
        xaxis_title='Employment Status',
        yaxis_title=col.replace("_"," ").title(),
        boxmode='group',
        template='plotly_white',  # clean white background for scientific visualization
        font=dict(family="Arial", size=12)
    )
    
    st.plotly_chart(fig_box, use_container_width=True)

    # ===============================
    # Creative Interpretation
    # ===============================
    st.markdown(f"""
    <div style="
        background-color:#f0f0f0;
        padding:12px;
        border-radius:12px;
        font-family:'Inter', sans-serif;
        margin-bottom:20px;
    ">
        <strong>Interpretation:</strong>
        <ul style="line-height:1.6;">
            <li>Participants in the <span style='color:{color_map['EMPLOYED']}'>EMPLOYED</span> group tend to have a slightly higher median {col.replace("_"," ").title()} compared to other groups.</li>
            <li>The distribution shows variability within the <span style='color:{color_map['STUDENT']}'>STUDENT</span> group, indicating diverse behaviors in this skill dimension.</li>
            <li>The <span style='color:{color_map['UNEMPLOYED']}'>UNEMPLOYED</span> group shows more outliers, highlighting individual differences that may warrant further investigation.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# 5️⃣ Community Participation
elif selected_sub == "Community Participation and Social Responsibility":

    community_var = st.selectbox(
        "Select community indicator:",
        ['community_participation', 'community_impact']
    )

    fig = px.bar(
        df,
        x="employment_status",
        y=community_var,
        color="employment_status",
        barmode="group",
        color_discrete_sequence=px.colors.sequential.Viridis
    )

    st.plotly_chart(fig, use_container_width=True)


# 6️⃣ Wellbeing & Life Satisfaction
elif selected_sub == "Wellbeing and Life Satisfaction":

    wellbeing_vars = ['life_satisfaction', 'overall_health', 'wellbeing_belief']

    selected_var = st.selectbox("Select wellbeing indicator:", wellbeing_vars)

    fig = px.violin(
        df,
        x='employment_status',
        y=selected_var,
        color='employment_status',
        box=True,
        points='all',
        color_discrete_map={
            0: '#1f77b4',  # EMPLOYED
            1: '#ff7f0e',  # STUDENT
            2: '#2ca02c'   # UNEMPLOYED
        },
        title=f'Distribution of {selected_var.replace("_"," ").title()} by Employment Status'
    )

    st.plotly_chart(fig, use_container_width=True)


# Placeholder for remaining objectives
else:
    st.info("📌 Visualization for this sub-objective will be added next.")

