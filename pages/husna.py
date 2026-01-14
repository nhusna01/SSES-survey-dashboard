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
    "calm_under_pressure", "cheerful",
    "enjoy_learning", "task_persistence",
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
            <span class="info-icon" title="Total number of key attributes analysed, including social, emotional, community engagement and well-being indicators">❓</span>
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



# -----------------------------
# Sub-objectives and Icons
# -----------------------------
subobjectives = {
    "Correlation Between Likert Variables": 
        "1️⃣ **Correlation Between Likert Variables**\n\n"
        "To examine the relationships among Likert-scale variables related to social, emotional, and well-being, "
        "and community attributes across different employment status groups.",
    "Social & Emotional Skills": 
        "2️⃣ **Social & Emotional Skills**\n\n"
        "To compare emotional regulation skills including emotional control, social, "
        "emotional skills, and even interaction among students, employed, and unemployed individuals.",
    "Task Persistence & Enjoy Learning": 
        "3️⃣ **Task Persistence & Enjoy Learning**\n\n"
        "To examine variations in task persistence and enjoyment of learning across different employment status groups.",
    "Social Skills Grouped Bar Chart": 
        "4️⃣ **Social Skills and Interpersonal Interaction**\n\n"
        "To analyze differences in social and interpersonal skills, including social support, "
        "and helping others in social interaction.",
    "Community Participation": 
        "5️⃣ **Community Participation and Social Responsibility**\n\n"
        "To investigate how community participation and civic engagement vary across employment status groups.",
    "Wellbeing and Life Satisfaction": 
        "6️⃣ **Wellbeing and Life Satisfaction**\n\n"
        "To assess differences in overall well-being and life satisfaction across students, employed, and unemployed individuals."
}

objective_icons = {
    "Correlation Between Likert Variables": "📊",
    "Social & Emotional Skills": "🧠",
    "Task Persistence & Enjoy Learning": "🎯",
    "Social Skills Grouped Bar Chart": "🤝",
    "Community Participation": "🏘️",
    "Wellbeing and Life Satisfaction": "😊"
}

# -----------------------------
# Sidebar: Select Sub-Objective
# -----------------------------
selected_sub = st.sidebar.selectbox(
    "Select Objective / Chapter:",
    list(subobjectives.keys())
)


# Add space
st.markdown("<br><br>", unsafe_allow_html=True)

# -----------------------------
# Employment Status Filter
# -----------------------------
selected_group = st.segmented_control(
    "Employment Status Filter:",
    options=["All", "Students", "Employed", "Unemployed"]
)

status_mapping = {
    "Students": 1,
    "Employed": 0,
    "Unemployed": 2
}

if selected_group and selected_group != "All":
    filtered_df = df[df["employment_status"] == status_mapping[selected_group]]
else:
    filtered_df = df.copy()

st.caption(f"Currently viewing data for: **{selected_group}**")

# -----------------------------
# Prepare Labels and Colors
# -----------------------------
status_mapping_str = {0: 'EMPLOYED', 1: 'STUDENT', 2: 'UNEMPLOYED'}
if filtered_df['employment_status'].dtype in [int, float]:
    filtered_df['employment_status'] = filtered_df['employment_status'].map(status_mapping_str)
filtered_df['employment_status'] = filtered_df['employment_status'].astype(str)

filtered_df['employment_status_label'] = filtered_df['employment_status'].map({
    'EMPLOYED': 'Employed',
    'STUDENT': 'Student',
    'UNEMPLOYED': 'Unemployed'
})

color_map = {
    'EMPLOYED': '#440154',   # Dark purple
    'STUDENT': '#21918c',    # Bright teal
    'UNEMPLOYED': '#fde725'  # Bright yellow
}

# -----------------------------
# Display Sub-Objective Description
# -----------------------------
st.markdown(f"## {objective_icons[selected_sub]} {subobjectives[selected_sub]}")

