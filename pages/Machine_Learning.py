import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans
from preprocess import load_data

st.set_page_config(
    page_title="Machine Learning Analysis",
    layout="wide"
)

df = load_data()

st.title("Respondent Segmentation (K-Means Clustering)")

st.markdown("""
This analysis groups respondents based on numeric survey responses
to identify similarity patterns using unsupervised learning.
""")

numeric_df = df.select_dtypes(include=["int64", "float64"])

if numeric_df.shape[1] < 2:
    st.warning("At least two numeric variables are required for clustering.")
    st.stop()

k = st.slider(
    "Select number of clusters (k)",
    min_value=2,
    max_value=6,
    value=3
)

model = KMeans(n_clusters=k, random_state=42)
clusters = model.fit_predict(numeric_df)

clustered_df = numeric_df.copy()
clustered_df["Cluster"] = clusters

fig = px.scatter(
    clustered_df,
    x=clustered_df.columns[0],
    y=clustered_df.columns[1],
    color="Cluster",
    title="Respondent Clustering Result"
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("View Clustered Data"):
    st.dataframe(clustered_df.head(), use_container_width=True)

