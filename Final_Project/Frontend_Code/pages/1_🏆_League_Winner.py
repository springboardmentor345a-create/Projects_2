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
        st.markdown('<div class="animate-slide-up delay-100">', unsafe_allow_html=True)
        st.markdown("### 📈 Team Performance Stats")
        
        with st.form("league_winner_form"):
            wins = st.number_input("Wins", 0, 38, 25)
            draws = st.number_input("Draws", 0, 38, 5)
            losses = st.number_input("Losses", 0, 38, 8)
            points_per_game = st.number_input("Points Per Game", 0.0, 3.0, 2.1, 0.01)
            goals_scored = st.number_input("Goals Scored", 0, 150, 80)
            goals_conceded = st.number_input("Goals Conceded", 0, 150, 30)
            
            submitted = st.form_submit_button("🔮 Predict Champion Status")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_viz:
        if submitted:
            try:
                # Loading Animation
                loader_placeholder = st.empty()
                render_loading_overlay(loader_placeholder)
                time.sleep(2.0) # Extended for effect
                
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
                st.markdown('<div class="animate-pop-in">', unsafe_allow_html=True)
                if prediction == 1:
                    futuristic_card("Prediction", "CHAMPION", f"Probability: {probability:.1%}", "cyan")
                else:
                    futuristic_card("Prediction", "NOT CHAMPION", f"Probability: {probability:.1%}", "purple")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # --- New Visualization Section ---
                
                # 1. Gauge Chart for Probability
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = probability * 100,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Championship Probability", 'font': {'size': 24, 'color': "white"}},
                    number = {'suffix': "%", 'font': {'color': "white"}},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                        'bar': {'color': "#00f3ff"},
                        'bgcolor': "rgba(0,0,0,0)",
                        'borderwidth': 2,
                        'bordercolor': "white",
                        'steps': [
                            {'range': [0, 50], 'color': 'rgba(255, 0, 0, 0.3)'},
                            {'range': [50, 80], 'color': 'rgba(255, 165, 0, 0.3)'},
                            {'range': [80, 100], 'color': 'rgba(0, 255, 0, 0.3)'}
                        ],
                        'threshold': {
                            'line': {'color': "white", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                
                fig_gauge.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    font={'color': "white", 'family': "Rajdhani"}
                )
                
                st.plotly_chart(fig_gauge, width="stretch")
                
                # 2. Benchmark Comparison Chart
                # Define benchmarks for a typical champion
                benchmarks = {
                    'Wins': 28,
                    'PPG': 2.4,
                    'Goals': 85,
                    'Defense (GA)': 30 # Lower is better, but for bar chart we might invert or just show raw
                }
                
                # Normalize for comparison (percentage of benchmark)
                # For Defense, we want to be LOWER than benchmark, so maybe we just show raw values side-by-side
                
                categories = ['Wins', 'Points Per Game', 'Goals Scored']
                team_values = [wins, points_per_game, goals_scored]
                benchmark_values = [benchmarks['Wins'], benchmarks['PPG'], benchmarks['Goals']]
                
                fig_bar = go.Figure()
                
                fig_bar.add_trace(go.Bar(
                    y=categories,
                    x=team_values,
                    name='Your Team',
                    orientation='h',
                    marker=dict(color='#00f3ff', line=dict(color='white', width=1))
                ))
                
                fig_bar.add_trace(go.Bar(
                    y=categories,
                    x=benchmark_values,
                    name='Champion Avg',
                    orientation='h',
                    marker=dict(color='rgba(255, 255, 255, 0.3)', line=dict(color='white', width=1))
                ))
                
                from utils.ui import update_plot_layout
                fig_bar = update_plot_layout(fig_bar, title="Vs. Champion Benchmarks", x_title="Value", y_title="")
                fig_bar.update_layout(barmode='group')
                
                st.plotly_chart(fig_bar, width="stretch")
                
            except Exception as e:
                st.error(f"Prediction Error: {str(e)}")
        else:
            st.markdown('<div class="animate-fade-in delay-200">', unsafe_allow_html=True)
            st.info("👈 Enter team stats to predict if they will win the league.")
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
