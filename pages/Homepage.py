import streamlit as st
import plotly.express as px

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

<img class="top-right-logo" src="https://img.icons8.com/color/64/000000/brain.png">
""", unsafe_allow_html=True)


# ===============================
# 📌 Dashboard Overview (Interactive Summary)
# ===============================

st.subheader("📌 Dashboard Overview")

st.markdown(
    """
    <style>
    .summary-container {
        border: 2px solid #6a5acd;
        border-radius: 16px;
        padding: 1.5rem;
        background-color: #ffffff;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }
    .summary-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
    }
    .summary-card {
        border: 1px solid #ddd;
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
        transition: all 0.2s ease-in-out;
    }
    .summary-card:hover {
        border-color: #6a5acd;
        box-shadow: 0 6px 16px rgba(106,90,205,0.25);
        transform: translateY(-3px);
    }
    .summary-icon {
        font-size: 34px;
        margin-bottom: 0.5rem;
    }
    .summary-value {
        font-size: 36px;
        font-weight: 700;
        color: #2c2c54;
    }
    .summary-label {
        font-size: 15px;
        color: #555;
        margin-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Container ---
st.markdown(
    f"""
    <div class="summary-container">
        <div class="summary-grid">
            <div class="summary-card">
                <div class="summary-icon">📋</div>
                <div class="summary-value">{len(df)}</div>
                <div class="summary-label">Total Responses</div>
            </div>
            <div class="summary-card">
                <div class="summary-icon">🧩</div>
                <div class="summary-value">{df.shape[1]}</div>
                <div class="summary-label">Total Variables</div>
            </div>
            <div class="summary-card">
                <div class="summary-icon">⚠️</div>
                <div class="summary-value">{df.isna().sum().sum()}</div>
                <div class="summary-label">Missing Values</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ===============================
# 🔗 Streamlit Interactive Section
# ===============================
st.markdown("## 📊 Interactive Data Tools")
st.markdown("---")

col1, col2, col3 = st.columns(3)

# ------------------------------
# 1️⃣ View Responses
# ------------------------------
with col1:
    if st.button("📋 View Responses"):
        st.info("Choose which dataset to preview:")

        dataset_option = st.selectbox(
            "Select Dataset:",
            options=["Cleaned Dataset", "Raw Dataset"]
        )

        if dataset_option == "Cleaned Dataset":
            cleaned_path = "data/cleaned_data.csv"
            if os.path.exists(cleaned_path):
                df_cleaned = pd.read_csv(cleaned_path)
                st.dataframe(df_cleaned, use_container_width=True, height=400)
            else:
                st.warning(f"Cleaned dataset not found at {cleaned_path}")

        else:  # Raw Dataset
            raw_path = "https://raw.githubusercontent.com/nhusna01/SSES-survey-dashboard/refs/heads/main/dataset/cleaned_group_survey_data.csv"
            if os.path.exists(raw_path):
                df_raw = pd.read_csv(raw_path)
                st.dataframe(df_raw, use_container_width=True, height=400)
            else:
                st.warning(f"Raw dataset not found at {raw_path}")

# ------------------------------
# 2️⃣ Explore Variables
# ------------------------------
with col2:
    if st.button("🧩 Explore Variables"):
        st.info("Interactive variable table")
        if "df" in st.session_state:
            # Show variable names in a dataframe to make it interactive
            var_df = pd.DataFrame({"Variable Name": st.session_state.df.columns})
            st.dataframe(var_df, use_container_width=True, height=400)
        else:
            st.warning("Dataset not loaded yet!")

# ------------------------------
# 3️⃣ Inspect Missing Values
# ------------------------------
with col3:
    if st.button("⚠️ Inspect Missing Data"):
        st.info("Missing values in the cleaned dataset")
        cleaned_path = "data/cleaned_data.csv"
        if os.path.exists(cleaned_path):
            df_cleaned = pd.read_csv(cleaned_path)
            missing_df = df_cleaned.isna().sum().reset_index()
            missing_df.columns = ["Variable", "Missing Values"]
            # Show only variables with missing values > 0
            missing_df = missing_df[missing_df["Missing Values"] > 0]
            if missing_df.empty:
                st.success("No missing values found in cleaned dataset!")
            else:
                st.dataframe(missing_df, use_container_width=True, height=400)
        else:
            st.warning(f"Cleaned dataset not found at {cleaned_path}")





with st.expander("🔍 View Dataset Preview"):
    st.dataframe(df, use_container_width=True)
    
with st.expander("📈 View Summary Statistics"):
    st.write(df.describe(include="all"))

# Demographics
st.subheader("👥 Demographic Analysis")
demo_col = st.selectbox(
    "Select Demographic Variable to Visualize",
    options=['gender', 'age', 'location', 'education_level'] if 'gender' in df.columns else df.columns
)
col1, col2 = st.columns([2, 1])
with col1:
    fig = px.pie(df, names=demo_col, hole=0.4,
                title=f"Distribution of {demo_col.replace('_',' ').title()}",
                color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.dataframe(df[demo_col].value_counts(), use_container_width=True)



    
