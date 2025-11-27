"""
Total Points Prediction Page
Predict final season points
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.model_loader import load_model, get_feature_order

# Page config
st.set_page_config(page_title="Total Points | ScoreSight", page_icon="📊", layout="wide")

# Apply custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.main { background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%); }
.metric-card {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}
.stButton>button {
    background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 32px;
    font-weight: 600;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

def main():
    # Back Button
    st.page_link("main.py", label="Back to Home", icon="🏠")
    
    # Header
    st.markdown("# 📊 Total Points Prediction")
    st.markdown("### Estimate a team's final points tally for the season")
    
    st.markdown("---")
    
    col_input, col_viz = st.columns([1, 1])
    
    with col_input:
        st.markdown("### 📈 Current Season Stats")
        
        with st.form("total_points_form"):
            matches_played = st.number_input("Matches Played", 0, 38, 20)
            goals_scored = st.number_input("Goals Scored (GF)", 0, 150, 35)
            goals_conceded = st.number_input("Goals Conceded (GA)", 0, 150, 25)
            goal_diff = st.number_input("Goal Difference (GD)", -100, 100, 10)
            
            submitted = st.form_submit_button("🔮 Predict Final Points", use_container_width=True)
    
    with col_viz:
        if submitted:
            try:
                # Load model
                with st.spinner("Calculating projection..."):
                    model = load_model("total_points")
                
                # Prepare input data
                feature_order = get_feature_order("total_points")
                
                input_data = {
                    "played": matches_played,
                    "gf": goals_scored,
                    "ga": goals_conceded,
                    "gd": goal_diff
                }
                
                input_df = pd.DataFrame([input_data])[feature_order]
                
                # Predict
                predicted_points = model.predict(input_df)[0]
                
                # Display Result
                st.markdown(f"""
                <div class="metric-card" style="text-align: center; margin-top: 20px;">
                    <h2 style="margin:0; color: #f8fafc;">Projected Final Points</h2>
                    <h1 style="font-size: 5rem; margin: 10px 0; background: linear-gradient(90deg, #c084fc, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{int(predicted_points)}</h1>
                    <p style="opacity: 0.8;">After 38 Matches</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Simple trajectory visualization
                current_points = (predicted_points / 38) * matches_played # Rough estimate
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=[0, matches_played, 38],
                    y=[0, current_points, predicted_points],
                    mode='lines+markers',
                    name='Points Trajectory',
                    line=dict(color='#818cf8', width=4)
                ))
                
                fig.update_layout(
                    title="Projected Season Trajectory",
                    xaxis_title="Matches Played",
                    yaxis_title="Points",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white',
                    margin=dict(t=40, b=20, l=20, r=20),
                    height=300
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Prediction Error: {str(e)}")
        else:
            st.info("👈 Enter current team stats to project the final season tally.")

if __name__ == "__main__":
    main()
