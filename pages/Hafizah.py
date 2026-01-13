import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ======================================
# PAGE CONFIG
# ======================================
st.set_page_config(
    page_title="Emotional Resilience Analysis",
    layout="wide"
)

st.title("🧠 Emotional Resilience & Personal Development Analysis")

# ======================================
# PROBLEM STATEMENT (INTERACTIVE)
# ======================================
st.markdown("### 📝 Problem Statement")

problem_option = st.selectbox(
    "Select explanation focus:",
    [
        "Why Emotional Resilience Matters",
        "Scientific Relevance of the Problem",
        "Why Survey-Based Data is Suitable"
    ]
)

if problem_option == "Why Emotional Resilience Matters":
    st.info("""
    Emotional resilience plays a critical role in how individuals cope with stress,
    regulate emotions, adapt to challenges, and collaborate effectively with others.
    Understanding resilience-related attributes provides insights into personal
    development and psychological well-being.
    """)

elif problem_option == "Scientific Relevance of the Problem":
    st.info("""
    Emotional resilience is a multidimensional construct involving emotional regulation,
    adaptability, motivation, persistence, and social interaction. Quantitative analysis
    of these dimensions supports scientific understanding of human behavior patterns.
    """)

elif problem_option == "Why Survey-Based Data is Suitable":
    st.info("""
    Survey-based data enables the systematic collection of subjective emotional and
    behavioral attributes that cannot be directly observed. Likert-scale measurements
    allow statistical comparison, correlation analysis, and visualization.
    """)

# ======================================
# OBJECTIVE (INTERACTIVE)
# ======================================
st.markdown("### 🎯 Objective")
st.success("""
The objective of this study is to investigate the relationship between emotional resilience
and personal development attributes, including motivation, adaptability, emotional control,
task persistence, and teamwork skills.
""")

# ======================================
# DATA LOADING
# ======================================
DATA_URL = "https://raw.githubusercontent.com/nhusna01/SSES-survey-dashboard/main/dataset/Hafizah_SSES_Cleaned.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_URL)

df = load_data()

attributes = [
    "calm_under_pressure",
    "emotional_control",
    "adaptability",
    "self_motivation",
    "task_persistence",
    "teamwork"
]

df[attributes] = df[attributes].apply(pd.to_numeric, errors="coerce")
df[attributes] = df[attributes].fillna(df[attributes].median())

# ======================================
# DATASET OVERVIEW (INTERACTIVE)
# ======================================
st.markdown("### 📊 Dataset Overview")

dataset_option = st.selectbox(
    "Select dataset explanation:",
    ["Dataset Description", "Survey Structure", "Measurement Scale"]
)

if dataset_option == "Dataset Description":
    st.info("""
    The dataset consists of self-reported survey responses designed to measure
    emotional resilience and personal development attributes. It captures respondents’
    perceived ability to manage pressure, regulate emotions, adapt to change,
    remain motivated, persist in challenges, and work effectively with others.
    """)

elif dataset_option == "Survey Structure":
    st.info(f"""
    The dataset contains {df.shape[0]} individual responses and {df.shape[1]} variables.
    Each row represents a respondent, while each column corresponds to a specific
    emotional or behavioral attribute.
    """)

elif dataset_option == "Measurement Scale":
    st.info("""
    All attributes were measured using a 5-point Likert scale, allowing respondents
    to indicate levels of agreement. This enables numerical analysis, comparison,
    and visualization of emotional resilience patterns.
    """)

with st.expander("🔍 Dataset Preview"):
    st.dataframe(df[attributes].head(10), use_container_width=True)

# ======================================
# KEY DATASET METRICS (INTERACTIVE)
# ======================================
st.markdown("### 📈 Key Dataset Metrics")

overall_mean = df[attributes].mean().mean()
strongest_attr = df[attributes].mean().idxmax().replace("_", " ").title()
weakest_attr = df[attributes].mean().idxmin().replace("_", " ").title()
overall_sd = df[attributes].stack().std()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Overall Mean Score", f"{overall_mean:.2f}")
col2.metric("Strongest Attribute", strongest_attr)
col3.metric("Weakest Attribute", weakest_attr)
col4.metric("Overall Variability (SD)", f"{overall_sd:.2f}")

metric_option = st.radio(
    "Metric interpretation:",
    ["Overall Trend", "Strength Insight", "Variability Insight"]
)

if metric_option == "Overall Trend":
    st.info("""
    The overall mean score suggests respondents generally demonstrate
    positive emotional resilience across measured attributes.
    """)

elif metric_option == "Strength Insight":
    st.info(f"""
    The highest average score was observed in **{strongest_attr}**,
    indicating this attribute is the most developed among respondents.
    """)

elif metric_option == "Variability Insight":
    st.info("""
    The observed variability reflects differences in individual resilience
    levels, suggesting diverse emotional development profiles.
    """)

st.markdown("---")

# ======================================
# VISUALIZATION 1: LIKERT DISTRIBUTION
# ======================================
st.subheader("1️⃣ Likert-Scale Distribution")

likert_dist = df[attributes].apply(lambda x: x.value_counts(normalize=True)).T
likert_dist = likert_dist.reindex(columns=[1,2,3,4,5], fill_value=0)

fig1 = px.bar(likert_dist, barmode="stack",
              labels={"value":"Proportion","index":"Attribute"})
st.plotly_chart(fig1, use_container_width=True)

viz1 = st.selectbox("Interpretation:", ["Purpose", "Key Findings", "Scientific Interpretation"], key="v1")

