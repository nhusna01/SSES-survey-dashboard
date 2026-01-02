import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from preprocess import load_data  # Using your central loading logic

st.title("🧠 Emotional Resilience Analysis")

# Use the central loader. 
# If you need the specific 'Hafizah_SSES_Cleaned' file, 
# ensure GOOGLE_SHEET_URL in configuration.py points to it.
try:
    df = load_data()
    
    # Check if the specific columns exist in your main dataset
    objective3_cols = [
        'calm_under_pressure', 
        'emotional_control', 
        'adaptability', 
        'self_motivation', 
        'task_persistence', 
        'teamwork'
    ]
    
    # Verify columns exist before processing
    missing_cols = [c for c in objective3_cols if c not in df.columns]
    
    if missing_cols:
        st.warning(f"Note: Some columns are missing from the current dataset: {', '.join(missing_cols)}")
        # Allow user to pick from available columns instead
        objective3_cols = [c for c in objective3_cols if c in df.columns]

    if not objective3_cols:
        st.error("No resilience columns found in the dataset. Please check your CSV headers.")
    else:
        # Data Cleaning
        df[objective3_cols] = df[objective3_cols].apply(pd.to_numeric, errors="coerce")
        df[objective3_cols] = df[objective3_cols].fillna(df[objective3_cols].median())

        # --- Metrics ---
        agree_prop = df[objective3_cols].isin([4, 5]).mean()
        m1, m2, m3 = st.columns(3)
        m1.metric("Avg. Resilience", f"{agree_prop.mean():.1%}")
        m2.metric("Strongest", agree_prop.idxmax().replace('_', ' ').title())
        m3.metric("Growth Area", agree_prop.idxmin().replace('_', ' ').title())

        # --- Radar Chart ---
        st.subheader("Resilience Profile")
        mean_scores = df[objective3_cols].mean()
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=mean_scores.values.tolist() + [mean_scores.values[0]],
            theta=[c.replace('_', ' ').title() for c in objective3_cols] + [objective3_cols[0].replace('_', ' ').title()],
            fill='toself',
            line_color='#00CC96'
        ))
        st.plotly_chart(fig_radar, use_container_width=True)

        # --- Heatmap ---
        st.subheader("Attribute Correlations")
        fig_corr = px.imshow(
            df[objective3_cols].corr(), 
            text_auto=".2f", 
            color_continuous_scale="RdBu_r"
        )
        st.plotly_chart(fig_corr, use_container_width=True)

except Exception as e:
    st.error(f"Failed to load data: {e}")
