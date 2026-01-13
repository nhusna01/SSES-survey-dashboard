import streamlit as st
import plotly.express as px
import pandas as pd
import os

# Check if data exists in session state before proceeding
if "df" not in st.session_state:
    st.error("Data not found! Please ensure the data is loaded in the main app.")
    st.stop() 

df = st.session_state.df


# Header + logo
st.markdown("""
<style>
.center-title { text-align: center; }
.top-right-logo { position: absolute; top: 10px; right: 20px; height: 60px; }
</style>

<div class="center-title">
    <h1 style="color:#4B0082; font-size:48px; font-weight:bold;">
        🏠 SSES Survey Dashboard
    </h1>
    <p style="color:#555; font-size:20px;">
        Interactive dashboard for Emotional Resilience & Personal Development
    </p>
</div>
<img class="top-right-logo" src="https://img.icons8.com/color/64/feelings.png">
""",
<img class="top-right-logo" src="https://img.icons8.com/color/64/emotional-intelligence.png">
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ===== Animated Gradient Divider ===== */
.animated-divider {
    width: 100%;
    height: 5px;
    border-radius: 8px;
    margin: 1.8rem 0 2.4rem 0;
    background: linear-gradient(
        90deg,
        #6366F1,
        #22C55E,
        #F97316,
        #EC4899,
        #6366F1
    );
    background-size: 400% 100%;
    animation: dividerFlow 5s linear infinite;
}

/* Animation */
@keyframes dividerFlow {
    0% { background-position: 0% 50%; }
    100% { background-position: 400% 50%; }
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="animated-divider"></div>', unsafe_allow_html=True)


# ------------------------------
# 🔗 Dataset Selector (Cleaned / Raw)
# ------------------------------
st.markdown("## 📋 Select Dataset to Work With")
dataset_option = st.selectbox(
    "Choose dataset:",
    options=["Cleaned Dataset", "Raw Dataset"]
)

if dataset_option == "Cleaned Dataset":
    # Cleaned dataset from GitHub raw URL
    cleaned_url = "https://raw.githubusercontent.com/nhusna01/SSES-survey-dashboard/refs/heads/main/dataset/cleaned_group_survey_data.csv"
    try:
        df_current = pd.read_csv(cleaned_url)
    except Exception as e:
        st.error(f"Error loading cleaned dataset from GitHub: {e}")
        st.stop()
else:
    # Raw dataset from Google Sheet URL
    GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1_7nl2F8Vfd90h8ce2TreDW5D_m3WHr6vEFtg10xz3BI/export?format=csv&gid=1821075619"
    try:
        df_current = pd.read_csv(GOOGLE_SHEET_URL)
    except Exception as e:
        st.error(f"Error loading raw dataset from Google Sheet: {e}")
        st.stop()


# ------------------------------
# 📌 Dashboard Overview (Summary Boxes)
# ------------------------------
st.markdown("---")
st.subheader("📌 Dashboard Overview")

st.markdown(
    f"""
    <div style="display: flex; gap: 1rem;">
        <div style="border: 1px solid #ddd; border-radius: 10px; padding: 1rem; flex:1; text-align:center;">
            <h3>📋 Total Responses</h3>
            <p style="font-size:24px; font-weight:bold;">{len(df_current)}</p>
        </div>
        <div style="border: 1px solid #ddd; border-radius: 10px; padding: 1rem; flex:1; text-align:center;">
            <h3>🧩 Total Variables</h3>
            <p style="font-size:24px; font-weight:bold;">{df_current.shape[1]}</p>
        </div>
        <div style="border: 1px solid #ddd; border-radius: 10px; padding: 1rem; flex:1; text-align:center;">
            <h3>⚠️ Missing Values</h3>
            <p style="font-size:24px; font-weight:bold;">{df_current.isna().sum().sum()}</p>
        </div>
    </div>
    """, unsafe_allow_html=True
)

# ------------------------------
# ⚠️ Inspect Missing Values Table
# ------------------------------
st.markdown("---")
st.subheader("⚠️ Inspect Missing Values")
missing_df = df_current.isna().sum().reset_index()
missing_df.columns = ["Variable", "Missing Values"]
missing_df = missing_df[missing_df["Missing Values"] > 0]

if missing_df.empty:
    st.success("No missing values found in this dataset!")
else:
    st.dataframe(missing_df, use_container_width=True, height=300)

# ------------------------------
# 🔍 View Dataset Preview
# ------------------------------
st.markdown("---")
st.subheader("🔍 View Dataset Preview")
with st.expander("Click to expand dataset preview"):
    st.dataframe(df_current, use_container_width=True, height=400)

# ------------------------------
# 🧩 View Variables Available 
# ------------------------------
st.markdown("---")
st.subheader("🧩 View Variables Available")

with st.expander("Click to expand and view all variables"):
    # Create a DataFrame of variable names only
    var_df = pd.DataFrame({"Variable Name": df_current.columns})
    st.dataframe(var_df, use_container_width=True, height=300)


# ------------------------------
# 📈 View Summary Statistics
# ------------------------------
st.markdown("---")
st.subheader("📈 View Summary Statistics")

# Select only numeric columns
numeric_cols = df_current.select_dtypes(include=['int64', 'float64']).columns

if len(numeric_cols) == 0:
    st.warning("No numeric columns available in this dataset.")
else:
    with st.expander("Click to expand summary statistics (numeric variables only)"):
        st.write(df_current[numeric_cols].describe().transpose())


# ------------------------------
# 👥 Demographic Analysis
# ------------------------------
st.markdown("---")
st.subheader("👥 Demographic Analysis")

demo_options = ['gender', 'age', 'location', 'education_level']
demo_options = [col for col in demo_options if col in df_current.columns]

demo_col = st.selectbox(
    "Select Demographic Variable to Visualize",
    options=demo_options if demo_options else df_current.columns
)

col1, col2 = st.columns([2,1])

with col1:
    fig = px.pie(df_current, names=demo_col, hole=0.4,
                 title=f"Distribution of {demo_col.replace('_',' ').title()}",
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.dataframe(df_current[demo_col].value_counts(), use_container_width=True)