# ===============================
# 1️⃣ Correlation Heatmap
# ===============================
st.title("Correlation Heatmap: Employment Status vs. Selected Likert Scale Variables")

if selected_sub == "Correlation Between Likert Variables":
    likert_cols = [
        'calm_under_pressure', 'cheerful', 'task_persistence', 'adaptability',
        'social_support', 'helping_others', 'community_participation',
        'community_impact', 'life_satisfaction', 'overall_health'
    ]

    cols_for_heatmap = ['employment_status'] + likert_cols
    df_corr = filtered_df[cols_for_heatmap].apply(pd.to_numeric, errors='coerce')
    correlation_matrix_specific = df_corr.corr()

    fig = px.imshow(
        correlation_matrix_specific,
        text_auto=True,
        aspect="auto",
        color_continuous_scale=px.colors.sequential.Viridis,
        title='Correlation Heatmap: Employment Status vs. Selected Likert Scale Variables'
    )

    fig.update_layout(
        xaxis_title='Variables',
        yaxis_title='Variables',
        xaxis_tickangle=-45,
        height=800,
        width=1000
    )

    st.plotly_chart(fig, use_container_width=True)

    # Interpretation
    st.markdown("""
    **Interpretation:**
    - `social_support` and `helping_others` show strong positive correlation, indicating linked social behaviors.  
    - Community engagement variables moderately correlate with `life_satisfaction` and `overall_health`.  
    - Employment status shows slight positive correlation with wellbeing metrics.  
    - Heatmap allows quick identification of key variables for interventions and predictive modeling.
    """)

    # Conclusion
    st.markdown("""
    **Conclusion for Correlation Heatmap:**
    - Social behaviors and community participation are linked to wellbeing.  
    - Employment status has mild association with life satisfaction and health.  
    - Highlights which variables could be targets for intervention.  
    - Useful for both descriptive and predictive insights.
    """)

# ===============================
# 2️⃣ Social & Emotional Skills Radar
# ===============================
elif selected_sub == "Social & Emotional Skills":
    independent_vars = [
        'calm_under_pressure', 'cheerful', 'task_persistence',
        'social_support', 'enjoy_learning', 'helping_others'
    ]
    filtered_df[independent_vars] = filtered_df[independent_vars].apply(pd.to_numeric, errors='coerce')
    radar_data = filtered_df.groupby('employment_status_label')[independent_vars].mean().reset_index()
    radar_data = radar_data.melt(
        id_vars='employment_status_label',
        var_name='Skill Dimension',
        value_name='Average Score'
    )

    color_map = {
        'EMPLOYED': '#440154',
        'STUDENT': '#21918c',
        'UNEMPLOYED': '#fde725'
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
        polar=dict(radialaxis=dict(visible=True, range=[1,5], tickvals=[1,2,3,4,5])),
        legend_title_text='Employment Status'
    )
    st.plotly_chart(fig, width='stretch')

    st.markdown("""
    **Interpretation:**
    - EMPLOYED participants consistently score higher across all skill dimensions.  
    - STUDENT group shows moderate skills with variability.  
    - UNEMPLOYED participants have lower scores.  
    - Radar chart efficiently compares multiple skills across employment groups.
    """)

    st.markdown("""
    **Conclusion for Social & Emotional Skills Radar:**
    - EMPLOYED group demonstrates stronger social and emotional skills.  
    - STUDENT group is moderate with some differences between dimensions.  
    - UNEMPLOYED group shows skill gaps that may need support.  
    - Radar chart visually summarizes skill patterns clearly.
    """)

