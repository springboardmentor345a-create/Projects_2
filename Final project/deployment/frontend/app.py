"""
EPL Prediction System - Streamlit Application
Main entry point with navigation to all prediction models.
"""
import sys
import os

# Add project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from frontend.utils.styles import get_custom_css

# Page configuration
st.set_page_config(
    page_title="EPL Prediction System",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit's default pages navigation  
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    
    /* Custom Floating Hamburger Button - Always Visible */
    .custom-menu-btn {
        position: fixed;
        top: 1rem;
        left: 1rem;
        z-index: 999999;
        background: rgba(57, 255, 20, 0.1);
        border: 2px solid #39ff14;
        border-radius: 8px;
        padding: 0.75rem;
        cursor: pointer;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        display: flex;
        flex-direction: column;
        gap: 4px;
        width: 40px;
        height: 40px;
        justify-content: center;
        align-items: center;
    }
    
    .custom-menu-btn:hover {
        background: rgba(57, 255, 20, 0.2);
        box-shadow: 0 0 20px rgba(57, 255, 20, 0.4);
        transform: scale(1.05);
    }
    
    .custom-menu-btn span {
        width: 20px;
        height: 2px;
        background: #39ff14;
        display: block;
        transition: all 0.3s ease;
    }
    
    /* Style Streamlit's collapse button when it appears */
    [data-testid="collapsedControl"] {
        background: rgba(57, 255, 20, 0.1) !important;
        border: 2px solid #39ff14 !important;
        border-radius: 8px !important;
        color: #39ff14 !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background: rgba(57, 255, 20, 0.2) !important;
        box-shadow: 0 0 20px rgba(57, 255, 20, 0.4) !important;
    }
    
    [data-testid="collapsedControl"] svg {
        color: #39ff14 !important;
        fill: #39ff14 !important;
    }
</style>
""", unsafe_allow_html=True)

# Apply custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

def go_to_page(page_name):
    """Navigate to a specific page."""
    st.session_state.current_page = page_name
    st.rerun()

# Main App
if st.session_state.current_page == 'home':
    # Hero Section
    st.markdown("""
<div class="float-animation" style="text-align: center; margin-bottom: 2rem; padding: 4rem 0; background: radial-gradient(circle at center, rgba(0, 242, 255, 0.1) 0%, transparent 70%);">
    <h1 style="margin-bottom: 0.5rem;">PREMIER LEAGUE</h1>
    <h1 style="margin-top: -1rem; color: var(--text-primary);">INTELLIGENCE</h1>
    <p style="font-size: 1.5rem; color: var(--text-secondary); margin-bottom: 3rem; letter-spacing: 0.1em;">
        POWERED BY ADVANCED METRICS & THE EXCLUSIVE SCORESIGHT ENGINE
    </p>
</div>
""", unsafe_allow_html=True)
    
    # Enter Arena Button (Centered)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # We use a custom styled button here
        st.markdown("""
<style>
div.stButton > button:first-child {
    background: rgba(57, 255, 20, 0.1);
    border: 2px solid #39ff14;
    color: #39ff14;
    font-size: 1.5rem;
    padding: 1rem 2rem;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    box-shadow: 0 0 30px rgba(57, 255, 20, 0.2);
}
div.stButton > button:first-child:hover {
    background: #39ff14;
    color: black;
    box-shadow: 0 0 50px rgba(57, 255, 20, 0.6);
}
</style>
""", unsafe_allow_html=True)
        if st.button("ENTER THE ARENA", use_container_width=True):
            go_to_page('match_winner')
            
    st.markdown("<div style='height: 4rem'></div>", unsafe_allow_html=True)
    
    # Feature Cards Grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
<div class="glass-card">
    <h3>🏆 Match Winner</h3>
    <p style="color: #94a3b8; margin-bottom: 1.5rem;">Predict the outcome of individual matches with high accuracy.</p>
</div>
""", unsafe_allow_html=True)
        if st.button("Launch Predictor", key="btn_match"):
            go_to_page('match_winner')
            
        st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)
        
        st.markdown("""
<div class="glass-card">
    <h3>📊 Total Points</h3>
    <p style="color: #94a3b8; margin-bottom: 1.5rem;">Forecast final team standings and total points.</p>
</div>
""", unsafe_allow_html=True)
        if st.button("View Projections", key="btn_points"):
            go_to_page('total_points')

    with col2:
        st.markdown("""
<div class="glass-card">
    <h3>👑 League Winner</h3>
    <p style="color: #94a3b8; margin-bottom: 1.5rem;">Identify the potential champion of the season.</p>
</div>
""", unsafe_allow_html=True)
        if st.button("See Champion", key="btn_league"):
            go_to_page('league_winner')
            
        st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)
        
        st.markdown("""
<div class="glass-card">
    <h3>⚽ Player Goals</h3>
    <p style="color: #94a3b8; margin-bottom: 1.5rem;">Predict top scorers and goal tallies.</p>
</div>
""", unsafe_allow_html=True)
        if st.button("Analyze Goals", key="btn_goals"):
            go_to_page('goals')

    with col3:
        st.markdown("""
<div class="glass-card">
    <h3>🎯 Player Assists</h3>
    <p style="color: #94a3b8; margin-bottom: 1.5rem;">Track playmakers and assist leaders.</p>
</div>
""", unsafe_allow_html=True)
        if st.button("Track Assists", key="btn_assists"):
            go_to_page('assists')
            
        st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)
        
        # Stats/Info Card
        st.markdown("""
<div class="glass-card pulse-glow" style="border-color: var(--primary-color);">
    <h3 style="color: var(--primary-color)">🚀 AI Powered</h3>
    <p style="color: #94a3b8;">Our models use advanced algorithms to analyze historical data and current form.</p>
</div>
""", unsafe_allow_html=True)

