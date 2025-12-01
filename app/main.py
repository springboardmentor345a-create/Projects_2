import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from utils.ui import load_css

# Page config
st.set_page_config(
    page_title="ScoreSight - EPL Prediction",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load Global CSS
load_css()

def main():
    # Banner Image - Resized and Centered
    banner_path = Path("app/image/banner.png")
    if banner_path.exists():
        _, col_banner, _ = st.columns([1, 2, 1])
        with col_banner:
            st.image(str(banner_path), use_container_width=True)
    
    # Title and Intro
    st.markdown("""
    <div style='text-align: center; padding: 10px 0 40px 0;'>
        <h1 style='font-size: 3.5rem; margin-bottom: 10px; background: linear-gradient(90deg, #38bdf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>ScoreSight</h1>
        <h3 style='font-weight: 300; opacity: 0.9;'>Advanced EPL Prediction System</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation Cards
    st.markdown("### 🎯 Select a Prediction Module")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("""
            <div class="card">
                <h3>🏆 League Winner</h3>
                <p>Predict which team will be crowned the Premier League Champion based on historical data and current form.</p>
            </div>
            """, unsafe_allow_html=True)
            st.page_link("pages/1_🏆_League_Winner.py", label="Go to League Winner", icon="🏆", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("""
            <div class="card">
                <h3>👟 Top Scorer</h3>
                <p>Forecast the Golden Boot winner and estimate player goal and assist tallies for the season.</p>
            </div>
            """, unsafe_allow_html=True)
            st.page_link("pages/3_👟_Top_Scorer.py", label="Go to Top Scorer", icon="👟", use_container_width=True)
            
    with col2:
        with st.container():
            st.markdown("""
            <div class="card">
                <h3>⚽ Match Winner</h3>
                <p>Predict the outcome of any specific match-up (Home Win, Draw, Away Win) using advanced ML models.</p>
            </div>
            """, unsafe_allow_html=True)
            st.page_link("pages/2_⚽_Match_Winner.py", label="Go to Match Winner", icon="⚽", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("""
            <div class="card">
                <h3>📊 Total Points</h3>
                <p>Estimate the final season points tally for any team based on their current performance metrics.</p>
            </div>
            """, unsafe_allow_html=True)
            st.page_link("pages/4_📊_Total_Points.py", label="Go to Total Points", icon="📊", use_container_width=True)

if __name__ == "__main__":
    main()