# ===============================
# 3️⃣ Task Persistence & Enjoy Learning Boxplots
# ===============================
elif selected_sub == "Task Persistence & Enjoy Learning":
    columns_to_plot = ['task_persistence', 'enjoy_learning']
    employment_options = st.multiselect(
        "Filter Employment Status:",
        options=filtered_df['employment_status_label'].unique(),
        default=filtered_df['employment_status_label'].unique()
    )
    df_filtered = filtered_df[filtered_df['employment_status_label'].isin(employment_options)]

    color_map = {
        'EMPLOYED': '#440154',
        'STUDENT': '#21918c',
        'UNEMPLOYED': '#fde725'
    }

    for col in columns_to_plot:
        fig_box = px.box(
            df_filtered,
            x='employment_status_label',
            y=col,
            color='employment_status_label',
            points='all',
            color_discrete_map=color_map,
            title=f'{col.replace("_"," ").title()} by Employment Status'
        )
        fig_box.update_layout(
            xaxis_title='Employment Status',
            yaxis_title=col.replace("_"," ").title(),
            boxmode='group',
            template='plotly_white',
            font=dict(family="Arial", size=12)
        )
        st.plotly_chart(fig_box, width='stretch')

        st.markdown(f"""
        **Interpretation for {col.replace('_',' ').title()}:**
        - EMPLOYED participants tend to have higher median scores.  
        - STUDENT group shows moderate variability.  
        - UNEMPLOYED participants have more outliers.  
        - Box plot highlights spread and distributional differences.
        """)

    st.markdown("""
    **Conclusion for Task Persistence & Enjoy Learning Boxplots:**
    - EMPLOYED group is generally more persistent and enjoys learning more.  
    - STUDENT group has mixed results.  
    - UNEMPLOYED group may need additional support.  
    - Boxplots reveal individual variation and distribution patterns.
    """)

# ===============================
# 4️⃣ Social Skills Grouped Bar Chart
# ===============================
elif selected_sub == "Social Skills Grouped Bar Chart":
    social_skills = ['enjoy_learning', 'helping_others']
    selected_skills = st.multiselect(
        "Select Social Skill(s) to Display",
        options=social_skills,
        default=social_skills
    )

    if selected_skills:
        color_map = {
            'EMPLOYED': '#440154',
            'STUDENT': '#21918c',
            'UNEMPLOYED': '#fde725'
        }

        df_avg = (
            filtered_df
            .groupby('employment_status_label')[selected_skills]
            .mean()
            .reset_index()
        )
        df_avg['employment_status_label'] = df_avg['employment_status_label'].str.upper()

        df_melt = df_avg.melt(
            id_vars='employment_status_label',
            var_name='Social Skill',
            value_name='Average Score'
        )

        fig_groupbar = px.bar(
            df_melt,
            x='employment_status_label',
            y='Average Score',
            color='employment_status_label',
            barmode='group',
            title='Average Social Skill Scores by Employment Status',
            labels={'employment_status_label': 'Employment Status', 'Average Score': 'Mean Likert Score'},
            color_discrete_map=color_map
        )

        fig_groupbar.update_layout(
            template='plotly_white',
            font=dict(family="Arial", size=12),
            legend_title='Employment Status'
        )

        st.plotly_chart(fig_groupbar, use_container_width=True)

        st.markdown("""
        **Interpretation:**
        - EMPLOYED participants show higher average scores across selected skills.  
        - STUDENT group shows moderate performance.  
        - UNEMPLOYED participants score lower.  
        - Grouped bar chart allows comparison across employment groups.
        """)

        st.markdown("""
        **Conclusion for Social Skills Grouped Bar Chart:**
        - Highlights clear differences in social skill levels by employment.  
        - Useful to identify skill gaps and target interventions.  
        - EMPLOYED group consistently outperforms others.  
        - Visual comparison is easier than analyzing numbers alone.
        """)
    else:
        st.warning("Please select at least one social skill to display.")

