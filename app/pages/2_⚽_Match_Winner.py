"""
Match Winner Prediction Page
Predict Home/Draw/Away outcome
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.model_loader import load_model, get_feature_order
from utils.data_loader import load_match_winner_data, get_unique_teams, get_team_stats, calculate_match_features
from utils.ui import load_css

# Page config
st.set_page_config(page_title="Match Winner | ScoreSight", page_icon="⚽", layout="wide")

# Load Global CSS
load_css()

def main():
    # Back Button
    st.page_link("main.py", label="Back to Home", icon="🏠")
    
    # Page Image
    img_path = Path("app/image/matchwinner.jpg")
    if img_path.exists():
        _, col_img, _ = st.columns([1, 2, 1])
        with col_img:
            st.image(str(img_path), use_container_width=True)
    
    # Header
    st.markdown("# ⚽ Match Winner Prediction")
    st.markdown("### Predict the outcome of a match between two teams")
    
    st.markdown("---")
    
    # Load data
    try:
        df = load_match_winner_data()
        teams = get_unique_teams("match_winner")
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return

    # Create tabs for different input modes
    tab1, tab2 = st.tabs(["🤖 Team Selection (Auto)", "✍️ Manual Input"])
    
    input_data = {}
    
    with tab1:
        st.markdown("### Select Teams")
        col1, col2 = st.columns(2)
        
        with col1:
            home_team = st.selectbox("Home Team", teams, index=0)
        with col2:
            away_team = st.selectbox("Away Team", teams, index=1)
            
        if home_team == away_team:
            st.warning("Please select different teams for Home and Away.")
        else:
            # Calculate features automatically
            if st.button("Generate Match Stats"):
                try:
                    with st.spinner("Calculating team stats..."):
                        features = calculate_match_features(home_team, away_team, df)
                        st.session_state['match_features'] = features
                        st.success("Stats calculated successfully!")
                except Exception as e:
                    st.error(f"Error calculating stats: {str(e)}")
                    
        # Use calculated features if available
        if 'match_features' in st.session_state:
            input_data = st.session_state['match_features']
            
            # Show calculated stats
            st.markdown("### 📊 Calculated Match Stats")
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.metric("Points Gap", f"{input_data.get('Points_Gap', 0):.1f}")
                st.metric("Goal Diff Gap", f"{input_data.get('Goal_Difference_Gap', 0):.1f}")
            with col_s2:
                st.metric("Home Win Streak", int(input_data.get('Home_Win_Streak', 0)))
                st.metric("Away Win Streak", int(input_data.get('Away_Win_Streak', 0)))
            with col_s3:
                st.metric("Home Goals Scored", int(input_data.get('Home_Goals_Scored', 0)))
                st.metric("Away Goals Scored", int(input_data.get('Away_Goals_Scored', 0)))

    with tab2:
        st.markdown("### Manual Feature Input")
        with st.form("manual_match_form"):
            col_m1, col_m2 = st.columns(2)
            
            with col_m1:
                points_gap = st.number_input("Points Gap (Home - Away)", value=0.0)
                gd_gap = st.number_input("Goal Difference Gap", value=0.0)
                form_gap = st.number_input("Form Gap", value=0.0)
                home_gd = st.number_input("Home Goal Difference", value=0.0)
                away_gd = st.number_input("Away Goal Difference", value=0.0)
                
            with col_m2:
                home_streak = st.number_input("Home Win Streak", value=0, min_value=0)
                away_streak = st.number_input("Away Win Streak", value=0, min_value=0)
                home_scored = st.number_input("Home Goals Scored", value=0, min_value=0)
                away_scored = st.number_input("Away Goals Scored", value=0, min_value=0)
                home_conceded = st.number_input("Home Goals Conceded", value=0, min_value=0)
                
            submitted = st.form_submit_button("Set Manual Stats")
            
            if submitted:
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
                st.session_state['match_features'] = input_data

    st.markdown("---")
    
    # Prediction Section
    if input_data:
        col_pred, col_viz = st.columns([1, 2])
        
        with col_pred:
            st.markdown("### 🔮 Prediction")
            if st.button("Predict Match Winner", use_container_width=True):
                try:
                    with st.spinner("Analyzing match-up..."):
                        model = load_model("match_winner")
                        feature_order = get_feature_order("match_winner")
                        
                        # Prepare dataframe
                        input_df = pd.DataFrame([input_data])[feature_order]
                        
                        # Predict
                        probabilities = model.predict_proba(input_df)[0]
                        
                        # Model is binary: 0=H (Home Win), 1=NH (Not Home Win)
                        # Based on alphabetical sorting of classes ['H', 'NH']
                        
                        probs = {
                            "Home Win": probabilities[0],
                            "Not Home Win (Draw/Away)": probabilities[1]
                        }
                        
                        # Find winner
                        winner = max(probs, key=probs.get)
                        confidence = probs[winner] * 100
                        
                        # Display Result
                        st.markdown(f"""
                        <div class="metric-card" style="text-align: center;">
                            <h2 style="margin:0;">{winner}</h2>
                            <h1 style="font-size: 3rem; color: #38bdf8;">{confidence:.1f}%</h1>
                            <p>Probability</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Store for visualization
                        st.session_state['probs'] = probs
                        
                except Exception as e:
                    st.error(f"Prediction Error: {str(e)}")
        
        with col_viz:
            if 'probs' in st.session_state:
                st.markdown("### 📊 Probability Distribution")
                probs = st.session_state['probs']
                
                # Create Plotly Chart
                fig = go.Figure(data=[
                    go.Bar(
                        x=list(probs.keys()),
                        y=[v*100 for v in probs.values()],
                        marker_color=['#22c55e', '#ef4444'], # Green (Home), Red (Not Home)
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
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
