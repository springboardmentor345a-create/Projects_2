"""
League Winner Prediction Page
Predict the EPL Champion
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
st.set_page_config(page_title="League Winner | ScoreSight", page_icon="🏆", layout="wide")

# Load Global CSS
load_css()

def main():
    # Back Button
    if st.button("🏠 Back to Home"):
        st.switch_page("main.py")
    
    # Header
    futuristic_header("LEAGUE WINNER")
    
    col_input, col_viz = st.columns([1, 1])
    
    with col_input:
        st.markdown("### 📈 Team Performance Stats")
        
        with st.form("league_winner_form"):
            wins = st.number_input("Wins", 0, 38, 25)
            draws = st.number_input("Draws", 0, 38, 5)
            losses = st.number_input("Losses", 0, 38, 8)
            points_per_game = st.number_input("Points Per Game", 0.0, 3.0, 2.1, 0.01)
            goals_scored = st.number_input("Goals Scored", 0, 150, 80)
            goals_conceded = st.number_input("Goals Conceded", 0, 150, 30)
            
            submitted = st.form_submit_button("🔮 Predict Champion Status")
    
    with col_viz:
        if submitted:
            try:
                # Loading Animation
                loader_placeholder = st.empty()
                render_loading_overlay(loader_placeholder)
                time.sleep(1.5) # Show animation for at least 1.5s
                
                # Load model
                model = load_model("league_winner")
                
                # Clear loader
                loader_placeholder.empty()
                
                # Prepare input data
                feature_order = get_feature_order("league_winner")
                
                input_data = {
                    "wins": wins,
                    "draws": draws,
                    "losses": losses,
                    "points_per_game": points_per_game,
                    "goals_scored": goals_scored,
                    "goals_conceded": goals_conceded
                }
                
                input_df = pd.DataFrame([input_data])[feature_order]
                
                # Predict
                prediction = model.predict(input_df)[0]
                probability = model.predict_proba(input_df)[0][1]
                
                # Display Result
                if prediction == 1:
                    futuristic_card("Prediction", "CHAMPION", f"Probability: {probability:.1%}", "cyan")
                else:
                    futuristic_card("Prediction", "NOT CHAMPION", f"Probability: {probability:.1%}", "purple")
                
                # Radar Chart
                categories = ['Wins', 'PPG', 'Goals', 'Defense']
                # Normalize values for visualization roughly
                values = [wins/38, points_per_game/3, goals_scored/100, (100-goals_conceded)/100]
                
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name='Team Stats',
                    line_color='#00f3ff',
                    fillcolor='rgba(0, 243, 255, 0.2)'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 1], showticklabels=False),
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
            st.info("👈 Enter team stats to predict if they will win the league.")

if __name__ == "__main__":
    main()
