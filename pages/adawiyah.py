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

# RESEARCH VISUALIZATIONS (UNIFIED PINK THEME) 

st.markdown("## Research Visualizations")

# VISUALIZATION 1: CORRELATION HEATMAP 
with st.expander("Visualization 1: Correlation Heatmap", expanded=True):
    
    viz1_cols = ['life_satisfaction', 'social_support_index', 'community_safety_index', 'emotion_management_index', 'overall_health']
    available_viz_cols = [col for col in viz1_cols if col in df.columns]

    if len(available_viz_cols) > 1:
        corr_matrix = df[available_viz_cols].corr()

        # UPDATED: color_continuous_scale set to 'Reds' to match the pink theme
        fig1 = px.imshow(
            corr_matrix, 
            text_auto=".2f", 
            color_continuous_scale='Reds', 
            aspect="auto",
            labels=dict(color="Strength"),
            zmin=0, zmax=1 # Focus on positive correlations for a cleaner look
        )

        fig1.update_layout(
            title="<b>Variable Correlation Analysis</b>",
            title_x=0.5,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )

        col_chart1, col_info1 = st.columns([4, 1])
        with col_chart1:
            st.plotly_chart(fig1, use_container_width=True, key="heatmap_1")
        
        with col_info1:
            st.write("") 
            with st.popover("Guide"):
                st.markdown("**Color Key:**\n- Dark Red: Strong Link\n- White: No Link")

        st.markdown(f"""
            <div style="background-color: #FFF0F5; padding: 15px; border-radius: 10px; border-left: 5px solid #FFB6C1;">
                <p style="margin: 0; color: #333;">
                    <b>Interpretation:</b> Darker squares indicate a stronger relationship. For example, a dark 
                    connection between <b>Social Support</b> and <b>Satisfaction</b> confirms that community 
                    is a key driver of well-being.
                </p>
            </div>
        """, unsafe_allow_html=True)

# VISUALIZATION 2: SOCIAL & COMMUNITY IMPACT 
with st.expander("Visualization 2: Social & Community Impact", expanded=False):
    
    sc_col1, sc_col2 = st.columns([2, 2])
    with sc_col1:
        show_trend = st.toggle("Show Analysis Trendline", value=True)
    with sc_col2:
        point_size = st.slider("Point Size", 5, 20, 10)

    # UPDATED: color_continuous_scale set to 'Reds' for consistency
    fig2 = px.scatter(
        df,
        x='social_support_index',
        y='life_satisfaction',
        color='community_safety_index',
        trendline="ols" if show_trend else None,
        opacity=0.8,
        size_max=point_size,
        color_continuous_scale='Reds', 
        labels={'social_support_index': 'Support Score', 'life_satisfaction': 'Satisfaction', 'community_safety_index': 'Safety'}
    )

    # UPDATED: Set trendline color to a darker red/maroon for visibility
    if show_trend:
        fig2.update_traces(line=dict(color='#8B0000'))

    fig2.update_layout(
        title="<b>Impact of Support & Safety</b>",
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    sc_chart_col, sc_guide_col = st.columns([4, 1])
    with sc_chart_col:
        st.plotly_chart(fig2, use_container_width=True, key="scatter_viz_2")

    with sc_guide_col:
        st.write("") 
        with st.popover("Reading Chart"):
            st.markdown("Darker dots represent respondents in **safer communities**.")

    st.markdown(f"""
        <div style="background-color: #FFF0F5; padding: 15px; border-radius: 10px; border-left: 5px solid #FFB6C1;">
            <p style="margin: 0; color: #333;">
                <b>Interpretation:</b> The rising trendline (in dark red) mathematically proves that as 
                <b>Social Support</b> increases, <b>Life Satisfaction</b> follows.
            </p>
        </div>
    """, unsafe_allow_html=True)

# VISUALIZATION 3: DISTRIBUTION
with st.expander("Visualization 3: Distribution of Scores", expanded=False):
    selected_dist = st.selectbox("Select Dimension:", ['life_satisfaction', 'social_support_index', 'emotion_management_index'])
    
    # UPDATED: Kept the primary Soft Pink color (#FFB6C1)
    fig3 = px.histogram(
        df, x=selected_dist, nbins=15, 
        color_discrete_sequence=['#FFB6C1'] 
    ) 
    
    fig3.update_layout(
        title=f"<b>Spread of {selected_dist.replace('_', ' ').title()}</b>",
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        bargap=0.1
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("""
        <div style="background-color: #FFF0F5; padding: 15px; border-radius: 10px; border-left: 5px solid #FFB6C1;">
            <b>Interpretation:</b> This histogram shows where most people fall on the scale. A 
            "right-skewed" graph (more bars on the right) is a positive sign for well-being.
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
        # FIX: Darker, bolder line (Deep Pink)
        line=dict(color='#FF1493', width=5),
        # FIX: Increased opacity from 0.4 to 0.6 for better fill visibility
        fillcolor='rgba(255, 182, 193, 0.6)', 
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
                <b>Interpretation:</b> The "shape" of this web reveals the strengths and weaknesses of the group. 
                A balanced shape indicates holistic well-being.
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
                    <b>Interpretation:</b> This chart shows the 'Average' satisfaction level at every 
                    safety rank. If the climb is steady, it suggests that <b>Environmental Safety</b> is 
                    not just a luxury, but a core <b>foundation</b> for individual well-being.
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Column 'community_safety_index' not found.")
        
st.markdown("---")

