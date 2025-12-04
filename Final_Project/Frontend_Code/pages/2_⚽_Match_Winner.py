"""
Match Winner Prediction Page
Predict Home/Draw/Away outcome
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.model_loader import load_model, get_feature_order
from utils.data_loader import load_match_winner_data, get_unique_teams, calculate_match_features
from utils.ui import load_css, futuristic_header, futuristic_card, render_loading_overlay
import time

# Page config
st.set_page_config(page_title="Match Winner | ScoreSight", page_icon="⚽", layout="wide")

# Load Global CSS
load_css()

def main():
    # Back Button
    if st.button("🏠 Back to Home"):
        st.switch_page("main.py")
    
    # Header
    futuristic_header("MATCH WINNER")
    
    # Load data
    try:
        df = load_match_winner_data()
        teams = get_unique_teams("match_winner")
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return

    # Create tabs for different input modes
    tab1, tab2 = st.tabs(["🤖 Team Selection (Auto)", "✍️ Manual Input"])
    
    # ==========================================
    # TAB 1: AUTO SELECTION
    # ==========================================
    with tab1:
        st.markdown('<div class="animate-slide-up delay-100">', unsafe_allow_html=True)
        st.markdown("### Select Teams")
        col1, col2 = st.columns(2)
        
        with col1:
            home_team = st.selectbox("Home Team", teams, index=0)
        with col2:
            away_team = st.selectbox("Away Team", teams, index=1)
            
        if home_team == away_team:
            st.warning("Please select different teams for Home and Away.")
        else:
            if st.button("🔮 Predict Match (Auto)", type="primary"):
                try:
                    # Loading Animation
                    loader_placeholder = st.empty()
                    render_loading_overlay(loader_placeholder)
                    time.sleep(2.0)
                    
                    # Clear loader
                    loader_placeholder.empty()
                    
                    # 1. Calculate Features
                    features = calculate_match_features(home_team, away_team, df)
                    
                    # 2. Load Model & Predict
                    model = load_model("match_winner")
                    feature_order = get_feature_order("match_winner")
                    input_df = pd.DataFrame([features])[feature_order]
                    
                    probabilities = model.predict_proba(input_df)[0]
                    probs = {
                        "Home Win": probabilities[0],
                        "Not Home Win": probabilities[1]
                    }
                    
                    # 3. Display Results
                    st.markdown('<div class="animate-pop-in">', unsafe_allow_html=True)
                    display_prediction_results(probs)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # 4. Show Stats Used
                    st.markdown("---")
                    st.markdown("### 📊 Match Stats Used")
                    col_s1, col_s2, col_s3 = st.columns(3)
                    with col_s1:
                        st.metric("Points Gap", f"{features.get('Points_Gap', 0):.1f}")
                        st.metric("Goal Diff Gap", f"{features.get('Goal_Difference_Gap', 0):.1f}")
                    with col_s2:
                        st.metric("Home Win Streak", int(features.get('Home_Win_Streak', 0)))
                        st.metric("Away Win Streak", int(features.get('Away_Win_Streak', 0)))
                    with col_s3:
                        st.metric("Home Goals Scored", int(features.get('Home_Goals_Scored', 0)))
                        st.metric("Away Goals Scored", int(features.get('Away_Goals_Scored', 0)))
                            
                except Exception as e:
                    st.error(f"Prediction Error: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # TAB 2: MANUAL INPUT
    # ==========================================
    with tab2:
        st.markdown('<div class="animate-slide-up delay-200">', unsafe_allow_html=True)
        st.markdown("### Manual Feature Input")
        
        if st.button("🎲 Randomize Inputs"):
            st.session_state['random_seed'] = np.random.randint(0, 1000)
            
        np.random.seed(st.session_state.get('random_seed', 42))
        
        with st.form("manual_match_form"):
            col_m1, col_m2 = st.columns(2)
            
            with col_m1:
                points_gap = st.number_input("Points Gap (Home - Away)", value=float(np.random.randint(-20, 20)))
                gd_gap = st.number_input("Goal Difference Gap", value=float(np.random.randint(-15, 15)))
                form_gap = st.number_input("Form Gap", value=float(np.random.randint(-10, 10)))
                home_gd = st.number_input("Home Goal Difference", value=float(np.random.randint(-20, 20)))
                away_gd = st.number_input("Away Goal Difference", value=float(np.random.randint(-20, 20)))
                
            with col_m2:
                home_streak = st.number_input("Home Win Streak", value=int(np.random.randint(0, 5)), min_value=0)
                away_streak = st.number_input("Away Win Streak", value=int(np.random.randint(0, 5)), min_value=0)
                home_scored = st.number_input("Home Goals Scored", value=int(np.random.randint(0, 4)), min_value=0)
                away_scored = st.number_input("Away Goals Scored", value=int(np.random.randint(0, 4)), min_value=0)
                home_conceded = st.number_input("Home Goals Conceded", value=int(np.random.randint(0, 3)), min_value=0)
                
            submitted = st.form_submit_button("🔮 Predict Match (Manual)", type="primary")
            
            if submitted:
                try:
                    # Loading Animation
                    loader_placeholder = st.empty()
                    render_loading_overlay(loader_placeholder)
                    time.sleep(2.0)
                    
                    # Clear loader
                    loader_placeholder.empty()
                    
                    input_data = {
                        "Points_Gap": points_gap,
                        "Goal_Difference_Gap": gd_gap,
                        "Form_Gap": form_gap,
                        "Home_Goal_Difference": home_gd,
                        "Away_Goal_Difference": away_gd,
                        "Home_Win_Streak": home_streak,
                        "Away_Win_Streak": away_streak,
                        "Home_Goals_Scored": home_scored,
                        "Away_Goals_Scored": away_scored,
                        "Home_Goals_Conceded": home_conceded
                    }
                    
                    model = load_model("match_winner")
                    feature_order = get_feature_order("match_winner")
                    input_df = pd.DataFrame([input_data])[feature_order]
                    
                    probabilities = model.predict_proba(input_df)[0]
                    probs = {
                        "Home Win": probabilities[0],
                        "Not Home Win": probabilities[1]
                    }
                    
                    st.markdown('<div class="animate-pop-in">', unsafe_allow_html=True)
                    display_prediction_results(probs)
                    st.markdown('</div>', unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"Prediction Error: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)

def display_prediction_results(probs):
    """Helper to display prediction results consistently"""
    winner = max(probs, key=probs.get)
    confidence = probs[winner] * 100
    
    col_res, col_chart = st.columns([1, 2])
    
    with col_res:
        color = "green" if winner == "Home Win" else "purple"
        futuristic_card("Predicted Outcome", winner.upper(), f"Confidence: {confidence:.1f}%", color)
        
    with col_chart:
        fig = go.Figure(data=[
            go.Bar(
                x=list(probs.keys()),
                y=[v*100 for v in probs.values()],
                marker_color=['#0aff0a', '#bc13fe'],
                text=[f"{v*100:.1f}%" for v in probs.values()],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            yaxis_title="Probability (%)",
            margin=dict(t=20, b=20, l=20, r=20),
            height=250
        )
        
        st.plotly_chart(fig, width="stretch")

if __name__ == "__main__":
    main()
