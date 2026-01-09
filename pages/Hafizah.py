import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ======================================
# PAGE CONFIG
# ======================================
st.set_page_config(page_title="Emotional Resilience Analysis", layout="wide")
st.title("🧠 Emotional Resilience & Personal Development Analysis")

# ======================================
# PROBLEM STATEMENT & OBJECTIVE
# ======================================
st.markdown("### 📝 Problem Statement")
st.info("""
Emotional resilience plays a critical role in how individuals manage stress,
adapt to challenges, regulate emotions, and collaborate with others.
Survey-based data provides a systematic way to examine these psychological
and behavioral attributes across individuals.
""")

st.markdown("### 🎯 Objective")
st.write("""
To investigate the relationship between emotional resilience and personal
development attributes, including motivation, adaptability, emotional control,
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
    'calm_under_pressure',
    'emotional_control',
    'adaptability',
    'self_motivation',
    'task_persistence',
    'teamwork'
]

df[attributes] = df[attributes].apply(pd.to_numeric, errors="coerce").fillna(df[attributes].median())

# ======================================
# DATASET OVERVIEW
# ======================================
st.markdown("### 📊 Dataset Overview")
st.info(f"""
• **Dataset:** Hafizah_SSES_Cleaned.csv  
• **Total Responses:** {df.shape[0]}  
• **Total Variables:** {df.shape[1]}  
• **Scale:** 5-point Likert Scale  
• **Focus:** Emotional resilience & personal development
""")

with st.expander("🔍 Dataset Preview"):
    st.dataframe(df[attributes].head(10), use_container_width=True)

# ======================================
# KEY METRICS
# ======================================
st.markdown("### 📈 Key Dataset Metrics")
col1, col2, col3, col4 = st.columns(4)
mean_score = df[attributes].mean().mean()
strongest = df[attributes].mean().idxmax().replace("_"," ").title()
weakest = df[attributes].mean().idxmin().replace("_"," ").title()
std_dev = df[attributes].stack().std()

col1.metric("Overall Mean", f"{mean_score:.2f}")
col2.metric("Strongest Attribute", strongest)
col3.metric("Weakest Attribute", weakest)
col4.metric("Overall Variability (SD)", f"{std_dev:.2f}")

st.markdown("---")

# ======================================
# 1. LIKERT DISTRIBUTION
# ======================================
st.subheader("1️⃣ Likert-Scale Distribution")

st.markdown("**Purpose:** To examine how respondents distribute their agreement levels across emotional resilience attributes.")

likert_dist = df[attributes].apply(lambda x: x.value_counts(normalize=True)).T.reindex(columns=[1,2,3,4,5], fill_value=0)

fig1 = px.bar(likert_dist, barmode="stack",
              labels={"value":"Proportion","index":"Attribute"},
              title="Distribution of Emotional Resilience Attributes")
st.plotly_chart(fig1, use_container_width=True)

st.success("""
**Interpretation:**  
Most attributes show higher proportions of agreement (Likert 4–5),
indicating generally positive emotional resilience among respondents.
""")

# ======================================
# 2. RADAR CHART
# ======================================
st.subheader("2️⃣ Average Emotional Resilience Profile")

st.markdown("**Purpose:** To compare multiple resilience attributes simultaneously using average scores.")

means = df[attributes].mean()
fig2 = go.Figure(go.Scatterpolar(
    r=means.tolist() + [means[0]],
    theta=[a.replace("_"," ").title() for a in attributes] + [attributes[0].replace("_"," ").title()],
    fill="toself"
))
fig2.update_layout(polar=dict(radialaxis=dict(range=[0,5])), showlegend=False)
st.plotly_chart(fig2, use_container_width=True)

st.success(f"""
**Interpretation:**  
Respondents demonstrate strongest resilience in **{means.idxmax().replace('_',' ').title()}**,
while **{means.idxmin().replace('_',' ').title()}** shows comparatively lower strength.
""")

# ======================================
# 3. CORRELATION HEATMAP
# ======================================
st.subheader("3️⃣ Correlation Between Attributes")

st.markdown("**Purpose:** To identify relationships and interdependencies among resilience attributes.")

corr = df[attributes].corr()
fig3 = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r",
                 title="Correlation Matrix")
st.plotly_chart(fig3, use_container_width=True)

st.success("""
**Interpretation:**  
Strong positive correlations suggest that improvements in one attribute
(e.g., emotional control) may positively influence other personal development skills.
""")

# ======================================
# 4. DISTRIBUTION & VARIABILITY (BOXPLOT)
# ======================================
st.subheader("4️⃣ Distribution & Variability")

st.markdown("**Purpose:** To analyze score spread, consistency, and potential variability among respondents.")

melted = df.melt(value_vars=attributes, var_name="Attribute", value_name="Score")
fig4 = px.box(melted, x="Attribute", y="Score", color="Attribute")
st.plotly_chart(fig4, use_container_width=True)

st.success("""
**Interpretation:**  
Attributes with wider interquartile ranges exhibit greater variability,
indicating unequal resilience development across individuals.
""")

# ======================================
# 5. SENTIMENT ANALYSIS (DIVERGING BAR)
# ======================================
st.subheader("5️⃣ Sentiment Analysis (Agreement vs Disagreement)")

st.markdown("**Purpose:** To clearly separate agreement, neutrality, and disagreement in Likert-scale responses.")

def sentiment(col):
    counts = col.value_counts(normalize=True).reindex([1,2,3,4,5], fill_value=0)
    return pd.Series({
        "Disagree": -(counts[1]+counts[2])*100,
        "Neutral": counts[3]*100,
        "Agree": (counts[4]+counts[5])*100
    })

sent_df = df[attributes].apply(sentiment).T.reset_index().rename(columns={"index":"Attribute"})
fig5 = px.bar(sent_df, x=["Disagree","Neutral","Agree"], y="Attribute",
              orientation="h", barmode="relative",
              title="Diverging Likert Sentiment")
st.plotly_chart(fig5, use_container_width=True)

st.success("""
**Interpretation:**  
Most attributes display stronger agreement than disagreement,
confirming overall positive emotional resilience perceptions.
""")

# ======================================
# 6. TREEMAP (ATTRIBUTE HIERARCHY)
# ======================================
st.subheader("6️⃣ Attribute Importance Hierarchy")

st.markdown("**Purpose:** To rank attributes based on their relative average importance.")

tree_df = pd.DataFrame({
    "Attribute":[a.replace("_"," ").title() for a in attributes],
    "Mean Score":means.values
})

fig6 = px.treemap(tree_df, path=["Attribute"], values="Mean Score",
                  color="Mean Score", color_continuous_scale="Blues")
st.plotly_chart(fig6, use_container_width=True)

st.success("""
**Interpretation:**  
Larger and darker areas represent dominant strengths, enabling easy identification
of priority areas for intervention or development.
""")

# ======================================
# CONCLUSION
# ======================================
st.markdown("---")
st.subheader("🏁 Conclusion")

st.success(f"""
The analysis reveals that respondents generally demonstrate strong emotional resilience,
particularly in **{strongest}**. However, **{weakest}** remains an area that could benefit
from targeted development initiatives.

Correlation patterns further suggest that emotional regulation skills act as a foundational
factor influencing multiple personal development attributes.
""")
