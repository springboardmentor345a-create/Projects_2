"""
Top Scorer Prediction Page
Predict total goals for a player
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
from utils.data_loader import load_top_scorer_data

# Page config
st.set_page_config(page_title="Top Scorer | ScoreSight", page_icon="👟", layout="wide")

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
.golden-boot {
    background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
    color: white;
    padding: 32px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(251, 191, 36, 0.4);
}
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("# 👟 Top Scorer Prediction")
    st.markdown("### Predict total goals for a player based on performance metrics")
    
    # Model info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model Type", "XGBoost")
    with col2:
        st.metric("R² Score", "0.957")
    with col3:
        st.metric("MAE", "0.030 goals")
    
    st.markdown("---")
    
    # Create two columns
    col_input, col_result = st.columns([1, 1])
    
    with col_input:
        st.markdown("### 📊 Player Performance Metrics")
        st.markdown("*Enter the player's per-90-minute statistics*")
        
        with st.form("top_scorer_form"):
            # Note about per-90 stats
            st.info("💡 **Per-90 Stats:** All metrics are normalized to 90 minutes of play")
            
            goals_per_90 = st.number_input(
                "**Goals per 90** ⚽",
                min_value=0.0,
                max_value=3.0,
                value=0.65,
                step=0.01,
                format="%.2f",
                help="Average goals scored per 90 minutes"
            )
            
            assists_per_90 = st.number_input(
                "**Assists per 90** 🎯",
                min_value=0.0,
                max_value=3.0,
                value=0.25,
                step=0.01,
                format="%.2f",
                help="Average assists per 90 minutes"
            )
            
            xg_per_90 = st.number_input(
                "**Expected Goals (xG) per 90** 📈",
                min_value=0.0,
                max_value=3.0,
                value=0.70,
                step=0.01,
                format="%.2f",
                help="Expected goals based on shot quality per 90 minutes"
            )
            
            npxg_per_90 = st.number_input(
                "**Non-Penalty xG per 90** 🚫🎯",
                min_value=0.0,
                max_value=3.0,
                value=0.55,
                step=0.01,
                format="%.2f",
                help="Expected goals excluding penalties per 90 minutes"
            )
            
            xag_per_90 = st.number_input(
                "**Expected Assisted Goals (xAG) per 90** 🅰️",
                min_value=0.0,
                max_value=3.0,
                value=0.20,
                step=0.01,
                format="%.2f",
                help="Expected goals from assists per 90 minutes"
            )
            
            npxg_plus_xag_per_90 = st.number_input(
                "**Non-Penalty xG + xAG per 90** 🔥",
                min_value=0.0,
                max_value=5.0,
                value=0.75,
                step=0.01,
                format="%.2f",
                help="Combined non-penalty xG and xAG per 90 minutes"
            )
            
            # Additional context
            st.markdown("---")
            matches_played = st.number_input(
                "**Matches Played** (for context)",
                min_value=1,
                max_value=50,
                value=30,
                help="Number of matches played (used to calculate total goals)"
            )
            
            minutes_per_match = st.number_input(
                "**Average Minutes per Match**",
                min_value=1,
                max_value=90,
                value=85,
                help="Average minutes played per match"
            )
            
            submitted = st.form_submit_button("🔮 Predict Total Goals", use_container_width=True)
    
    with col_result:
        st.markdown("### 🎯 Goal Prediction")
        
        if submitted:
            try:
                # Load model
                with st.spinner("Loading model..."):
                    model = load_model("top_scorer")
                
                # Prepare input data
                feature_order = get_feature_order("top_scorer")
                
                # Calculate interaction features
                input_data = {
                    "goals_per_90": goals_per_90,
                    "goals_per_90 xg_per_90": goals_per_90 * xg_per_90,
                    "goals_per_90 npxg_per_90": goals_per_90 * npxg_per_90,
                    "goals_per_90 xag_per_90": goals_per_90 * xag_per_90,
                    "goals_per_90 npxg_plus_xag_per_90": goals_per_90 * npxg_plus_xag_per_90,
                    "goals_per_90 matches_played": goals_per_90 * matches_played,
                    "xg_per_90 matches_played": xg_per_90 * matches_played,
                    "npxg_per_90 matches_played": npxg_per_90 * matches_played
                }
                
                input_df = pd.DataFrame([input_data])[feature_order]
                
                # Make prediction
                with st.spinner("Analyzing player performance..."):
                    predicted_goals = model.predict(input_df)[0]
                    
                    # Calculate for full season
                    total_90s = (matches_played * minutes_per_match) / 90
                    season_goals = predicted_goals * total_90s
                
                # Display prediction
                st.markdown(f"""
                <div class="golden-boot">
                    <h2 style='margin: 0;'>⚽ PREDICTED GOALS</h2>
                    <h1 style='font-size: 5rem; margin: 20px 0;'>{season_goals:.0f}</h1>
                    <p style='font-size: 1.2rem; opacity: 0.9;'>Goals this season</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Additional metrics
                st.markdown("### 📊 Detailed Breakdown")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Goals per 90", f"{predicted_goals:.2f}")
                    st.metric("Goals per Match", f"{predicted_goals * (minutes_per_match/90):.2f}")
                    st.metric("Expected Season Goals", f"{season_goals:.0f}")
                
                with col2:
                    st.metric("xG per 90", f"{xg_per_90:.2f}")
                    st.metric("Finishing Efficiency", f"{(goals_per_90/max(xg_per_90, 0.01)*100):.1f}%")
                    st.metric("Total 90s Played", f"{total_90s:.1f}")
                
                # Performance analysis
                st.markdown("### 🔍 Performance Analysis")
                
                # Create radar chart
                categories = ['Goals/90', 'Assists/90', 'xG/90', 'npxG/90', 'xAG/90']
                values = [goals_per_90, assists_per_90, xg_per_90, npxg_per_90, xag_per_90]
                
                # Normalize to 0-1 scale for better visualization (max 1.5)
                max_val = 1.5
                normalized_values = [min(v/max_val, 1.0) * 100 for v in values]
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatterpolar(
                    r=normalized_values + [normalized_values[0]],  # Close the shape
                    theta=categories + [categories[0]],
                    fill='toself',
                    name='Player Stats',
                    line=dict(color='#38bdf8', width=2),
                    fillcolor='rgba(56, 189, 248, 0.3)'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100],
                            showticklabels=False
                        )
                    ),
                    showlegend=False,
                    template="plotly_dark",
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Insights
                if season_goals >= 20:
                    st.success("🏆 **Golden Boot Contender!** This player is on track for 20+ goals!")
                elif season_goals >= 15:
                    st.info("⭐ **Strong Scorer:** Upper-tier goal output expected")
                elif season_goals >= 10:
                    st.warning("📈 **Solid Contributor:** Double-digit goals expected")
                else:
                    st.info("🎯 **Development Stage:** Focus on improving finishing")
                
                # Compare to xG
                xg_season = xg_per_90 * total_90s
                overperformance = season_goals - xg_season
                
                if abs(overperformance) > 2:
                    if overperformance > 0:
                        st.success(f"📈 **Overperforming xG** by {overperformance:.1f} goals - Elite finishing!")
                    else:
                        st.warning(f"📉 **Underperforming xG** by {abs(overperformance):.1f} goals - Room for improvement")
                
            except Exception as e:
                st.error(f"❌ Prediction Error: {str(e)}")
                st.exception(e)
        else:
            st.info("👈 Fill in the player stats and click **Predict** to see results")
            
            st.markdown("### 💡 Example: Elite Striker")
            st.markdown("""
            <div style='background: rgba(56, 189, 248, 0.1); padding: 16px; border-radius: 8px;'>
                <ul style='line-height: 2;'>
                    <li><strong>Goals per 90:</strong> 0.6-0.9</li>
                    <li><strong>Assists per 90:</strong> 0.1-0.3</li>
                    <li><strong>xG per 90:</strong> 0.65-0.95</li>
                    <li><strong>npxG per 90:</strong> 0.5-0.8</li>
                    <li><strong>xAG per 90:</strong> 0.15-0.35</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
