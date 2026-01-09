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
# PROBLEM STATEMENT & OBJECTIVE
# ======================================
st.markdown("### 📝 Problem Statement")
st.info("""
Emotional resilience influences how individuals manage stress, regulate emotions,
adapt to change, and collaborate with others. Understanding these attributes through
survey-based data enables systematic analysis of personal development patterns.
""")

st.markdown("### 🎯 Objective")
st.write("""
To investigate the relationship between emotional resilience and personal development
attributes, including motivation, adaptability, emotional control, task persistence,
and teamwork skills.
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
# DATASET OVERVIEW
# ======================================
st.markdown("### 📊 Dataset Overview")
st.info(f"""
• **Dataset Name:** Hafizah_SSES_Cleaned.csv  
• **Total Respondents:** {df.shape[0]}  
• **Total Variables:** {df.shape[1]}  
• **Measurement Scale:** 5-point Likert scale  
• **Focus Area:** Emotional resilience & personal development
""")

with st.expander("🔍 Dataset Preview"):
    st.dataframe(df[attributes].head(10), use_container_width=True)

# ======================================
# KEY DATASET METRICS
# ======================================
st.markdown("### 📈 Key Dataset Metrics")

col1, col2, col3, col4 = st.columns(4)
overall_mean = df[attributes].mean().mean()
strongest_attr = df[attributes].mean().idxmax().replace("_", " ").title()
weakest_attr = df[attributes].mean().idxmin().replace("_", " ").title()
overall_sd = df[attributes].stack().std()

col1.metric("Overall Mean Score", f"{overall_mean:.2f}")
col2.metric("Strongest Attribute", strongest_attr)
col3.metric("Weakest Attribute", weakest_attr)
col4.metric("Overall Variability (SD)", f"{overall_sd:.2f}")

st.markdown("---")

# ======================================
# 1️⃣ LIKERT DISTRIBUTION
# ======================================
st.subheader("1️⃣ Likert-Scale Distribution of Attributes")
st.markdown("**Purpose:** To examine response patterns across agreement levels.")

likert_dist = df[attributes].apply(lambda x: x.value_counts(normalize=True)).T
likert_dist = likert_dist.reindex(columns=[1,2,3,4,5], fill_value=0)

fig1 = px.bar(
    likert_dist,
    barmode="stack",
    labels={"value": "Proportion", "index": "Attribute"},
    title="Distribution of Emotional Resilience Attributes"
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown("### 📋 Key Findings: Likert Distribution")
st.dataframe((likert_dist * 100).round(2), use_container_width=True)

st.success("""
Most respondents selected higher agreement levels (4–5),
indicating generally positive emotional resilience across attributes.
""")

# ======================================
# 2️⃣ RADAR CHART
# ======================================
st.subheader("2️⃣ Average Emotional Resilience Profile")
st.markdown("**Purpose:** To compare average strength of multiple attributes simultaneously.")

mean_scores = df[attributes].mean()

fig2 = go.Figure(go.Scatterpolar(
    r=mean_scores.tolist() + [mean_scores[0]],
    theta=[a.replace("_"," ").title() for a in attributes] +
          [attributes[0].replace("_"," ").title()],
    fill="toself"
))
fig2.update_layout(
    polar=dict(radialaxis=dict(range=[0,5])),
    showlegend=False
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 📋 Key Findings: Descriptive Statistics")
desc_table = pd.DataFrame({
    "Attribute": [a.replace("_"," ").title() for a in attributes],
    "Mean": mean_scores.round(2).values,
    "Std Dev": df[attributes].std().round(2).values,
    "Min": df[attributes].min().values,
    "Max": df[attributes].max().values
}).sort_values(by="Mean", ascending=False)

st.dataframe(desc_table, use_container_width=True)

# ======================================
# 3️⃣ CORRELATION HEATMAP
# ======================================
st.subheader("3️⃣ Correlation Between Attributes")
st.markdown("**Purpose:** To identify relationships among emotional resilience attributes.")

corr = df[attributes].corr()
fig3 = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    title="Correlation Matrix"
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("### 📋 Key Findings: Strongest Correlations")
corr_pairs = (
    corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
        .stack()
        .reset_index()
)
corr_pairs.columns = ["Attribute 1", "Attribute 2", "Correlation"]
corr_pairs["Attribute 1"] = corr_pairs["Attribute 1"].str.replace("_"," ").str.title()
corr_pairs["Attribute 2"] = corr_pairs["Attribute 2"].str.replace("_"," ").str.title()

st.table(corr_pairs.sort_values(by="Correlation", ascending=False).head(5))

# ======================================
# 4️⃣ VARIABILITY (BOXPLOT)
# ======================================
st.subheader("4️⃣ Distribution & Variability Analysis")
st.markdown("**Purpose:** To examine score spread and consistency across respondents.")

melted = df.melt(value_vars=attributes, var_name="Attribute", value_name="Score")
fig4 = px.box(melted, x="Attribute", y="Score", color="Attribute")
st.plotly_chart(fig4, use_container_width=True)

st.markdown("### 📋 Key Findings: Variability Summary")
variability_table = pd.DataFrame({
    "Attribute": [a.replace("_"," ").title() for a in attributes],
    "IQR": (df[attributes].quantile(0.75) - df[attributes].quantile(0.25)).round(2).values,
    "Std Dev": df[attributes].std().round(2).values
})
st.dataframe(variability_table, use_container_width=True)

# ======================================
# 5️⃣ SENTIMENT ANALYSIS
# ======================================
st.subheader("5️⃣ Sentiment Analysis (Agreement vs Disagreement)")
st.markdown("**Purpose:** To separate agreement, neutrality, and disagreement clearly.")

def sentiment(col):
    counts = col.value_counts(normalize=True).reindex([1,2,3,4,5], fill_value=0)
    return pd.Series({
        "Disagree (%)": -(counts[1] + counts[2]) * 100,
        "Neutral (%)": counts[3] * 100,
        "Agree (%)": (counts[4] + counts[5]) * 100
    })

sentiment_df = df[attributes].apply(sentiment).T.reset_index()
sentiment_df.rename(columns={"index":"Attribute"}, inplace=True)
sentiment_df["Attribute"] = sentiment_df["Attribute"].str.replace("_"," ").str.title()

fig5 = px.bar(
    sentiment_df,
    x=["Disagree (%)","Neutral (%)","Agree (%)"],
    y="Attribute",
    orientation="h",
    barmode="relative",
    title="Diverging Likert Sentiment"
)
st.plotly_chart(fig5, use_container_width=True)

st.markdown("### 📋 Key Findings: Sentiment Breakdown")
st.dataframe(sentiment_df.round(2), use_container_width=True)

# ======================================
# 6️⃣ ATTRIBUTE PRIORITY (TREEMAP)
# ======================================
st.subheader("6️⃣ Attribute Priority Ranking")
st.markdown("**Purpose:** To rank attributes based on relative strength.")

priority_df = pd.DataFrame({
    "Attribute": [a.replace("_"," ").title() for a in attributes],
    "Mean Score": mean_scores.round(2).values
}).sort_values(by="Mean Score", ascending=False)

fig6 = px.treemap(
    priority_df,
    path=["Attribute"],
    values="Mean Score",
    color="Mean Score",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig6, use_container_width=True)

st.markdown("### 📋 Key Findings: Attribute Ranking")
priority_df.index += 1
st.table(priority_df.rename_axis("Rank"))

# ======================================
# CONCLUSION
# ======================================
st.markdown("---")
st.subheader("🏁 Conclusion")

st.success(f"""
The findings indicate that respondents generally demonstrate strong emotional
resilience, particularly in **{strongest_attr}**. However, **{weakest_attr}**
represents an area requiring targeted development.

Correlation analysis suggests emotional regulation plays a foundational role,
influencing adaptability, motivation, and teamwork skills.
""")
