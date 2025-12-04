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
        st.markdown("### Select Teams")
        col1, col2 = st.columns(2)
        
        with col1:
            home_team = st.selectbox("Home Team", teams, index=0)
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
