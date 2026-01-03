# adawiyah's page
import streamlit as st
import pandas as pd
import plotly.express as px


# Page Configuration
st.set_page_config(page_title="Social & Emotional Impact Analysis", layout="wide")

# Main Title Section
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #2C3E50; /* Deep charcoal for a neat look */
        padding-top: 10px;
        padding-bottom: 20px;
        font-weight: 700;
    }
    </style>
    <h1 class="main-title">✦ Social & Emotional Impact Analysis</h1>
""", unsafe_allow_html=True)

st.markdown("---")

# Custom CSS for Soft Pink Boxes 
st.markdown("""
    <style>
    .pink-box {
        background-color: #FFF0F5; /* Soft Lavender Blush/Pink */
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #FFB6C1; /* Accent Pink border */
        margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .pink-box h4 {
        color: #D02090; /* Darker pink for the header */
        margin-top: 0;
    }
    .pink-box p {
        color: #333333;
        font-size: 16px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# Interactive Section 
# Expander
with st.expander("View Research Objective", expanded=True):
    
    # Objective Box
    st.markdown(f"""
        <div class="pink-box">
            <h4>Objective Statement</h4>
            <p>To analyze how <b>social support</b> from family and friends, along with a <b>safe community environment</b>, 
            influences an individual's ability to manage their emotions and how these factors collectively impact 
            their overall <b>life satisfaction</b>.</p>
        </div>
    """, unsafe_allow_html=True)

    

st.markdown("---")

# 1. Initialize df as an empty DataFrame at the very start
# This ensures line 69 always knows what 'df' is!
df = pd.DataFrame() 

csv_url = "https://raw.githubusercontent.com/nhusna01/SSES-survey-dashboard/refs/heads/main/dataset/Adawiyah_SSES_cleaned.csv"

@st.cache_data  
def fetch_data(url):
    data = pd.read_csv(url)
    # ... (your indexing logic here) ...
    return data

# 2. Attempt to fill 'df' with real data
with st.spinner("✦ Accessing Research Data..."):
    try:
        df = fetch_data(csv_url)
    except Exception as e:
        st.error(f"Connection Error: {e}")
        # df is already an empty DataFrame from line 1, so no NameError will happen

# INTERACTIVE EXPLORATION SECTION 
if not df.empty:
    # Header and Methodology button
    head_col, method_col = st.columns([3, 1])
    
    with head_col:
        st.markdown("### Data Exploration")
    
    with method_col:
        with st.popover("View Methodology"):
            st.markdown("#### Indexing Logic")
            st.write("To improve analysis, raw variables were grouped into indices:")
            st.markdown("""
            - **Social Support Index:** `social_support`, `social_time`, `community_care`
            - **Emotion Management:** `calm_under_pressure`, `emotional_control`
            - **Community Safety:** `neighborhood_safety`, `community_care`
            """)
            st.caption("Calculation: Arithmetic Mean of grouped variables.")

    # Using an expander for the actual data table
    with st.expander("Preview & Filter Raw Dataset", expanded=False):
        
        # DATASET DESCRIPTION BOX  ---
        st.markdown("""
            <div style="background-color: #FFF0F5; padding: 15px; border-radius: 10px; border-left: 5px solid #FFB6C1; margin-bottom: 20px;">
                <p style="margin: 0; color: #333; font-size: 15px;">
                    <b>About this Dataset:</b> This cleaned dataset contains survey responses that focused on 
                    social-emotional well-being. It captures how individuals perceive their <b>social networks</b>, 
                    <b>environmental safety</b>, and their internal ability to <b>manage emotions</b>. The data has been 
                    cleaned to ensure statistical accuracy.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Search bar
        search_query = st.text_input("🔍 Search data by any value:", placeholder="Search by score, category, or ID...")
        
        # Apply search filter
        if search_query:
            df_display = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
            st.write(f"Showing {len(df_display)} matching results:")
        else:
            df_display = df.head(10)
            st.caption("Showing first 10 rows. Use the search bar above to filter.")

        # Display the table
        st.dataframe(df_display, use_container_width=True)

st.markdown("---")

# INTERACTIVE METRICS SECTION 

if not df.empty:
    # 1. Sidebar Interactivity: Filtering the Data
    st.sidebar.header("Filters")
    st.sidebar.write("Adjust the range to update key metrics below.")
    
    # Example: Filtering by Overall Health Score to see how it impacts other metrics
    if 'overall_health' in df.columns:
        min_health = float(df['overall_health'].min())
        max_health = float(df['overall_health'].max())
        
        health_range = st.sidebar.slider(
            "Filter by Overall Health Score",
            min_health, max_health, (min_health, max_health)
        )
        
        # Apply the filter to the dataframe
        df_filtered = df[(df['overall_health'] >= health_range[0]) & (df['overall_health'] <= health_range[1])]
    else:
        df_filtered = df

    st.subheader("Key Performance Indicators")

    # 2. Layout: Summary Metrics in clean columns
    col1, col2, col3, col4 = st.columns(4)

    # Calculations based on FILTERED data
    avg_life_sat = df_filtered['life_satisfaction'].mean() if 'life_satisfaction' in df_filtered else 0
    avg_social = df_filtered['social_support_index'].mean() if 'social_support_index' in df_filtered else 0
    avg_safety = df_filtered['community_safety_index'].mean() if 'community_safety_index' in df_filtered else 0
    avg_emotion = df_filtered['emotion_management_index'].mean() if 'emotion_management_index' in df_filtered else 0

    # Custom CSS to make the metric boxes even neater
    st.markdown("""
        <style>
        [data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #e6e6e6;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: transform 0.2s ease-in-out;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            border-color: #FFB6C1; /* Soft pink border on hover */
        }
        </style>
    """, unsafe_allow_html=True)

    # 3. Displaying Metrics with Black & White Icons
    col1.metric(
        label="✦ Avg. Life Satisfaction", 
        value=f"{avg_life_sat:.2f}",
        help="Overall fulfillment score", 
        border=True
    )
    
    col2.metric(
        label="⚭ Social Support", 
        value=f"{avg_social:.2f}",
        help="Strength of family & friend networks", 
        border=True
    )
    
    col3.metric(
        label="◈ Community Safety", 
        value=f"{avg_safety:.2f}",
        help="Environmental safety perception", 
        border=True
    )
    
    col4.metric(
        label="◉ Emotion Management", 
        value=f"{avg_emotion:.2f}",
        help="Internal ability to manage stress", 
        border=True
    )

st.markdown("---")

# VISUALIZATION 1: CORRELATION HEATMAP 

st.markdown("### Variable Relationship Analysis")

# 1. Interactive Feature: User selects which variables to correlate
st.write("Customize the heatmap by adding or removing variables:")
default_cols = ['life_satisfaction', 'social_support_index', 'community_safety_index', 'emotion_management_index', 'overall_health']
selected_cols = st.multiselect("Select variables for correlation:", 
                               options=df.columns.tolist(), 
                               default=[col for col in default_cols if col in df.columns])

# 2. Check if enough columns are selected
if len(selected_cols) > 1:
    # Calculate Correlation
    corr_matrix = df[selected_cols].corr()

    # 3. Create the Heatmap (Plotly)
    fig1 = px.imshow(
        corr_matrix, 
        text_auto=".2f", 
        color_continuous_scale='RdBu_r', # Red-Blue scale (Scientific standard)
        aspect="auto",
        labels=dict(color="Correlation Strength"),
        zmin=-1, zmax=1 # Ensures the scale is always -1 to 1
    )

    fig1.update_layout(
        title="<b>Correlation Matrix: Interplay of Social & Emotional Factors</b>",
        title_x=0.5,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )

    # 4. Interactive Help Popover
    col_v1, col_v2 = st.columns([3, 1])
    with col_v2:
        with st.popover("How to read this heatmap?"):
            st.markdown("""
                **What do the numbers mean?**
                - **+1.00 (Dark Blue):** Perfect positive relationship (as one goes up, the other goes up).
                - **0.00 (White):** No relationship at all.
                - **-1.00 (Dark Red):** Perfect negative relationship (as one goes up, the other goes down).
                
                *Look for the darkest blue squares to find the strongest drivers of life satisfaction.*
            """)

    # Display Chart
    st.plotly_chart(fig1, use_container_width=True)

    # 5. Scientific Insight Box (Neat & Interactive)
    st.info("""
        **✦ Key Observation:** Strong correlations (values above 0.50) between **Social Support** and **Life Satisfaction** suggest that personal networks may be a primary driver of well-being in this dataset.
    """)

else:
    st.warning("Please select at least two variables to generate the correlation heatmap.")

st.markdown("---")

