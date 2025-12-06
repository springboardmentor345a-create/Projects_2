import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from models import problem5_logic

# Page config
st.set_page_config(
    page_title="ScoreSight - Total Points Prediction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Session state
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False
if 'team_data' not in st.session_state:
    st.session_state.team_data = {}

# --------------------- CSS ---------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@400;500;600;700&display=swap');

#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top:0 !important; padding-bottom:0 !important; max-width:100% !important;}

/* Prediction Form Styles */
.prediction-container {max-width:1400px; margin:0 auto; padding:2rem;}
.prediction-header {text-align:center; margin-bottom:3rem;}
.prediction-header h1 {font-family:'Orbitron',sans-serif; font-size:clamp(2.5rem,5vw,4rem); font-weight:900; background:linear-gradient(to right,#3b82f6,#8b5cf6,#06b6d4); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:1rem;}
.prediction-header p {font-size:1.25rem; color:#94a3b8; max-width:600px; margin:0 auto;}
.input-section {background:linear-gradient(135deg, rgba(30,41,59,0.8), rgba(15,23,42,0.8)); border-radius:1.5rem; padding:2.5rem; border:1px solid rgba(139,92,246,0.3); margin-bottom:3rem;}
.input-grid {display:grid; grid-template-columns:repeat(3,1fr); gap:2rem;}
.input-card {background:rgba(255,255,255,0.05); padding:1.5rem; border-radius:1rem; border:1px solid rgba(255,255,255,0.1); transition:all 0.3s ease;}
.input-card:hover {border-color:rgba(139,92,246,0.5); transform:translateY(-2px);}
.input-label {font-family:'Inter',sans-serif; font-weight:600; color:#e2e8f0; margin-bottom:0.75rem; font-size:1.1rem; display:flex; align-items:center; gap:0.5rem;}
.input-number {width:100%; padding:0.75rem; border-radius:0.5rem; border:1px solid rgba(255,255,255,0.2); background:rgba(0,0,0,0.3); color:white; font-size:1rem;}
.predict-button {display:block; margin:2rem auto 0; padding:1.25rem 3rem !important; font-size:1.25rem !important; font-weight:700 !important; background:linear-gradient(to right,#3b82f6,#8b5cf6) !important; border:none !important; border-radius:0.75rem !important;}

/* Result Section */
.result-section {background:linear-gradient(135deg, rgba(30,41,59,0.95), rgba(15,23,42,0.95)); border-radius:1.5rem; padding:3rem; border:1px solid rgba(139,92,246,0.3); margin-top:3rem; animation:fadeIn 0.8s ease-out;}
.result-card {text-align:center; padding:2rem; background:linear-gradient(135deg, rgba(59,130,246,0.1), rgba(139,92,246,0.1)); border-radius:1rem; margin-bottom:3rem;}
.points-badge {font-size:5rem; animation:glow 2s ease-in-out infinite alternate; margin-bottom:1rem;}
.points-text {font-family:'Orbitron',sans-serif; font-size:3rem; font-weight:900; background:linear-gradient(to right,#10b981,#3b82f6); -webkit-background-clip:text; -webkit-text-fill-color:transparent;}
.stats-grid {display:grid; grid-template-columns:repeat(3,1fr); gap:1.5rem; margin-bottom:3rem;}
.stat-card {background:rgba(255,255,255,0.05); padding:1.5rem; border-radius:1rem; text-align:center; border:1px solid rgba(255,255,255,0.1);}
.stat-value {font-family:'Orbitron',sans-serif; font-size=2.5rem; font-weight:700; color:#3b82f6; margin-bottom:0.5rem;}
.stat-label {color:#94a3b8; font-size:0.9rem; text-transform:uppercase; letter-spacing:0.05em;}
.viz-section {margin-top:3rem;}
.viz-title {font-family:'Inter',sans-serif; font-size:1.5rem; font-weight:700; color:#e2e8f0; margin-bottom:2rem; text-align:center;}

/* Animations */
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
@keyframes glow {
    from {filter: drop-shadow(0 0 10px rgba(59,130,246,0.5));}
    to {filter: drop-shadow(0 0 25px rgba(59,130,246,0.9));}
}

/* Points Bar */
.points-container {margin:3rem 0; padding:2rem; background:rgba(15,23,42,0.8); border-radius:1rem; border:1px solid rgba(139,92,246,0.3);}
.points-bar {width:100%; height:60px; background:rgba(255,255,255,0.1); border-radius:30px; overflow:hidden; position:relative; margin-top:1rem;}
.points-fill {height:100%; border-radius:30px; transition:width 1.5s ease-in-out;}
.points-text-display {position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-family:'Orbitron',sans-serif; font-size:1.5rem; font-weight:700; color:white; text-shadow:0 2px 4px rgba(0,0,0,0.5);}

/* Goal Difference Warning */
.gd-warning {background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.3); padding:0.75rem; border-radius:0.5rem; margin-top:0.5rem;}
.gd-warning-text {color:#f59e0b; font-size:0.85rem;}

</style>
""", unsafe_allow_html=True)

def create_points_bar(predicted_points):
    """Create animated points bar"""
    # Determine color based on points
    if predicted_points >= 80:
        color = "#10b981"  # Champion
    elif predicted_points >= 70:
        color = "#3b82f6"  # Top 4
    elif predicted_points >= 60:
        color = "#f59e0b"  # Mid-table
    else:
        color = "#ef4444"  # Relegation
    
    percentage = min(100, (predicted_points / 100) * 100)
    
    st.markdown(f"""
    <div class="points-container">
        <div class="points-bar">
            <div class="points-fill" style="width:{percentage}%; background:linear-gradient(90deg, {color}, {color}dd);"></div>
            <div class="points-text-display">{predicted_points} Points</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_points_chart(predicted_points):
    """Create simple bar chart for points prediction"""
    categories = ['Relegation', 'Mid-table', 'Europe', 'Top 4', 'Champion']
    ranges = [(0, 40), (40, 60), (60, 70), (70, 80), (80, 100)]
    colors = ['#ef4444', '#f59e0b', '#8b5cf6', '#3b82f6', '#10b981']
    
    # Determine which category the prediction falls into
    bar_values = []
    for low, high in ranges:
        if low <= predicted_points <= high:
            bar_values.append(predicted_points)
        else:
            bar_values.append((low + high) / 2)
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=bar_values,
            marker_color=colors,
            text=[f"{predicted_points} pts" if low <= predicted_points <= high else "" for (low, high) in ranges],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Predicted Points Range",
        title_font=dict(size=24, color='white'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(
            tickfont=dict(size=14),
            title="Position"
        ),
        yaxis=dict(
            title="Points",
            range=[0, 100],
            gridcolor='rgba(255,255,255,0.1)'
        ),
        height=400
    )
    
    return fig

def calculate_predicted_points(goals_scored, goals_conceded, goal_diff):
    """Simple calculation for predicted points"""
    # Base calculation
    points = 50
    
    # Adjust based on goal difference
    if goal_diff > 0:
        points += goal_diff * 0.5
    elif goal_diff < 0:
        points += goal_diff * 0.3
    
    # Adjust based on goals
    points += goals_scored * 0.2
    points -= goals_conceded * 0.15
    
    # Ensure realistic range
    points = max(0, min(100, round(points)))
    
    return points

def total_points_prediction():
    """Total Points Prediction - SIMPLE VERSION"""
    
    st.markdown('<div class="prediction-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="prediction-header">
        <h1>📊 Total Points Prediction</h1>
        <p>Predict total points based on goal statistics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input Section - ONLY 3 INPUTS
    with st.container():
        st.markdown("""
        <div class="input-section">
            <h2 style="color:#e2e8f0; font-family:'Inter',sans-serif; margin-bottom:2rem;">⚽ Input Goal Statistics</h2>
        """, unsafe_allow_html=True)
        
        # Create 3 columns for the 3 inputs
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="input-card">', unsafe_allow_html=True)
            st.markdown('<div class="input-header">Goals Scored</div>', unsafe_allow_html=True)
            
            goals_scored = st.number_input(
                "Goals Scored",
                min_value=0,
                value=45,
                key="goals_scored",
                label_visibility="collapsed"
            )
            
            st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem;">
                <div style="font-size: 2.5rem; color: #10b981; font-family: 'Orbitron';">
                    {goals_scored}
                </div>
                <div style="color: #94a3b8; font-size: 0.9rem;">
                    Total goals
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="input-card">', unsafe_allow_html=True)
            st.markdown('<div class="input-header">Goals Conceded</div>', unsafe_allow_html=True)
            
            goals_conceded = st.number_input(
                "Goals Conceded",
                min_value=0,
                value=30,
                key="goals_conceded",
                label_visibility="collapsed"
            )
            
            st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem;">
                <div style="font-size: 2.5rem; color: #ef4444; font-family: 'Orbitron';">
                    {goals_conceded}
                </div>
                <div style="color: #94a3b8; font-size: 0.9rem;">
                    Total conceded
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="input-card">', unsafe_allow_html=True)
            st.markdown('<div class="input-header">Goal Difference</div>', unsafe_allow_html=True)
            
            # Calculate goal difference automatically
            goal_diff_calculated = goals_scored - goals_conceded
            
            goal_diff = st.number_input(
                "Goal Difference",
                value=goal_diff_calculated,
                key="goal_diff",
                label_visibility="collapsed"
            )
            
            # Show warning if mismatch
            if goal_diff != goal_diff_calculated:
                st.markdown(f"""
                <div class="gd-warning">
                    <div class="gd-warning-text">
                        ⚠️ Note: GD should be {goal_diff_calculated} (GS {goals_scored} - GC {goals_conceded})
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="text-align: center; margin-top: 1rem;">
                <div style="font-size: 2.5rem; color: #3b82f6; font-family: 'Orbitron';">
                    {goal_diff:+}
                </div>
                <div style="color: #94a3b8; font-size: 0.9rem;">
                    Goal difference
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Predict Button
        st.markdown('<div style="text-align: center; margin-top: 2rem;">', unsafe_allow_html=True)
        if st.button("Predict Total Points", 
                    type="primary",
                    use_container_width=False,
                    key="predict_btn"):
            
            # Calculate predicted points
            predicted_points = calculate_predicted_points(goals_scored, goals_conceded, goal_diff)
            
            # Try to use model if available
            try:
                user_input_df = pd.DataFrame([{
                    "Goals_Scored": goals_scored,
                    "Goals_Conceded": goals_conceded,
                    "Goal_Diff": goal_diff
                }])
                
                result = problem5_logic(user_input_df)
                
                # Extract prediction from model
                if isinstance(result, pd.DataFrame) and not result.empty:
                    model_result = result.iloc[0, 0]
                    if isinstance(model_result, (int, float)):
                        predicted_points = int(model_result)
                    else:
                        # Try to extract number from string
                        try:
                            predicted_points = int(float(str(model_result)))
                        except:
                            pass
                elif isinstance(result, (int, float)):
                    predicted_points = int(result)
                    
            except Exception as e:
                st.warning(f"Using calculated prediction (model error: {str(e)[:50]}...)")
            
            # Store data
            st.session_state.team_data = {
                'goals_scored': goals_scored,
                'goals_conceded': goals_conceded,
                'goal_diff': goal_diff,
                'predicted_points': predicted_points
            }
            
            st.session_state.prediction_made = True
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)  # Close input-section
    
    # Show Results
    if st.session_state.prediction_made:
        team_data = st.session_state.team_data
        predicted_points = team_data['predicted_points']
        
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        
        # Display result
        st.markdown(f"""
        <div class="result-card">
            <div class="points-badge">📊</div>
            <div class="points-text">
                {predicted_points} POINTS
            </div>
            <p style="color:#94a3b8; font-size:1.25rem; margin-top:1rem;">
                Predicted total points at season end
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Points bar
        create_points_bar(predicted_points)
        
        # Stats grid
        st.markdown("""
        <div style="text-align:center; margin:2rem 0;">
            <h3 style="color:#e2e8f0; font-family:'Inter',sans-serif;">Input Statistics</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{team_data['goals_scored']}</div>
                <div class="stat-label">Goals Scored</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{team_data['goals_conceded']}</div>
                <div class="stat-label">Goals Conceded</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{team_data['goal_diff']:+}</div>
                <div class="stat-label">Goal Difference</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Chart
        st.markdown('<div class="viz-section">', unsafe_allow_html=True)
        fig = create_points_chart(predicted_points)
        st.plotly_chart(fig, use_container_width=True)
        
        # Simple analysis
        if predicted_points >= 80:
            position = "Champion/title challenge 🏆"
            color = "#10b981"
        elif predicted_points >= 70:
            position = "Top 4 (Champions League) 🔵"
            color = "#3b82f6"
        elif predicted_points >= 60:
            position = "European qualification 🟣"
            color = "#8b5cf6"
        elif predicted_points >= 40:
            position = "Mid-table 🟠"
            color = "#f59e0b"
        else:
            position = "Relegation battle 🔴"
            color = "#ef4444"
        
        st.markdown(f"""
        <div style="margin-top: 2rem; padding: 2rem; background: rgba(30,41,59,0.5); border-radius: 1rem; text-align: center;">
            <div style="color: {color}; font-family: 'Inter'; font-size: 1.5rem; font-weight: 700; margin-bottom: 1rem;">
                Expected Finish: {position}
            </div>
            <div style="color: #94a3b8; font-size: 1.1rem; line-height: 1.6;">
                Based on your goal statistics ({team_data['goals_scored']} GS, {team_data['goals_conceded']} GC, GD {team_data['goal_diff']:+}), 
                your team is projected to finish with <strong>{predicted_points} points</strong>.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close result-section
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close prediction-container

# --------------------- MAIN ---------------------
if __name__ == "__main__":
    total_points_prediction()