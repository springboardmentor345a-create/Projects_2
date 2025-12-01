"""
League Winner Prediction Page
Predict teams that will finish in Top 4
"""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.model_loader import load_model, get_feature_order
from utils.ui import load_css

# Page config
st.set_page_config(page_title="League Winner | ScoreSight", page_icon="🏆", layout="wide")

# Load Global CSS
load_css()

def main():
    # Back Button
    st.page_link("main.py", label="Back to Home", icon="🏠")
    
    # Page Image
    img_path = Path("app/image/league_winner.jpg")
    if img_path.exists():
        _, col_img, _ = st.columns([1, 2, 1])
        with col_img:
            st.image(str(img_path), use_container_width=True)
    
    # Header
    st.markdown("# 🏆 League Winner Prediction")
    st.markdown("### Predict if a team will become the Premier League Champion")
    
    st.markdown("---")
    
    # Create two columns for input and results
    col_input, col_result = st.columns([1, 1])
    
    with col_input:
        st.markdown("### 📊 Enter Team Statistics")
        st.markdown("*Enter the team's season statistics to predict Championship chances*")
        
        with st.form("league_winner_form"):
            # Input fields for all required features
            wins = st.number_input(
                "**Wins** 🏅",
                min_value=0,
                max_value=38,
                value=20,
                help="Number of matches won in the season"
            )
            
            draws = st.number_input(
                "**Draws** ⚖️",
                min_value=0,
                max_value=38,
                value=8,
                help="Number of matches drawn"
            )
            
            losses = st.number_input(
                "**Losses** ❌",
                min_value=0,
                max_value=38,
                value=10,
                help="Number of matches lost"
            )
            
            points_per_game = st.number_input(
                "**Points Per Game** 📈",
                min_value=0.0,
                max_value=3.0,
                value=1.84,
                step=0.01,
                format="%.2f",
                help="Average points earned per match"
            )
            
            goals_scored = st.number_input(
                "**Goals Scored** ⚽",
                min_value=0,
                max_value=150,
                value=65,
                help="Total goals scored in the season"
            )
            
            goals_conceded = st.number_input(
                "**Goals Conceded** 🥅",
                min_value=0,
                max_value=150,
                value=35,
                help="Total goals conceded in the season"
            )
            
            # Submit button
            submitted = st.form_submit_button("🔮 Predict Championship Chances", use_container_width=True)
    
    with col_result:
        st.markdown("### 🎯 Prediction Result")
        
        if submitted:
            try:
                # Load model
                with st.spinner("Loading model..."):
                    model = load_model("league_winner")
                
                # Prepare input data in correct order
                feature_order = get_feature_order("league_winner")
                input_data = {
                    "wins": wins,
                    "draws": draws,
                    "losses": losses,
                    "points_per_game": points_per_game,
                    "goals_scored": goals_scored,
                    "goals_conceded": goals_conceded
                }
                
                # Create DataFrame with correct feature order
                input_df = pd.DataFrame([input_data])[feature_order]
                
                # Make prediction
                with st.spinner("Analyzing team performance..."):
                    prediction = model.predict(input_df)[0]
                    
                    # Get probability if available
                    if hasattr(model, 'predict_proba'):
                        probabilities = model.predict_proba(input_df)[0]
                        confidence = max(probabilities) * 100
                    else:
                        confidence = 95  # Model accuracy
                
                # Display result
                if prediction == 1:
                    st.markdown(f"""
                    <div class="card" style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(16, 185, 129, 0.2) 100%); border-color: #22c55e;">
                        <h2 style='margin: 0; color: #4ade80 !important;'>🏆 LEAGUE CHAMPION</h2>
                        <h1 style='font-size: 4rem; margin: 20px 0; color: #ffffff;'>LIKELY</h1>
                        <p style='font-size: 1.2rem; opacity: 0.9;'>Confidence: {confidence:.1f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.success("**Predicted to WIN the Premier League! 🥇**")
                else:
                    st.markdown(f"""
                    <div class="card" style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.2) 100%); border-color: #ef4444;">
                        <h2 style='margin: 0; color: #f87171 !important;'>🏆 LEAGUE CHAMPION</h2>
                        <h1 style='font-size: 4rem; margin: 20px 0; color: #ffffff;'>UNLIKELY</h1>
                        <p style='font-size: 1.2rem; opacity: 0.9;'>Confidence: {confidence:.1f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.warning("**Unlikely to win the title this season**")
                
                # Display input summary
                st.markdown("### 📋 Input Summary")
                
                # Calculate derived stats
                total_matches = wins + draws + losses
                goal_difference = goals_scored - goals_conceded
                total_points = wins * 3 + draws
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Matches", total_matches)
                    st.metric("Total Points", total_points)
                    st.metric("Win Rate", f"{(wins/max(total_matches,1)*100):.1f}%")
                
                with col2:
                    st.metric("Goal Difference", f"+{goal_difference}" if goal_difference >= 0 else str(goal_difference))
                    st.metric("Goals Scored", goals_scored)
                    st.metric("Goals Conceded", goals_conceded)
                
            except Exception as e:
                st.error(f"❌ Prediction Error: {str(e)}")
                st.exception(e)
        else:
            st.info("👈 Fill in the team statistics and click **Predict** to see results")
            
            # Show example
            st.markdown("### 💡 Example Input")
            st.markdown("""
            <div class="card">
                <h4>Champion Team Profile (Typical Stats)</h4>
                <ul style='line-height: 2;'>
                    <li><strong>Wins:</strong> 25-30</li>
                    <li><strong>Draws:</strong> 5-8</li>
                    <li><strong>Losses:</strong> 2-5</li>
                    <li><strong>PPG:</strong> 2.3+</li>
                    <li><strong>Goals Scored:</strong> 85+</li>
                    <li><strong>Goals Conceded:</strong> <35</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
