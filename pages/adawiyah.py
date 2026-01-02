import streamlit as st
import plotly.express as px
from sklearn.cluster import KMeans
from preprocess import load_data

st.title("🤖 Respondent Segmentation")
st.markdown("Using K-Means clustering to group similar respondents based on their scores.")

df = load_data()
numeric_df = df.select_dtypes(include=["int64", "float64"]).dropna()

if numeric_df.shape[1] < 2:
    st.error("Not enough numeric data for clustering.")
else:
    k = st.sidebar.slider("Number of Clusters (k)", 2, 6, 3)
    
    # ML Logic
    kmeans = KMeans(n_clusters=k, random_state=42)
    df["Cluster"] = kmeans.fit_predict(numeric_df)
    
    # Visualization
    col_x = st.selectbox("X-Axis Feature", options=numeric_df.columns, index=0)
    col_y = st.selectbox("Y-Axis Feature", options=numeric_df.columns, index=1)
    
    fig = px.scatter(
        df, x=col_x, y=col_y, color=df["Cluster"].astype(str),
        title=f"Clusters based on {col_x} and {col_y}",
        labels={"color": "Cluster Group"}
    )
    st.plotly_chart(fig, use_container_width=True)