# Import and display pages based on navigation
elif st.session_state.current_page == 'match_winner':
    if st.button("← Back to Home", key="back_match"):
        go_to_page('home')
    from pages import match_winner
    match_winner.show()
    
elif st.session_state.current_page == 'league_winner':
    if st.button("← Back to Home", key="back_league"):
        go_to_page('home')
    from pages import league_winner
    league_winner.show()
    
elif st.session_state.current_page == 'total_points':
    if st.button("← Back to Home", key="back_points"):
        go_to_page('home')
    from pages import total_points
    total_points.show()
    
elif st.session_state.current_page == 'goals':
    if st.button("← Back to Home", key="back_goals"):
        go_to_page('home')
    from pages import goals
    goals.show()
    
elif st.session_state.current_page == 'assists':
    if st.button("← Back to Home", key="back_assists"):
        go_to_page('home')
    from pages import assists
    assists.show()

# Sidebar Navigation (Always visible)
with st.sidebar:
    st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style="font-size: 2rem; margin: 0;">⚽</h1>
    <h3 style="margin: 0; color: var(--primary-color);">EPL PREDICTOR</h3>
</div>
""", unsafe_allow_html=True)
    
    if st.button("🏠 DASHBOARD", use_container_width=True):
        go_to_page('home')
    
    st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-secondary); font-size: 0.7rem; letter-spacing: 0.1em; margin-bottom: 0.5rem;'>MODELS</p>", unsafe_allow_html=True)
    
    if st.button("🏆 MATCH WINNER", key="sb_match", use_container_width=True):
        go_to_page('match_winner')
    
    if st.button("👑 LEAGUE WINNER", key="sb_league", use_container_width=True):
        go_to_page('league_winner')
    
    if st.button("📊 TOTAL POINTS", key="sb_points", use_container_width=True):
        go_to_page('total_points')
    
    if st.button("⚽ PLAYER GOALS", key="sb_goals", use_container_width=True):
        go_to_page('goals')
    
    if st.button("🎯 PLAYER ASSISTS", key="sb_assists", use_container_width=True):
        go_to_page('assists')
    
    st.markdown("<div style='margin-top: auto; padding-top: 2rem; text-align: center; color: var(--text-secondary); font-size: 0.8rem;'>v2.0 • AI Powered</div>", unsafe_allow_html=True)