if viz1 == "Purpose":
    st.info("This visualization examines response distribution across Likert agreement levels.")
elif viz1 == "Key Findings":
    st.info("Most responses cluster at higher agreement levels, indicating strong resilience.")
else:
    st.info("High agreement dominance suggests positive self-perceived emotional capability.")

# ======================================
# VISUALIZATION 2: RADAR CHART
# ======================================
st.subheader("2️⃣ Average Emotional Resilience Profile")

mean_scores = df[attributes].mean()
fig2 = go.Figure(go.Scatterpolar(
    r=mean_scores.tolist() + [mean_scores[0]],
    theta=[a.replace("_"," ").title() for a in attributes] +
          [attributes[0].replace("_"," ").title()],
    fill="toself"
))
fig2.update_layout(polar=dict(radialaxis=dict(range=[0,5])), showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

viz2 = st.selectbox("Interpretation:", ["Purpose", "Key Findings", "Scientific Interpretation"], key="v2")

if viz2 == "Purpose":
    st.info("This chart compares average strength across multiple attributes simultaneously.")
elif viz2 == "Key Findings":
    st.info(f"{strongest_attr} shows the highest average strength.")
else:
    st.info("Radar profiles reveal balanced but unequal development across resilience traits.")

# ======================================
# VISUALIZATION 3: CORRELATION HEATMAP
# ======================================
st.subheader("3️⃣ Correlation Analysis")

corr = df[attributes].corr()
fig3 = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r")
st.plotly_chart(fig3, use_container_width=True)

viz3 = st.selectbox("Interpretation:", ["Purpose", "Key Findings", "Scientific Interpretation"], key="v3")

if viz3 == "Purpose":
    st.info("This visualization identifies relationships between resilience attributes.")
elif viz3 == "Key Findings":
    st.info("Several attributes exhibit moderate to strong positive correlations.")
else:
    st.info("Emotional regulation appears to influence adaptability and motivation.")

# ======================================
# VISUALIZATION 4: BOXPLOT
# ======================================
st.subheader("4️⃣ Variability & Distribution")

melted = df.melt(value_vars=attributes, var_name="Attribute", value_name="Score")
fig4 = px.box(melted, x="Attribute", y="Score", color="Attribute")
st.plotly_chart(fig4, use_container_width=True)

viz4 = st.selectbox("Interpretation:", ["Purpose", "Key Findings", "Scientific Interpretation"], key="v4")

if viz4 == "Purpose":
    st.info("This plot examines score spread and consistency across respondents.")
elif viz4 == "Key Findings":
    st.info("Some attributes show wider variability than others.")
else:
    st.info("Greater spread indicates differing resilience development levels.")

# ======================================
# VISUALIZATION 5: SENTIMENT ANALYSIS
# ======================================
st.subheader("5️⃣ Sentiment Analysis")

def sentiment(col):
    counts = col.value_counts(normalize=True).reindex([1,2,3,4,5], fill_value=0)
    return pd.Series({
        "Disagree": -(counts[1] + counts[2]) * 100,
        "Neutral": counts[3] * 100,
        "Agree": (counts[4] + counts[5]) * 100
    })

sentiment_df = df[attributes].apply(sentiment).T.reset_index()
sentiment_df.rename(columns={"index":"Attribute"}, inplace=True)
sentiment_df["Attribute"] = sentiment_df["Attribute"].str.replace("_"," ").str.title()

fig5 = px.bar(sentiment_df, x=["Disagree","Neutral","Agree"],
              y="Attribute", orientation="h", barmode="relative")
st.plotly_chart(fig5, use_container_width=True)

viz5 = st.selectbox("Interpretation:", ["Purpose", "Key Findings", "Scientific Interpretation"], key="v5")

if viz5 == "Purpose":
    st.info("This visualization separates agreement, neutrality, and disagreement.")
elif viz5 == "Key Findings":
    st.info("Agreement outweighs disagreement across all attributes.")
else:
    st.info("Positive sentiment dominance suggests strong perceived resilience.")

# ======================================
# VISUALIZATION 6: TREEMAP
# ======================================
st.subheader("6️⃣ Attribute Priority Ranking")

priority_df = pd.DataFrame({
    "Attribute": [a.replace("_"," ").title() for a in attributes],
    "Mean Score": mean_scores.round(2).values
}).sort_values(by="Mean Score", ascending=False)

fig6 = px.treemap(priority_df, path=["Attribute"], values="Mean Score",
                  color="Mean Score", color_continuous_scale="Blues")
st.plotly_chart(fig6, use_container_width=True)

viz6 = st.selectbox("Interpretation:", ["Purpose", "Key Findings", "Scientific Interpretation"], key="v6")

if viz6 == "Purpose":
    st.info("This visualization ranks attributes based on relative strength.")
elif viz6 == "Key Findings":
    st.info(f"{priority_df.iloc[0]['Attribute']} ranks highest among attributes.")
else:
    st.info("Priority ranking highlights areas of strength and development needs.")

# ======================================
# CONCLUSION
# ======================================
st.markdown("---")
st.subheader("🏁 Conclusion")

st.success(f"""
The analysis indicates generally strong emotional resilience among respondents,
with **{strongest_attr}** emerging as the most developed attribute. However,
**{weakest_attr}** represents an area requiring further development.

Overall, emotional regulation appears to play a foundational role,
influencing adaptability, motivation, and teamwork skills.
""")
