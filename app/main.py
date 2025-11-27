import streamlit as st
from pathlib import Path

# Page config
st.set_page_config(
    page_title="ScoreSight - EPL Prediction",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Create a simple CSS file for styling
css_path = Path("app/style.css")
if not css_path.exists():
    with open(css_path, "w") as f:
        f.write("""
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f8fafc;
        }
        .card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 20px;
            transition: transform 0.2s;
            height: 100%;
        }
        .card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.1);
        }
        h1, h2, h3 {
            color: #f8fafc !important;
        }
        .stButton button {
            background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 600;
            width: 100%;
        }
        """)

local_css("app/style.css")

def main():
    # Banner Image - Resized and Centered
    banner_path = Path("app/image/banner.png")
    if banner_path.exists():
        # Use columns to center and constrain width/height effectively
        # [1, 2, 1] ratio means the image takes up 2/4 = 50% of width
        _, col_banner, _ = st.columns([1, 2, 1])
        with col_banner:
            st.image(str(banner_path), use_container_width=True)
    
    # Title and Intro
    st.markdown("""
    <div style='text-align: center; padding: 10px 0 30px 0;'>
        <h1 style='font-size: 3.5rem; margin-bottom: 10px; background: linear-gradient(90deg, #38bdf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>ScoreSight</h1>
        <h3 style='font-weight: 300; opacity: 0.9;'>Advanced EPL Prediction System</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation Cards
    st.markdown("### 🎯 Select a Prediction Module")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🏆 League Winner</h3>
            <p>Predict which team will be crowned the Premier League Champion.</p>
        </div>
        """, unsafe_allow_html=True)
        # Fix: Ensure path is relative to entrypoint (app/main.py) -> pages/1_...
        st.page_link("pages/1_🏆_League_Winner.py", label="Go to League Winner", icon="🏆", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3>👟 Top Scorer</h3>
            <p>Forecast the Golden Boot winner and player goal tallies.</p>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/3_👟_Top_Scorer.py", label="Go to Top Scorer", icon="👟", use_container_width=True)
            
    with col2:
        st.markdown("""
        <div class="card">
            <h3>⚽ Match Winner</h3>
            <p>Predict the outcome of any specific match-up (Home/Draw/Away).</p>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/2_⚽_Match_Winner.py", label="Go to Match Winner", icon="⚽", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <h3>📊 Total Points</h3>
            <p>Estimate the final season points tally for any team.</p>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/4_📊_Total_Points.py", label="Go to Total Points", icon="📊", use_container_width=True)

if __name__ == "__main__":
    main()
