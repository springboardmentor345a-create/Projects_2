"""
ScoreSight - EPL Prediction Command Center
A premium Streamlit application for Premier League predictions
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Page configuration
st.set_page_config(
    page_title="ScoreSight | EPL Prediction Hub",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "ScoreSight - Advanced EPL Prediction System by Prathamesh Fuke"
    }
)

# Custom CSS for premium design
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Modern Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background - Dark Premium Theme */
    .main {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1f2e 0%, #0f1419 100%);
        border-right: 1px solid rgba(56, 189, 248, 0.1);
    }
    
    /* Premium Card Design */
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 48px rgba(56, 189, 248, 0.2);
        border-color: rgba(56, 189, 248, 0.4);
    }
    
    /* Gradient Text */
    .gradient-text {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        font-size: 3rem;
        letter-spacing: -1px;
    }
    
    /* Stats Display */
    .stat-box {
        background: rgba(56, 189, 248, 0.1);
        border-left: 4px solid #38bdf8;
        padding: 16px;
        border-radius: 8px;
        margin: 8px 0;
    }
    
    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(56, 189, 248, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(56, 189, 248, 0.4);
    }
    
    /* Input Fields */
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>div {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 8px;
        color: white;
    }
    
    /* Success/Warning/Error Messages */
    .stSuccess {
        background: rgba(34, 197, 94, 0.1);
        border-left: 4px solid #22c55e;
    }
    
    .stWarning {
        background: rgba(251, 191, 36, 0.1);
        border-left: 4px solid #fbbf24;
    }
    
    .stError {
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 41, 59, 0.4);
        border-radius: 8px;
        color: rgba(255, 255, 255, 0.7);
        padding: 12px 24px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
        color: white;
    }
    
    /* Metric Container */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #38bdf8;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Animated Gradient Border */
    @keyframes gradient-border {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .animated-border {
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc, #38bdf8);
        background-size: 300% 300%;
        animation: gradient-border 3s ease infinite;
        padding: 2px;
        border-radius: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    load_custom_css()
    
    # Hero Section
    st.markdown('<h1 class="gradient-text">⚽ ScoreSight</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style='background: rgba(56, 189, 248, 0.1); padding: 20px; border-radius: 12px; border-left: 4px solid #38bdf8; margin-bottom: 30px;'>
        <h3 style='color: #38bdf8; margin: 0;'>🎯 Advanced EPL Prediction Command Center</h3>
        <p style='color: rgba(255, 255, 255, 0.8); margin: 8px 0 0 0;'>
            Powered by Machine Learning | 5 Production Models | 95%+ Accuracy
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation Guide
    st.markdown("### 🧭 Navigation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4 style='color: #38bdf8;'>📊 Available Predictions</h4>
            <ul style='color: rgba(255, 255, 255, 0.9); line-height: 2;'>
                <li><strong>League Winner</strong> - Predict Top 4 teams (95% Accuracy)</li>
                <li><strong>Match Winner</strong> - H/D/A prediction (66% Accuracy)</li>
                <li><strong>Top Scorer</strong> - Player goals prediction (R² = 0.957)</li>
                <li><strong>Total Points</strong> - Season points forecast (R² = 0.937)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4 style='color: #818cf8;'>🚀 How to Use</h4>
            <ol style='color: rgba(255, 255, 255, 0.9); line-height: 2;'>
                <li>Select a prediction type from the <strong>sidebar</strong></li>
                <li>Enter the required features/inputs</li>
                <li>Click <strong>"Predict"</strong> to see results</li>
                <li>Explore insights and visualizations</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    # Model Performance Overview
    st.markdown("### 🏆 Model Performance Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-box">
            <h4 style='color: #38bdf8; margin: 0;'>League Winner</h4>
            <p style='font-size: 2rem; font-weight: 700; color: #22c55e; margin: 8px 0;'>95%</p>
            <p style='color: rgba(255, 255, 255, 0.7); margin: 0; font-size: 0.9rem;'>Accuracy (RandomForest)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-box">
            <h4 style='color: #818cf8; margin: 0;'>Match Winner</h4>
            <p style='font-size: 2rem; font-weight: 700; color: #fbbf24; margin: 8px 0;'>66%</p>
            <p style='color: rgba(255, 255, 255, 0.7); margin: 0; font-size: 0.9rem;'>Accuracy (XGBoost)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-box">
            <h4 style='color: #c084fc; margin: 0;'>Top Scorer</h4>
            <p style='font-size: 2rem; font-weight: 700; color: #22c55e; margin: 8px 0;'>0.957</p>
            <p style='color: rgba(255, 255, 255, 0.7); margin: 0; font-size: 0.9rem;'>R² Score (XGBoost)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-box">
            <h4 style='color: #38bdf8; margin: 0;'>Total Points</h4>
            <p style='font-size: 2rem; font-weight: 700; color: #22c55e; margin: 8px 0;'>0.937</p>
            <p style='color: rgba(255, 255, 255, 0.7); margin: 0; font-size: 0.9rem;'>R² Score (Ridge)</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown("### 📈 Project Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Training Matches", "6,840", delta="18 Seasons")
    
    with col2:
        st.metric("Player Records", "2,274", delta="Multiple Seasons")
    
    with col3:
        st.metric("Features Engineered", "96", delta="Advanced ML")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: rgba(255, 255, 255, 0.6); padding: 20px;'>
        <p><strong>ScoreSight v3.0</strong> | Created by Prathamesh Fuke | Powered by Streamlit & ML</p>
        <p style='font-size: 0.85rem;'>📊 Data Quality: Zero nulls | No leakage | Production Ready</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
