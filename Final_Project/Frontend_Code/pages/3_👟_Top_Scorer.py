"""
Top Scorer Prediction Page
Predict player goals and assists
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.model_loader import load_model, get_feature_order
from utils.ui import load_css, futuristic_header, futuristic_card

# Page config
st.set_page_config(page_title="Top Scorer | ScoreSight", page_icon="👟", layout="wide")

# Load Global CSS
load_css()

def main():
    # Back Button
    if st.button("🏠 Back to Home"):
        st.switch_page("main.py")
    
    # Header
    futuristic_header("TOP SCORER")
    
    col_input, col_viz = st.columns([1, 1])
    
    with col_input:
        st.markdown("### 📊 Player Stats Profile")
        
        with st.form("top_scorer_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                position = st.selectbox("Position", ["Forward", "Midfielder", "Defender"])
                age = st.number_input("Age", 16, 45, 25)
                matches_played = st.number_input("Matches Played", 1, 38, 30)
                starts = st.number_input("Starts", 0, 38, matches_played)
                minutes = st.number_input("Minutes Played", 0, 3420, matches_played * 90)
                
            with col2:
                goals_per_90 = st.number_input("Goals per 90", 0.0, 3.0, 0.5, 0.01)
                assists_per_90 = st.number_input("Assists per 90", 0.0, 3.0, 0.2, 0.01)
                xg_per_90 = st.number_input("xG per 90", 0.0, 3.0, 0.45, 0.01)
                npxg_per_90 = st.number_input("npxG per 90", 0.0, 3.0, 0.4, 0.01)
                xag_per_90 = st.number_input("xAG per 90", 0.0, 3.0, 0.2, 0.01)
                npxg_plus_xag_per_90 = st.number_input("npxG + xAG", 0.0, 5.0, 0.6, 0.01)
                non_penalty_goals_per_90 = st.number_input("Non-Penalty Goals per 90", 0.0, 3.0, 0.4, 0.01)
            
            submitted = st.form_submit_button("🔮 Predict Season Stats")
    
    with col_viz:
        if submitted:
            try:
                # Load models
                with st.spinner("Analyzing player profile..."):
                    model_goals = load_model("top_scorer")
                    model_assists = load_model("top_scorer_assists")
                
                # Prepare input data
                feature_order = get_feature_order("top_scorer")
                
                # Feature Engineering
                # 1. Calculate derived ratios (avoid division by zero)
                goals_est = goals_per_90 * (minutes / 90)
                xg_est = xg_per_90 * (minutes / 90)
                assists_est = assists_per_90 * (minutes / 90)
                xag_est = xag_per_90 * (minutes / 90)
                
                goals_per_xg = goals_est / xg_est if xg_est > 0 else 0
                assists_per_xag = assists_est / xag_est if xag_est > 0 else 0
                
                # 2. Calculate Impact Scores
                xag_impact = xag_per_90 * matches_played
                npxg_impact = npxg_per_90 * matches_played
                
                # 3. Calculate Interaction Terms (Required by Model)
                input_data = {
                    "position": position,
                    "age": age,
                    "matches_played": matches_played,
                    "starts": starts,
                    "minutes": minutes,
                    "goals_per_90": goals_per_90,
                    "assists_per_90": assists_per_90,
                    "xg_per_90": xg_per_90,
                    "npxg_per_90": npxg_per_90,
                    "xag_per_90": xag_per_90,
                    "npxg_plus_xag_per_90": npxg_plus_xag_per_90,
                    "non_penalty_goals_per_90": non_penalty_goals_per_90,
                    "goals_per_xg": goals_per_xg,
                    "assists_per_xag": assists_per_xag,
                    "xag_impact": xag_impact,
                    "npxg_impact": npxg_impact,
                    # Interaction Terms
                    "goals_per_90 xg_per_90": goals_per_90 * xg_per_90,
                    "goals_per_90 npxg_per_90": goals_per_90 * npxg_per_90,
                    "goals_per_90 xag_per_90": goals_per_90 * xag_per_90,
                    "goals_per_90 npxg_plus_xag_per_90": goals_per_90 * npxg_plus_xag_per_90,
                    "goals_per_90 matches_played": goals_per_90 * matches_played,
                    "xg_per_90 matches_played": xg_per_90 * matches_played,
                    "npxg_per_90 matches_played": npxg_per_90 * matches_played
                }
                
                input_df = pd.DataFrame([input_data])[feature_order]
                
                # Predict
                predicted_goals = model_goals.predict(input_df)[0]
                predicted_assists = model_assists.predict(input_df)[0]
                
                # Display Result
                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    futuristic_card("Predicted Goals", int(round(predicted_goals)), f"Based on {matches_played} matches", "cyan")
                with col_res2:
                    futuristic_card("Predicted Assists", int(round(predicted_assists)), "Season Projection", "purple")
                
                # Radar Chart
                categories = ['Goals/90', 'xG/90', 'npxG/90', 'xAG/90', 'Contribution']
                values = [goals_per_90, xg_per_90, npxg_per_90, xag_per_90, npxg_plus_xag_per_90]
                
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name='Player Stats',
                    line_color='#00f3ff',
                    fillcolor='rgba(0, 243, 255, 0.2)'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, max(values)*1.2], showticklabels=False),
                        bgcolor='rgba(0,0,0,0)'
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    margin=dict(t=20, b=20, l=20, r=20),
                    height=300,
                    showlegend=False
                )
                
                st.plotly_chart(fig, width="stretch")
                
            except Exception as e:
                st.error(f"Prediction Error: {str(e)}")
        else:
            # Placeholder for visualization area
            st.info("👈 Enter player stats to see the prediction and performance radar.")

if __name__ == "__main__":
    main()
