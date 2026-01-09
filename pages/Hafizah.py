import streamlit as st
import pandas as pd
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
Emotional resilience plays a critical role in an individual’s ability to manage stress,
adapt to challenges, regulate emotions, and collaborate effectively with others.
Understanding these attributes through survey-based data allows for evidence-based
insights into personal development and well-being.
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

@st.cache_data(ttl=3600)
def load_data():
    return pd.read_csv(DATA_URL)

df = load_data()

objective3_cols = [
    'calm_under_pressure',
    'emotional_control',
    'adaptability',
    'self_motivation',
    'task_persistence',
    'teamwork'
]

available_cols = [c for c in objective3_cols if c in df.columns]

df[available_cols] = df[available_cols].apply(
    pd.to_numeric, errors="coerce"
).fillna(df[available_cols].median())

# ======================================
# DATASET OVERVIEW
# ======================================
st.markdown("### 📊 Dataset Overview")
st.info(f"""
**Dataset Name:** Hafizah_SSES_Cleaned.csv  
**Total Responses:** {df.shape[0]}  
**Total Variables:** {df.shape[1]}  
**Measurement Scale:** 5-point Likert Scale  
**Focus Area:** Emotional resilience and personal development attributes  
""")

# ======================================
# DATASET PREVIEW
# ======================================
st.markdown("### 🔍 Dataset Preview")
with st.expander("Click to view sample data"):
    st.dataframe(df[available_cols].head(10), use_container_width=True)

# ======================================
# KEY DATASET METRICS
# ======================================
st.markdown("### 📈 Key Dataset Metrics")

col1, col2, col3, col4 = st.columns(4)

overall_mean = df[available_cols].mean().mean()
strongest_attr = df[available_cols].mean().idxmax().replace("_", " ").title()
weakest_attr = df[available_cols].mean().idxmin().replace("_", " ").title()
overall_std = df[available_cols].stack().std()

col1.metric("Average Score", f"{overall_mean:.2f} / 5")
col2.metric("Strongest Attribute", strongest_attr)
col3.metric("Weakest Attribute", weakest_attr)
col4.metric("Overall Variability (SD)", f"{overall_std:.2f}")

st.markdown("---")

# ======================================
# 1. LIKERT DISTRIBUTION (STACKED BAR)
# ======================================
st.subheader("1️⃣ Likert-Scale Distribution")

likert_counts = (
    df[available_cols]
    .apply(lambda x: x.value_counts(normalize=True))
    .T
    .reindex(columns=[1,2,3,4,5], fill_value=0)
)

fig_likert = px.bar(
    likert_counts,
    barmode="stack",
    labels={"value": "Proportion", "index": "Attribute"},
    title="Distribution of Emotional Resilience Attributes"
)
st.plotly_chart(fig_likert, use_container_width=True)

# ======================================
# SUMMARY OVERVIEW
# ======================================
agree_prop = df[available_cols].isin([4,5]).mean()
st.markdown("#### 🧾 Summary Overview")
st.success(f"""
Respondents generally demonstrate **positive emotional resilience**.
The highest agreement is observed for **{agree_prop.idxmax().replace('_',' ').title()}**,
while **{agree_prop.idxmin().replace('_',' ').title()}** shows comparatively lower agreement,
indicating a potential area for personal development.
""")

# ======================================
# 2. RADAR CHART
# ======================================
st.subheader("2️⃣ Average Emotional Resilience Profile")

mean_scores = df[available_cols].mean()

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=mean_scores.tolist() + [mean_scores[0]],
    theta=[c.replace("_"," ").title() for c in available_cols] + 
          [available_cols[0].replace("_"," ").title()],
    fill="toself"
))
fig_radar.update_layout(
    polar=dict(radialaxis=dict(range=[0,5])),
    showlegend=False
)
st.plotly_chart(fig_radar, use_container_width=True)

# ======================================
# 3. CORRELATION HEATMAP
# ======================================
st.subheader("3️⃣ Correlation Between Attributes")

corr = df[available_cols].corr()
fig_corr = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    title="Correlation Matrix"
)
st.plotly_chart(fig_corr, use_container_width=True)

# ======================================
# 4. DISTRIBUTION & VARIABILITY (BOXPLOT)
# ======================================
st.subheader("4️⃣ Distribution & Variability")

melted = df.melt(value_vars=available_cols,
                 var_name="Attribute",
                 value_name="Score")

fig_box = px.box(
    melted,
    x="Attribute",
    y="Score",
    color="Attribute"
)
st.plotly_chart(fig_box, use_container_width=True)

# ======================================
# 5. SENTIMENT ANALYSIS (DIVERGING BAR)
# ======================================
st.subheader("5️⃣ Sentiment Analysis (Agreement vs Disagreement)")

def sentiment(series):
    counts = series.value_counts(normalize=True).reindex([1,2,3,4,5], fill_value=0)
    return pd.Series({
        "Disagree": -(counts[1] + counts[2]) * 100,
        "Neutral": counts[3] * 100,
        "Agree": (counts[4] + counts[5]) * 100
    })

sentiment_df = df[available_cols].apply(sentiment).T.reset_index()
sentiment_df.rename(columns={"index": "Attribute"}, inplace=True)

fig_sent = px.bar(
    sentiment_df,
    x=["Disagree","Neutral","Agree"],
    y="Attribute",
    orientation="h",
    barmode="relative",
    title="Diverging Likert Sentiment"
)
st.plotly_chart(fig_sent, use_container_width=True)

# ======================================
# 6. ATTRIBUTE HIERARCHY (TREEMAP)
# ======================================
st.subheader("6️⃣ Attribute Importance Hierarchy")

tree_df = pd.DataFrame({
    "Attribute": [c.replace("_"," ").title() for c in available_cols],
    "Mean Score": mean_scores.values
})

fig_tree = px.treemap(
    tree_df,
    path=["Attribute"],
    values="Mean Score",
    color="Mean Score",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig_tree, use_container_width=True)

# ======================================
# CONCLUSION
# ======================================
st.markdown("---")
st.subheader("🏁 Conclusion & Recommendations")

st.success(f"""
The analysis indicates that respondents exhibit strong emotional resilience overall,
particularly in **{strongest_attr}**. However, **{weakest_attr}** represents a potential
area for targeted improvement.

Correlation patterns suggest that emotional regulation skills play a foundational role,
implying that strengthening these abilities may positively influence multiple
personal development dimensions simultaneously.
""")
