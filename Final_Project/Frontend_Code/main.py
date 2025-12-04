import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from utils.ui import load_css, futuristic_header, logo_container, futuristic_divider

# Page config
st.set_page_config(
    page_title="ScoreSight | AI Football Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load Global CSS
load_css()

def main():
    # Dynamic Logo
    logo_path = Path(__file__).parent / "image/logo_dark.jpg" # Default to dark for the futuristic theme
    if logo_path.exists():
        st.logo(str(logo_path), icon_image=str(logo_path))
    
    # Hero Section - Centered Layout
    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    
    if logo_path.exists():
        logo_container(str(logo_path))
            
    futuristic_header("SCORESIGHT AI")
    
    st.markdown("""
    <div class="hero-text animate-fade-in delay-100">
        <p class="hero-desc">
            Advanced machine learning algorithms predicting the beautiful game. 
            Experience the future of football analytics.
        </p>
    </div>
    """, unsafe_allow_html=True)

    futuristic_divider()

    # Navigation Grid
    col1, col2 = st.columns(2)
    
    with col1:
        # League Winner Card
        st.markdown("""
        <div class="card animate-slide-up delay-200">
            <h3 style="color: #00f3ff;">🏆 League Winner</h3>
            <p>Predict the EPL champion using season-long performance metrics.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Module ↗", key="btn_league"):
            st.switch_page("pages/1_🏆_League_Winner.py")
            
        # Top Scorer Card
        st.markdown("""
        <div class="card animate-slide-up delay-400" style="margin-top: 20px;">
            <h3 style="color: #bc13fe;">👟 Top Scorer</h3>
            <p>Forecast the Golden Boot winner with player performance analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Module ↗", key="btn_scorer"):
            st.switch_page("pages/3_👟_Top_Scorer.py")

    with col2:
        # Match Winner Card
        st.markdown("""
        <div class="card animate-slide-up delay-300">
            <h3 style="color: #0aff0a;">⚽ Match Winner</h3>
            <p>Predict match outcomes (Home/Draw/Away) with high precision.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Module ↗", key="btn_match"):
            st.switch_page("pages/2_⚽_Match_Winner.py")
            
        # Total Points Card
        st.markdown("""
        <div class="card animate-slide-up delay-500" style="margin-top: 20px;">
            <h3 style="color: #ff0055;">📊 Total Points</h3>
            <p>Estimate final season points tally for any team.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Module ↗", key="btn_points"):
            st.switch_page("pages/4_📊_Total_Points.py")

    # Footer
    futuristic_divider()
    st.markdown("""
    <div class="footer-text animate-fade-in delay-500">
        POWERED BY ADVANCED ML MODELS | V2.0.0
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