# ===============================
# 5️⃣ Community Participation Histogram
# ===============================
elif selected_sub == "Community Participation":
    community_vars = ['community_participation', 'community_impact']

    df_hist = filtered_df.melt(
        id_vars='employment_status_label',
        value_vars=community_vars,
        var_name='Community Dimension',
        value_name='Likert Score'
    )
    df_hist = df_hist.dropna()
    df_hist['Likert Score'] = df_hist['Likert Score'].astype(int)
    df_hist['employment_status_label'] = df_hist['employment_status_label'].str.upper()

    color_map = {
        'EMPLOYED': '#440154',
        'STUDENT': '#21918c',
        'UNEMPLOYED': '#fde725'
    }

    fig = px.histogram(
        df_hist,
        x='Likert Score',
        color='employment_status_label',
        facet_col='Community Dimension',
        barmode='overlay',
        nbins=5,
        title='Distribution of Community Participation Scores by Employment Status',
        labels={'Likert Score': 'Likert Scale'},
        color_discrete_map=color_map
    )
    fig.update_layout(
        template='plotly_white',
        bargap=0.2,
        legend_title='Employment Status',
        xaxis_title='Likert Score',
        yaxis_title='Count'
    )
    fig.update_xaxes(dtick=1)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Interpretation:**
    - EMPLOYED respondents have higher upper Likert scores (4–5).  
    - STUDENT responses are more spread out.  
    - UNEMPLOYED respondents lean toward lower/neutral scores.  
    - Histogram reveals distribution differences that averages cannot capture.
    """)

    st.markdown("""
    **Conclusion for Community Participation Histogram:**
    - Shows clear distributional differences in community engagement by employment.  
    - EMPLOYED group is most engaged.  
    - UNEMPLOYED group shows lower participation.  
    - Useful for designing programs targeting lower-engaged groups.
    """)

# ===============================
# 6️⃣ Wellbeing and Life Satisfaction Violin Plot
# ===============================
elif selected_sub == "Wellbeing and Life Satisfaction":
    wellbeing_vars = ['life_satisfaction', 'overall_health', 'wellbeing_belief']
    selected_var = st.selectbox("Select wellbeing indicator:", wellbeing_vars)

    color_map = {
        'EMPLOYED': '#440154',
        'STUDENT': '#21918c',
        'UNEMPLOYED': '#fde725'
    }

    fig = px.violin(
        filtered_df,
        x='employment_status_label',
        y=selected_var,
        color='employment_status_label',
        box=True,
        points='all',
        color_discrete_map=color_map,
        title=f'Distribution of {selected_var.replace("_"," ").title()} by Employment Status'
    )
    st.plotly_chart(fig, width='stretch')

    interpretations = {
        'life_satisfaction': [
            "EMPLOYED participants report higher life satisfaction.",
            "STUDENT group shows moderate satisfaction.",
            "UNEMPLOYED group reports lower satisfaction with more outliers.",
            "Violin plot highlights distribution differences."
        ],
        'overall_health': [
            "EMPLOYED participants report slightly better health.",
            "STUDENT group shows consistent health.",
            "UNEMPLOYED group has more variability with occasional low scores.",
            "Violin plot visualizes spread effectively."
        ],
        'wellbeing_belief': [
            "EMPLOYED participants feel more positive about wellbeing.",
            "STUDENT group shows mixed perceptions.",
            "UNEMPLOYED group reports lower confidence in wellbeing.",
            "Violin plot provides clear view of variability."
        ]
    }

    st.markdown(f"""
    **Interpretation:**
    - <span style='color:{color_map['EMPLOYED']}'>EMPLOYED:</span> {interpretations[selected_var][0]}  
    - <span style='color:{color_map['STUDENT']}'>STUDENT:</span> {interpretations[selected_var][1]}  
    - <span style='color:{color_map['UNEMPLOYED']}'>UNEMPLOYED:</span> {interpretations[selected_var][2]}  
    - {interpretations[selected_var][3]}
    """, unsafe_allow_html=True)

    st.markdown(f"""
    **Conclusion for Wellbeing and Life Satisfaction Violin Plot:**
    - EMPLOYED participants report higher wellbeing and health outcomes.  
    - STUDENT group shows moderate levels with some variability.  
    - UNEMPLOYED participants report lower wellbeing and more outliers.  
    - Violin plot effectively shows distribution, spread, and outliers across employment groups.
    """)
