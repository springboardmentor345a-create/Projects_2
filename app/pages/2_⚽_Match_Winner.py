"""
Match Winner Prediction Page
Predict Home Win / Draw / Away Win
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.model_loader import load_model, get_model_info, get_feature_order
from utils.data_loader import load_match_winner_data, get_unique_teams, calculate_match_features

# Page config
st.set_page_config(page_title="Match Winner | ScoreSight", page_icon="⚽", layout="wide")

# Apply custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.main { background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%); }
.stButton>button {
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 32px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("# ⚽ Match Winner Prediction")
    st.markdown("### Predict match outcome: Home Win / Draw / Away Win")
    
    # Model info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model Type", "XGBoost")
    with col2:
        st.metric("Accuracy", "66%")
    with col3:
        st.metric("F1-Score", "0.658")
    
    st.markdown("---")
    
    # Mode selection
    mode = st.radio(
        "**Input Mode:**",
        ["Manual Input", "Team Selection (Auto-Calculate)"],
        horizontal=True,
        help="Choose how you want to input the match features"
    )
    
    col_input, col_result = st.columns([1, 1])
    
    with col_input:
        st.markdown("### 📊 Match Features")
        
        if mode == "Team Selection (Auto-Calculate)":
            st.info("Select teams and we'll automatically fetch their current statistics")
            
            # Load teams
            teams = get_unique_teams("match_winner")
            
            with st.form("match_teams_form"):
                home_team = st.selectbox("🏠 **Home Team**", teams, index=0 if teams else None)
                away_team = st.selectbox("✈️ **Away Team**", teams, index=1 if len(teams) > 1 else 0)
                
                submitted = st.form_submit_button("🔮 Predict Match Winner", use_container_width=True)
                
                if submitted:
                    # Load match data
                    df = load_match_winner_data()
                    features = calculate_match_features(home_team, away_team, df)
                    
                    if features is None:
                        st.error("❌ Could not find statistics for the selected teams")
                        return
                    
                    # Store features in session state
                    st.session_state['match_features'] = features
                    st.session_state['home_team'] = home_team
                    st.session_state['away_team'] = away_team
                    st.session_state['prediction_mode'] = 'auto'
        
        else:  # Manual Input
            st.markdown("*Enter the match statistics manually*")
            
            with st.form("match_manual_form"):
                points_gap = st.number_input(
                    "**Points Gap** (Home - Away)",
                    min_value=-100,
                    max_value=100,
                    value=5,
                    help="Difference in current league points (Home team points - Away team points)"
                )
                
                goal_diff_gap = st.number_input(
                    "**Goal Difference Gap** (Home - Away)",
                    min_value=-100,
                    max_value=100,
                    value=10,
                    help="Difference in goal difference (Home GD - Away GD)"
                )
                
                form_gap = st.number_input(
                    "**Form Gap** (Recent Points)",
                    min_value=-30,
                    max_value=30,
                    value=3,
                    help="Difference in recent form points (Home - Away)"
                )
                
                home_gd = st.number_input(
                    "**Home Team Goal Difference**",
                    min_value=-100,
                    max_value=100,
                    value=15,
                    help="Home team's goal difference this season"
                )
                
                away_gd = st.number_input(
                    "**Away Team Goal Difference**",
                    min_value=-100,
                    max_value=100,
                    value=5,
                    help="Away team's goal difference this season"
                )
                
                home_streak = st.number_input(
                    "**Home Team Win Streak**",
                    min_value=0,
                    max_value=20,
                    value=2,
                    help="Number of consecutive wins for home team"
                )
                
                away_streak = st.number_input(
                    "**Away Team Win Streak**",
                    min_value=0,
                    max_value=20,
                    value=0,
                    help="Number of consecutive wins for away team"
                )
                
                home_scored = st.number_input(
                    "**Home Team Goals Scored**",
                    min_value=0,
                    max_value=150,
                    value=45,
                    help="Total goals scored by home team this season"
                )
                
                away_scored = st.number_input(
                    "**Away Team Goals Scored**",
                    min_value=0,
                    max_value=150,
                    value=35,
                    help="Total goals scored by away team this season"
                )
                
                home_conceded = st.number_input(
                    "**Home Team Goals Conceded**",
                    min_value=0,
                    max_value=150,
                    value=30,
help="Total goals conceded by home team this season"
                )
                
                submitted = st.form_submit_button("🔮 Predict Match Winner", use_container_width=True)
                
                if submitted:
                    features = {
                        'Points_Gap': points_gap,
                        'Goal_Difference_Gap': goal_diff_gap,
                        'Form_Gap': form_gap,
                        'Home_Goal_Difference': home_gd,
                        'Away_Goal_Difference': away_gd,
                        'Home_Win_Streak': home_streak,
                        'Away_Win_Streak': away_streak,
                        'Home_Goals_Scored': home_scored,
                        'Away_Goals_Scored': away_scored,
                        'Home_Goals_Conceded': home_conceded,
                    }
                    
                    st.session_state['match_features'] = features
                    st.session_state['home_team'] = "Home Team"
                    st.session_state['away_team'] = "Away Team"
                    st.session_state['prediction_mode'] = 'manual'
    
    with col_result:
        st.markdown("### 🎯 Match Prediction")
        
        if 'match_features' in st.session_state:
            try:
                features = st.session_state['match_features']
                home_team = st.session_state.get('home_team', 'Home')
                away_team = st.session_state.get('away_team', 'Away')
                
                # Load model
                with st.spinner("Loading model..."):
                    model = load_model("match_winner")
                
                # Prepare input
                feature_order = get_feature_order("match_winner")
                input_df = pd.DataFrame([features])[feature_order]
                
                # Make prediction
                with st.spinner("Analyzing match..."):
                    prediction = model.predict(input_df)[0]
                    
                    # Get probabilities if available
                    if hasattr(model, 'predict_proba'):
                        probabilities = model.predict_proba(input_df)[0]
                        # Assuming order: H, D, A or similar
                        class_labels = ['Home Win', 'Draw', 'Away Win']
                        
                        # Create probability chart
                        fig = go.Figure(data=[
                            go.Bar(
                                x=class_labels,
                                y=probabilities * 100,
                                marker=dict(
                                    color=['#22c55e', '#fbbf24', '#ef4444'],
                                    line=dict(color='rgba(255, 255, 255, 0.2)', width=2)
                                ),
                                text=[f'{p*100:.1f}%' for p in probabilities],
                                textposition='auto',
                            )
                        ])
                        
                        fig.update_layout(
                            title="Match Outcome Probabilities",
                            yaxis_title="Probability (%)",
                            template="plotly_dark",
                            height=350,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Determine prediction based on highest probability
                        max_idx = np.argmax(probabilities)
                        predicted_outcome = class_labels[max_idx]
                        confidence = probabilities[max_idx] * 100
                    else:
                        # Fallback if no probabilities
                        outcomes = {0: 'Home Win', 1: 'Draw', 2: 'Away Win'}
                        predicted_outcome = outcomes.get(prediction, 'Unknown')
                        confidence = 66  # Model accuracy
                
                # Display prediction
                if 'Home' in predicted_outcome:
                    color = "#22c55e"
                    icon = "🏠"
                    result_text = f"{home_team} Wins"
                elif 'Draw' in predicted_outcome:
                    color = "#fbbf24"
                    icon = "⚖️"
                    result_text = "Match Drawn"
                else:
                    color = "#ef4444"
                    icon = "✈️"
                    result_text = f"{away_team} Wins"
                
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, {color} 0%, {color}dd 100%);
                     color: white; padding: 32px; border-radius: 16px; text-align: center;
                     box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);'>
                    <h2 style='margin: 0;'>{icon} PREDICTED OUTCOME</h2>
                    <h1 style='font-size: 3rem; margin: 20px 0;'>{result_text}</h1>
                    <p style='font-size: 1.2rem; opacity: 0.9;'>Confidence: {confidence:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Feature summary
                st.markdown("### 📋 Match Statistics")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Points Gap", features['Points_Gap'])
                    st.metric("Home Goal Diff", features['Home_Goal_Difference'])
                    st.metric("Home Win Streak", features['Home_Win_Streak'])
                
                with col2:
                    st.metric("Form Gap", features['Form_Gap'])
                    st.metric("Away Goal Diff", features['Away_Goal_Difference'])
                    st.metric("Away Win Streak", features['Away_Win_Streak'])
                
            except Exception as e:
                st.error(f"❌ Prediction Error: {str(e)}")
                st.exception(e)
        else:
            st.info("👈 Fill in the match details and click **Predict** to see results")
            
            st.markdown("### 💡 Tip")
            st.markdown("""
            <div style='background: rgba(56, 189, 248, 0.1); padding: 16px; border-radius: 8px;'>
                <p><strong>For best results:</strong></p>
                <ul>
                    <li>Use current season statistics</li>
                    <li>Higher positive gaps favor home team</li>
                    <li>Win streaks significantly influence outcomes</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
