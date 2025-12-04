"""
Total Points Prediction Page
Predict final season points
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.model_loader import load_model, get_feature_order
from utils.ui import load_css, futuristic_header, futuristic_card, render_loading_overlay
import time

# Page config
st.set_page_config(page_title="Total Points | ScoreSight", page_icon="📊", layout="wide")

# Load Global CSS
load_css()

def main():
    # Back Button
    if st.button("🏠 Back to Home"):
        st.switch_page("main.py")
    
    # Header
    futuristic_header("TOTAL POINTS")
    
    col_input, col_viz = st.columns([1, 1])
    
    with col_input:
        st.markdown("### 📈 Current Season Stats")
        
        with st.form("total_points_form"):
            matches_played = st.number_input("Matches Played", 0, 38, 20)
            goals_scored = st.number_input("Goals Scored (GF)", 0, 150, 35)
            goals_conceded = st.number_input("Goals Conceded (GA)", 0, 150, 25)
            
            # Auto-calculate Goal Difference
            goal_diff = goals_scored - goals_conceded
            st.info(f"Calculated Goal Difference (GD): {goal_diff}")
            
            submitted = st.form_submit_button("🔮 Predict Final Points")
    
    with col_viz:
        if submitted:
            try:
                # Load model
                # Loading Animation
                loader_placeholder = st.empty()
                render_loading_overlay(loader_placeholder)
                time.sleep(1.5)
                
                # Load model
                model = load_model("total_points")
                
                # Clear loader
                loader_placeholder.empty()
                
                # Prepare input data
                feature_order = get_feature_order("total_points")
                
                input_data = {
                    "played": matches_played,
                    "gf": goals_scored,
                    "ga": goals_conceded,
                    "gd": goal_diff
                }
                
                input_df = pd.DataFrame([input_data])[feature_order]
                
                # Predict
                predicted_points = model.predict(input_df)[0]
                
                # Display Result
                futuristic_card("Projected Final Points", int(round(predicted_points)), "After 38 Matches", "green")
                
                # Simple trajectory visualization
                current_points = (predicted_points / 38) * matches_played # Rough estimate
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=[0, matches_played, 38],
                    y=[0, current_points, predicted_points],
                    mode='lines+markers',
                    name='Points Trajectory',
                    line=dict(color='#0aff0a', width=4),
                    marker=dict(size=10, color='#0aff0a')
                ))
                
                fig.update_layout(
                    title="Projected Season Trajectory",
                    xaxis_title="Matches Played",
                    yaxis_title="Points",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    margin=dict(t=40, b=20, l=20, r=20),
                    height=300
                )
                
                st.plotly_chart(fig, width="stretch")
                
            except Exception as e:
                st.error(f"Prediction Error: {str(e)}")
        else:
            st.info("👈 Enter current team stats to project the final season tally.")

if __name__ == "__main__":
    main()
