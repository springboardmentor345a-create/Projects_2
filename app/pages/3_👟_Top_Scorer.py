"""
Top Scorer Prediction Page
Predict player goals
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.model_loader import load_model, get_feature_order
from utils.ui import load_css

# Page config
st.set_page_config(page_title="Top Scorer | ScoreSight", page_icon="👟", layout="wide")

# Load Global CSS
load_css()

def main():
    # Back Button
    st.page_link("main.py", label="Back to Home", icon="🏠")
    
    # Page Image
    img_path = Path("app/image/topscorer.jpg")
    if img_path.exists():
        _, col_img, _ = st.columns([1, 2, 1])
        with col_img:
            st.image(str(img_path), use_container_width=True)
    
    # Header
    st.markdown("# 👟 Top Scorer Prediction")
    st.markdown("### Forecast a player's total goals for the season")
    
    st.markdown("---")
    
    col_input, col_viz = st.columns([1, 1])
    
    with col_input:
        st.markdown("### 📊 Player Stats")
        
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
            
            submitted = st.form_submit_button("🔮 Predict Season Stats", use_container_width=True)
    
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
                    "npxg_impact": npxg_impact
                }
                
                input_df = pd.DataFrame([input_data])[feature_order]
                
                # Predict
                predicted_goals = model_goals.predict(input_df)[0]
                predicted_assists = model_assists.predict(input_df)[0]
                
                # Display Result
                st.markdown(f"""
                <div style="display: flex; gap: 20px; justify-content: center; margin-top: 20px;">
                    <div class="metric-card" style="text-align: center; flex: 1;">
                        <h2 style="margin:0; color: #f8fafc; font-size: 1.2rem;">Predicted Goals</h2>
                        <h1 style="font-size: 4rem; margin: 10px 0; background: linear-gradient(90deg, #38bdf8, #22c55e); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{int(round(predicted_goals))}</h1>
                    </div>
                    <div class="metric-card" style="text-align: center; flex: 1;">
                        <h2 style="margin:0; color: #f8fafc; font-size: 1.2rem;">Predicted Assists</h2>
                        <h1 style="font-size: 4rem; margin: 10px 0; background: linear-gradient(90deg, #fbbf24, #f87171); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{int(round(predicted_assists))}</h1>
                    </div>
                </div>
                <p style="text-align: center; opacity: 0.8; margin-top: 10px;">Based on {matches_played} matches</p>
                """, unsafe_allow_html=True)
                
                # Radar Chart
                categories = ['Goals/90', 'xG/90', 'npxG/90', 'xAG/90', 'Contribution']
                values = [goals_per_90, xg_per_90, npxg_per_90, xag_per_90, npxg_plus_xag_per_90]
                
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name='Player Stats',
                    line_color='#38bdf8'
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
                
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Prediction Error: {str(e)}")
        else:
            # Placeholder for visualization area
            st.info("👈 Enter player stats to see the prediction and performance radar.")

if __name__ == "__main__":
    main()
