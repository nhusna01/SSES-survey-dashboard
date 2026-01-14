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
with st.spinner("Accessing Research Data..."):
    try:
        df = fetch_data(csv_url)
    except Exception as e:
        st.error(f"Connection Error: {e}")
        # df is already an empty DataFrame from line 1, so no NameError will happen

# INTERACTIVE EXPLORATION SECTION 
if not df.empty:
    # 1. Header and Methodology Popover
    head_col, method_col = st.columns([3, 1])
    
    with head_col:
        st.markdown("### Data Exploration")
    
    with method_col:
        # Using a popover for methodology keeps the UI clean
        with st.popover("View Methodology"):
            st.markdown("#### Indexing Logic")
            st.write("To improve analysis, raw variables were grouped into indices:")
            st.markdown("""
            - **Social Support Index:** `social_support`, `social_time`, `community_care`
            - **Emotion Management:** `calm_under_pressure`, `emotional_control`
            - **Community Safety:** `neighborhood_safety`, `community_care`
            """)
            st.caption("Calculation: Arithmetic Mean of grouped variables.")

    # 2. Data Preview Expander - Set to TRUE to be open by default
    with st.expander("🔍 Preview & Filter Raw Dataset", expanded=True):
        
        # DATASET DESCRIPTION BOX
        st.markdown("""
            <div style="background-color: #FFF0F5; padding: 15px; border-radius: 10px; border-left: 5px solid #FFB6C1; margin-bottom: 20px;">
                <p style="margin: 0; color: #333; font-size: 15px;">
                    <b>About this Dataset:</b> This cleaned dataset contains survey responses that focused on 
                    social-emotional well-being. It captures how individuals perceive their <b>social networks</b>, 
                    <b>environmental safety</b>, and their internal ability to <b>manage emotions</b>.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # 3. Search and Filtering Logic
        search_query = st.text_input("Search data by any value:", placeholder="Search by state, education level, or scores...")
        
        # Apply search filter
        if search_query:
            # Filters the dataframe if any column contains the search string
            df_display = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
            st.info(f"Showing {len(df_display)} matching results:")
        else:
            # Default view - showing first 10 rows to keep it clean
            df_display = df.head(10)
            st.caption("Showing first 10 rows. Use the search bar above to filter all records.")

        # 4. Display the table with interactive features
        st.dataframe(
            df_display, 
            use_container_width=True,
            column_config={
                "life_satisfaction": st.column_config.NumberColumn("Satisfaction"),
                "overall_health": st.column_config.NumberColumn("Health")
            }
        )

st.markdown("---")

# INTERACTIVE METRICS SECTION 

if not df.empty:
    # 1. Sidebar Interactivity: Filtering the Data
    st.sidebar.header("Filters")
    st.sidebar.write("Adjust the range to update the key metrics")
    
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

# RESEARCH VISUALIZATIONS (UNIFIED PINK THEME) 

st.markdown("### Research Visualizations")

# VISUALIZATION 1: CORRELATION HEATMAP 
with st.expander("Visualization 1: Correlation Heatmap", expanded=True):
    
    # Ensure indices are defined before plotting
    # (Calculated here just in case they weren't defined earlier in your script)
    if 'social_support_index' not in df.columns:
        df['social_support_index'] = df[['social_support', 'social_time', 'community_care']].mean(axis=1)
    if 'community_safety_index' not in df.columns:
        df['community_safety_index'] = df[['neighborhood_safety', 'community_care']].mean(axis=1)
    if 'emotion_management_index' not in df.columns:
        df['emotion_management_index'] = df[['calm_under_pressure', 'emotional_control']].mean(axis=1)

    viz1_cols = ['life_satisfaction', 'social_support_index', 'community_safety_index', 'emotion_management_index', 'overall_health']
    available_viz_cols = [col for col in viz1_cols if col in df.columns]

    if len(available_viz_cols) > 1:
        corr_matrix = df[available_viz_cols].corr()

        # Create Heatmap
        fig1 = px.imshow(
            corr_matrix, 
            text_auto=".2f", 
            color_continuous_scale='Reds', 
            aspect="auto",
            zmin=0, zmax=1,
            labels=dict(color="Correlation Strength") # This names the color indicator
        )

        # UPDATED: Customizing the color bar to act as the "Guide"
        fig1.update_layout(
            title="<b>Variable Correlation Analysis</b>",
            title_x=0.5,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            coloraxis_colorbar=dict(
                title="Strength",
                tickvals=[0, 0.5, 1],
                ticktext=["Weak (White)", "Medium", "Strong (Red)"], # Directly tells the user what colors mean
                lenmode="pixels", len=300,
            )
        )

        # Simplified layout: Just the chart (No more col_info1 button)
        st.plotly_chart(fig1, use_container_width=True, key="heatmap_1")

        # Interpretation Box
        st.markdown(f"""
            <div style="background-color: #FFF0F5; padding: 15px; border-radius: 10px; border-left: 5px solid #FFB6C1;">
                <p style="margin: 0; color: #333;">
                    <b>Interpretation:</b> Health, emotional control, and social safety are all factors that contribute to life satisfaction. 
                    Safety and support have a strong <b>0.68 correlation</b>, proving that community-level security is a direct foundation for social connection.
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Not enough data to generate correlation heatmap.")

# --- VISUALIZATION 2: SOCIAL & COMMUNITY IMPACT (Simplified) ---
with st.expander("Visualization 2: Social & Community Impact", expanded=False):
    
    # Ensure indices are calculated (if not already done at the top of the script)
    df['social_support_index'] = df[['social_support', 'social_time', 'community_care']].mean(axis=1)
    df['community_safety_index'] = df[['neighborhood_safety', 'community_care']].mean(axis=1)

    # Simplified Scatter Plot
    fig2 = px.scatter(
        df,
        x='social_support_index',
        y='life_satisfaction',
        color='community_safety_index',
        opacity=0.8,
        color_continuous_scale='Reds', 
        labels={
            'social_support_index': 'Support Score', 
            'life_satisfaction': 'Satisfaction', 
            'community_safety_index': 'Safety'
        }
    )

    fig2.update_layout(
        title="<b>Impact of Support & Safety</b>",
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    # Layout: Chart + Guide
    sc_chart_col, sc_guide_col = st.columns([4, 1])
    with sc_chart_col:
        st.plotly_chart(fig2, use_container_width=True, key="scatter_viz_2")

    with sc_guide_col:
        st.write("") 
        with st.popover("Reading Chart"):
            st.markdown("Darker dots represent respondents in **safer communities**.")

    # Interpretation Box
    st.markdown(f"""
        <div style="background-color: #FFF5F5; padding: 15px; border-radius: 10px; border-left: 5px solid #FFB6C1;">
            <p style="margin: 0; color: #333;">
                <b>Interpretation:</b> The distribution demonstrates that life satisfaction generally rises in line with social support.
                Furthermore, the concentration of darker red dots at greater satisfaction levels indicates that overall well-being is significantly strengthened by community safety.
            </p>
        </div>
    """, unsafe_allow_html=True)


# VISUALIZATION 3: DYNAMIC DISTRIBUTION (Histogram)
with st.expander("Visualization 3: Distribution of Scores", expanded=True):
    
    # 1. Selection Menu
    selected_dist = st.selectbox(
        "Select Index to View Distribution:", 
        ['life_satisfaction', 'social_support_index', 'emotion_management_index'],
        key="dist_selector_v3"
    )
    
    # 2. Define Dynamic Interpretation Text
    if selected_dist == 'life_satisfaction':
        text = "The majority of respondents received a score of 3 or 4, indicating a right-skewed data set. This suggests that people generally have moderate to high levels of life satisfaction."
    elif selected_dist == 'social_support_index':
        text = "Few people feel alone (scores of 2 or less), and the peak at 3.5 indicates that while people feel well-supported, their experiences are generally very similar."
    else:
        text = "The majority of respondents have a "neutral" or "average" capacity to control their emotions, as indicated by the highest concentration of respondents at score 3."

    # 3. Create the Histogram
    # We use 'marginal="rug"' to show the exact 'point' data locations under the bars
    fig3 = px.histogram(
        df, 
        x=selected_dist, 
        nbins=20, 
        marginal="rug", # Adds tiny lines at the bottom for every 'point' data entry
        color_discrete_sequence=['#D32F2F'],
        opacity=0.85,
        labels={selected_dist: "Score (1-5)"}
    ) 
    
    fig3.update_layout(
        title=f"<b>Frequency Distribution of {selected_dist.replace('_', ' ').title()}</b>",
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[0.8, 5.2], gridcolor='#EEEEEE'),
        yaxis_title="Number of Respondents",
        bargap=0.05 # Small gap makes it look cleaner
    )
    
    st.plotly_chart(fig3, use_container_width=True, key="dist_chart_v3")
    
    # 4. Dynamic Interpretation Box
    st.markdown(f"""
        <div style="background-color: #FFF0F5; padding: 15px; border-radius: 10px; border-left: 5px solid #FFB6C1 ;">
            <p style="margin: 0; color: #333;">
                <b>Interpretation:</b> {text}
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")
# VISUALIZATION 4: GROUP WELL-BEING PROFILE ---
with st.expander("Visualization 4: Group Psychological Profile", expanded=False):
    
    # 1. Prepare Data
    categories = ['Life Sat.', 'Social Support', 'Safety', 'Emotion Mgmt.']
    values = [
        df['life_satisfaction'].mean(), 
        df['social_support_index'].mean(), 
        df['community_safety_index'].mean(), 
        df['emotion_management_index'].mean()
    ]
    
    # Close the loop
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    import plotly.graph_objects as go
    
    fig5 = go.Figure()

    fig5.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        # UPDATED: Bold Deep Red line (#B22222)
        line=dict(color='#B22222', width=5),
        # UPDATED: Semi-transparent Red fill
        fillcolor='rgba(178, 34, 34, 0.4)', 
        name='Group Average'
    ))

    # 3. Clean up the Layout
    fig5.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                # FIX: Darkened grid lines from #f0f0f0 to #BDBDBD
                gridcolor="#BDBDBD", 
                gridwidth=1,
                tickfont=dict(color="#333", size=12),
                angle=45, # Tilts labels for better reading
            ),
            angularaxis=dict(
                # FIX: Darkened outer grid lines
                gridcolor="#BDBDBD",
                rotation=90, 
                direction="clockwise",
                tickfont=dict(size=13, color="black")
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        title={
            'text': "<b>Average Dimensions of Well-being</b>",
            'y': 0.98,
            'x': 0.5,
            'xanchor': 'center'
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=80, b=40, l=40, r=40) # Adds space so labels aren't cut off
    )

    # 4. Display Chart
    st.plotly_chart(fig5, use_container_width=True, key="radar_viz_5")

    # 5. Scientific Insight Box
    st.markdown(f"""
        <div style="background-color: #FFF0F5; padding: 15px; border-radius: 10px; border-left: 5px solid #FFB6C1;">
            <p style="margin: 0; color: #333;">
                <b>Interpretation:</b> A balanced psychological profile is shown by the radar chart, with all dimensions regularly averaging between 3.5 and 4.0. 
                The group's overall well-being is shown by this symmetrical diamond shape, which indicates internal emotional regulation and external environmental factors like safety and support are in balance.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
st.markdown("---")

# VISUALIZATION 5: COMMUNITY CARE IMPACT 
with st.expander("Visualization 5: Community Safety vs. Average Satisfaction", expanded=False):
    
    # 1. Prepare Data: Average satisfaction per Community Safety level
    # We use community_safety_index which we know exists in your df
    if 'community_safety_index' in df.columns:
        # We group by safety and find the mean satisfaction for each level
        safety_avg = df.groupby('community_safety_index')['life_satisfaction'].mean().reset_index()

        # 2. Create Bar Chart
        fig6 = px.bar(
            safety_avg, 
            x='community_safety_index', 
            y='life_satisfaction',
            color='life_satisfaction',
            color_continuous_scale='Reds', # Unified Red/Pink theme
            title="<b>How a Safe Community Drives Life Satisfaction</b>",
            labels={
                'community_safety_index': 'Community Safety Level (1-5)', 
                'life_satisfaction': 'Average Satisfaction'
            }
        )

        fig6.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickmode='linear'),
            coloraxis_showscale=False # Keeps it neat by hiding the side color bar
        )

        # 3. Layout: Chart + Guide
        col_chart6, col_info6 = st.columns([4, 1])
        with col_chart6:
            st.plotly_chart(fig6, use_container_width=True, key="bar_viz_6")
        
        with col_info6:
            st.write("") 
            with st.popover("Guide"):
                st.markdown("""
                    **What to look for:**
                    If the bars get **taller and darker** as the safety level moves from 1 to 5, it proves that safety is a direct requirement for a happy life.
                """)

        # 4. Insight Box
        st.markdown(f"""
            <div style="background-color: #FFF0F5; padding: 15px; border-radius: 10px; border-left: 5px solid #FFB6C1;">
                <p style="margin: 0; color: #333;">
                    <b>Interpretation:</b> The bar chat clearly shows a positive trend, with the Average Satisfaction rising steadily as the Community Safety Level goes from 2 to 5. 
                    Although the anomaly at safety level 2 demonstrates that a tiny segment of the population may still report high satisfaction despite decreased perceived safety, this suggests that a secure environment serves as a crucial basis for individual happiness.
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Column 'community_safety_index' not found.")
        
st.markdown("---")

# VISUALIZATION 6: EMOTIONAL MANAGEMENT SHAPE
with st.expander("Visualization 6: Emotional Stability across Health Status", expanded=False):
    
    # 1. Create Violin Plot
    # UPDATED: Unified Red sequence from light to deep red
    red_sequence = ['#FFCDD2', '#EF9A9A', '#E57373', '#EF5350', '#D32F2F']

    fig7 = px.violin(
        df, 
        x='overall_health', 
        y='emotion_management_index', 
        color='overall_health',
        box=True, 
        points="all",
        color_discrete_sequence=red_sequence,
        title="<b>The 'Shape' of Emotional Management by Health Status</b>"
    )

    fig7.update_layout(
        xaxis_title="Overall Health Status",
        yaxis_title="Emotion Management Score",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )

    # 2. Layout: Chart + Guide
    col_chart7, col_info7 = st.columns([4, 1])
    with col_chart7:
        st.plotly_chart(fig7, use_container_width=True, key="violin_viz_7")
    
    with col_info7:
        st.write("") 
        with st.popover("Guide"):
            st.markdown("The **width** of the violin shows where most people are. A 'fat' middle means most people have average scores.")

    # 3. Insight Box
    st.markdown(f"""
        <div style="background-color: #FFF0F5; padding: 15px; border-radius: 10px; border-left: 5px solid #FFB6C1;">
            <p style="margin: 0; color: #333;">
                <b>Interpretation:</b> This graph shows that as health improves, emotional regulation becomes more reliable. 
                The respondents with "Excellent" health (Level 5) have the most steady and effective emotional resilience, as evidenced by the violins' changing fatness.
            </p>
        </div>
    """, unsafe_allow_html=True)
