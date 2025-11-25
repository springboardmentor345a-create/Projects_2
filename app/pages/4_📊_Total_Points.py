"""
Total Points Prediction Page
Predict team's total season points
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
from utils.data_loader import load_points_tally_data

# Page config
st.set_page_config(page_title="Total Points | ScoreSight", page_icon="📊", layout="wide")

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
    st.markdown("# 📊 Total Points Prediction")
    st.markdown("### Predict a team's final season points tally")
    
    # Model info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model Type", "Ridge Regression")
    with col2:
        st.metric("R² Score", "0.937")
    with col3:
        st.metric("MAE", "3.70 points")
    
    st.markdown("---")
    
    # Create two columns
    col_input, col_result = st.columns([1, 1])
    
    with col_input:
        st.markdown("### 📊 Team Season Statistics")
        st.markdown("*Enter the team's current season stats*")
        
        with st.form("total_points_form"):
            played = st.number_input(
                "**Matches Played** ⚽",
                min_value=1,
                max_value=38,
                value=20,
                help="Number of matches played so far"
            )
            
            gf = st.number_input(
                "**Goals For (GF)** ⚽",
                min_value=0,
                max_value=150,
                value=40,
                help="Total goals scored"
            )
            
            ga = st.number_input(
                "**Goals Against (GA)** 🥅",
                min_value=0,
                max_value=150,
                value=25,
                help="Total goals conceded"
            )
            
            gd = st.number_input(
                "**Goal Difference (GD)** 📈",
                min_value=-100,
                max_value=100,
                value=15,
                help="Goal difference (GF - GA)"
            )
            
            # Auto-calculate button
            if st.form_submit_button("Calculate GD from GF & GA", use_container_width=False):
                gd = gf - ga
                st.rerun()
            
            st.markdown("---")
            
            # Optional: Current points for comparison
            current_points = st.number_input(
                "**Current Points** (Optional - for comparison)",
                min_value=0,
                max_value=114,
                value=0,
                help="Current points tally (leave 0 if unknown)"
            )
            
            submitted = st.form_submit_button("🔮 Predict Final Points", use_container_width=True)
    
    with col_result:
        st.markdown("### 🎯 Points Prediction")
        
        if submitted:
            try:
                # Validate GD
                calculated_gd = gf - ga
                if abs(gd - calculated_gd) > 1:
                    st.warning(f"⚠️ Note: GD should be {calculated_gd} based on GF ({gf}) and GA ({ga})")
                
                # Load model
                with st.spinner("Loading model..."):
                    model = load_model("total_points")
                
                # Prepare input data
                feature_order = get_feature_order("total_points")
                input_data = {
                    "played": played,
                    "gf": gf,
                    "ga": ga,
                    "gd": gd
                }
                
                input_df = pd.DataFrame([input_data])[feature_order]
                
                # Make prediction
                with st.spinner("Calculating season projection..."):
                    predicted_points = model.predict(input_df)[0]
                    
                    # Round to nearest integer
                    predicted_points = round(predicted_points)
                
                # Determine tier
                if predicted_points >= 85:
                    color = "#22c55e"
                    tier = "🏆 TITLE CONTENDER"
                    message = "Champions League + Title Race"
                elif predicted_points >= 70:
                    color = "#38bdf8"
                    tier = "⭐ TOP 4"
                    message = "Champions League Qualification"
                elif predicted_points >= 60:
                    color = "#fbbf24"
                    tier = "🎯 EUROPEAN FOOTBALL"
                    message = "Europa League Qualification"
                elif predicted_points >= 45:
                    color = "#818cf8"
                    tier = "📊 MID-TABLE"
                    message = "Safe from relegation"
                else:
                    color = "#ef4444"
                    tier = "⚠️ RELEGATION BATTLE"
                    message = "Relegation concerns"
                
                # Display prediction
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, {color} 0%, {color}dd 100%);
                     color: white; padding: 32px; border-radius: 16px; text-align: center;
                     box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);'>
                    <h2 style='margin: 0;'>📊 PREDICTED FINAL POINTS</h2>
                    <h1 style='font-size: 5rem; margin: 20px 0; font-weight: 900;'>{predicted_points}</h1>
                    <h3 style='margin: 0; opacity: 0.9;'>{tier}</h3>
                    <p style='font-size: 1.1rem; opacity: 0.8; margin-top: 8px;'>{message}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Projection metrics
                st.markdown("### 📈 Season Projection")
                
                remaining_matches = 38 - played
                points_per_game = predicted_points / 38
                projected_remaining = points_per_game * remaining_matches
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Matches Remaining", remaining_matches)
                    st.metric("Points Per Game", f"{points_per_game:.2f}")
                
                with col2:
                    st.metric("Projected Points from Remaining", f"{projected_remaining:.0f}")
                    if current_points > 0:
                        st.metric("Current Points", current_points)
                
                with col3:
                    st.metric("Goals For (GF)", gf)
                    st.metric("Goals Against (GA)", ga)
                
                # Create points progression chart
                st.markdown("### 📉 Points Accumulation Projection")
                
                # Calculate projection
                matches_range = list(range(1, 39))
                cumulative_points = [points_per_game * m for m in matches_range]
                
                # Actual points so far (if provided)
                if current_points > 0:
                    actual_ppg = current_points / played
                    actual_cumulative = [actual_ppg * m for m in range(1, played + 1)]
                
                fig = go.Figure()
                
                # Projected line
                fig.add_trace(go.Scatter(
                    x=matches_range,
                    y=cumulative_points,
                    mode='lines',
                    name='Predicted Trajectory',
                    line=dict(color='#38bdf8', width=3),
                    fill='tozeroy',
                    fillcolor='rgba(56, 189, 248, 0.1)'
                ))
                
                # Actual line (if available)
                if current_points > 0:
                    fig.add_trace(go.Scatter(
                        x=list(range(1, played + 1)),
                        y=actual_cumulative,
                        mode='lines+markers',
                        name='Actual Progress',
                        line=dict(color='#22c55e', width=3),
                        marker=dict(size=6)
                    ))
                
                # Reference lines
                fig.add_hline(y=70, line_dash="dash", line_color="rgba(56, 189, 248, 0.5)", 
                             annotation_text="Top 4 (~70 pts)")
                fig.add_hline(y=85, line_dash="dash", line_color="rgba(34, 197, 94, 0.5)", 
                             annotation_text="Title Race (~85 pts)")
                
                fig.update_layout(
                    title="Season Points Projection",
                    xaxis_title="Matches Played",
                    yaxis_title="Cumulative Points",
                    template="plotly_dark",
                    height=450,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # League table position estimate
                st.markdown("### 🏆 Estimated League Position")
                
                if predicted_points >= 90:
                    position = "1st-2nd"
                    emoji = "🥇"
                elif predicted_points >= 80:
                    position = "2nd-4th"
                    emoji = "🥈"
                elif predicted_points >= 70:
                    position = "4th-6th"
                    emoji = "🥉"
                elif predicted_points >= 60:
                    position = "6th-10th"
                    emoji = "📊"
                elif predicted_points >= 50:
                    position = "10th-14th"
                    emoji = "📉"
                else:
                    position = "14th-20th"
                    emoji = "⚠️"
                
                st.markdown(f"""
                <div style='background: rgba(56, 189, 248, 0.1); padding: 24px; border-radius: 12px; text-align: center;'>
                    <h3 style='color: #38bdf8; margin: 0;'>Likely Final Position</h3>
                    <h1 style='font-size: 3rem; margin: 16px 0;'>{emoji} {position}</h1>
                </div>
                """, unsafe_allow_html=True)
                
                # Insights
                st.markdown("### 🔍 Key Insights")
                
                attack_rating = "Strong" if gf / played > 1.5 else "Average" if gf / played > 1.0 else "Weak"
                defense_rating = "Strong" if ga / played < 1.0 else "Average" if ga / played < 1.3 else "Weak"
                
                st.markdown(f"""
                <div style='background: rgba(56, 189, 248, 0.1); padding: 16px; border-radius: 8px;'>
                    <ul style='line-height: 2;'>
                        <li><strong>Attack:</strong> {attack_rating} ({gf/played:.1f} goals/match)</li>
                        <li><strong>Defense:</strong> {defense_rating} ({ga/played:.1f} conceded/match)</li>
                        <li><strong>Goal Difference:</strong> {gd:+d} ({gd/played:+.1f} per match)</li>
                        <li><strong>Points Needed per Match:</strong> {points_per_game:.2f}</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Prediction Error: {str(e)}")
                st.exception(e)
        else:
            st.info("👈 Fill in the team stats and click **Predict** to see results")
            
            st.markdown("### 💡 Example: Top 4 Team")
            st.markdown("""
            <div style='background: rgba(56, 189, 248, 0.1); padding: 16px; border-radius: 8px;'>
                <h4>Mid-Season Stats (20 matches)</h4>
                <ul style='line-height: 2;'>
                    <li><strong>Matches Played:</strong> 20</li>
                    <li><strong>Goals For:</strong> 40</li>
                    <li><strong>Goals Against:</strong> 25</li>
                    <li><strong>Goal Difference:</strong> +15</li>
                </ul>
                <p><em>Expected to finish with ~70+ points (Top 4)</em></p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
