import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import streamlit.components.v1 as components
import json
import os

# ============================================================================
# Page config
# ============================================================================

st.set_page_config(
    page_title="ScoreSight Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS Styling
# ============================================================================

css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* { font-family: 'Rajdhani', sans-serif; }
h1, h2, h3 { font-family: 'Poppins', sans-serif; font-weight: 700; }

.main-title {
    text-align: center;
    background: linear-gradient(135deg, #00FF85 0%, #FFD700 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3.8rem;
    text-shadow: 0 0 30px rgba(0, 255, 133, 0.4);
    font-weight: 900;
    margin-bottom: 0.5rem;
    letter-spacing: 4px;
}

.subtitle {
    text-align: center;
    color: #FFD700;
    font-size: 1.4rem;
    letter-spacing: 4px;
    font-weight: 700;
    text-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
    margin-bottom: 2rem;
}

.page-header {
    background: linear-gradient(135deg, #00FF85 0%, #64FF9E 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    border-bottom: 3px solid #00FF85;
    padding-bottom: 1.2rem;
    margin-bottom: 2rem;
    font-size: 2.8rem;
    letter-spacing: 2px;
}

.card-container {
    background: linear-gradient(135deg, rgba(0, 255, 133, 0.15), rgba(255, 215, 0, 0.10));
    border-left: 6px solid #00FF85;
    border-radius: 15px;
    padding: 2.2rem;
    margin: 1.5rem 0;
    box-shadow: 0 8px 25px rgba(0, 255, 133, 0.12);
    transition: all 0.4s;
    border: 1px solid rgba(0, 255, 133, 0.2);
}

.card-container:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 40px rgba(0, 255, 133, 0.25);
}

.prediction-card {
    background: linear-gradient(135deg, rgba(0, 255, 133, 0.15), rgba(255, 215, 0, 0.10));
    border: 2px solid #00FF85;
    border-radius: 15px;
    padding: 2.5rem;
    text-align: center;
    margin: 1.5rem 0;
    box-shadow: 0 8px 30px rgba(0, 255, 133, 0.20);
}

.prediction-card h3 {
    color: #FFD700;
    font-size: 3rem;
    margin: 0.5rem 0;
    text-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
}

/* Animations */
@keyframes shimmer {
    0% { background-position: -500px 0; }
    100% { background-position: 500px 0; }
}

@keyframes pulse {
    0% { transform: scale(1); opacity: 0.9; }
    50% { transform: scale(1.06); opacity: 1; }
    100% { transform: scale(1); opacity: 0.95; }
}

.main-title {
        animation: pulse 3s ease-in-out infinite;
}

.page-header {
        animation: shimmer 6s linear infinite;
        background: linear-gradient(90deg, #00FF85 0%, #FFD700 50%, #64FF9E 100%);
        background-size: 1000px 100%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
}

.prediction-card h3 {
        animation: pulse 2s ease-in-out infinite;
}

.team-card {
    background: linear-gradient(135deg, rgba(100, 200, 255, 0.12), rgba(100, 150, 255, 0.08));
    border-left: 5px solid #64C8FF;
    border-radius: 12px;
    padding: 1.8rem;
    margin: 1rem 0;
    border: 1px solid rgba(100, 200, 255, 0.2);
}

div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #00FF85 0%, #00DD70 100%) !important;
    color: #000 !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    padding: 1rem 2rem !important;
    border-radius: 10px !important;
    border: none !important;
    transition: all 0.3s !important;
    box-shadow: 0 6px 20px rgba(0, 255, 133, 0.3) !important;
}

div[data-testid="stButton"] > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 30px rgba(0, 255, 133, 0.5) !important;
}

[data-testid="metric-container"] {
    background: linear-gradient(135deg, rgba(0, 255, 133, 0.1), rgba(255, 215, 0, 0.08));
    border-radius: 12px;
    padding: 1.5rem;
    border: 1px solid rgba(0, 255, 133, 0.2);
}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

# ============================================================================
# Load Models
# ============================================================================
@st.cache_resource
def load_models():
    try:
        # 1. Get the path to the current file (Frontend/app.py)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 2. Construct the path to the Backend folder (Sibling directory)
        #    ".." means go up one level
        backend_dir = os.path.join(current_dir, '..', 'Backend')
        
        # 3. Load all models using the backend_dir path
        models = {
            'match': joblib.load(os.path.join(backend_dir, 'match_winner_model.pkl')),
            'league_class': joblib.load(os.path.join(backend_dir, 'league_class_model.pkl')),
            'league_points': joblib.load(os.path.join(backend_dir, 'league_points_model.pkl')),
            'goals': joblib.load(os.path.join(backend_dir, 'player_goals_model.pkl')),
            'assists': joblib.load(os.path.join(backend_dir, 'player_assists_model.pkl'))
        }
        return models
        
    except FileNotFoundError as e:
        st.error(f"Critical Error: Model file not found.")
        st.error(str(e))
        # Debug helper to show where it was looking
        st.code(f"Looking in: {os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Backend'))}")
        return None

# ============================================================================
# Sidebar Navigation
# ============================================================================

st.sidebar.markdown("<h1 style='color: #00FF85; text-align: center; font-size: 2rem;'>SCORESIGHT ANALYTICS</h1>", unsafe_allow_html=True)
st.sidebar.markdown("---")

models = load_models()
if models is None:
    st.error("Models not loaded!")
    st.stop()

if 'page_nav' not in st.session_state:
    st.session_state.page_nav = "Home"

nav_pages = [
    "Home",
    "Goals Predicted",
    "Assists Predicted",
    "League Winner",
    "Match Winner",
    "Total Points"
]


# Custom sidebar navigation (selectbox)
def render_sidebar_nav(pages, default='Home'):
    st.sidebar.markdown("<div style='text-align:center; font-weight:800; color:#00FF85; margin-bottom:6px;'>NAVIGATION</div>", unsafe_allow_html=True)
    icons = {
        'Home': '🏠',
        'Goals Predicted': '⚽',
        'Assists Predicted': '🅰️',
        'League Winner': '🏆',
        'Match Winner': '🔮',
        'Total Points': '📈'
    }

    # Use a selectbox for navigation
    current = st.session_state.get('page_nav', default)
    labeled_pages = [f"{icons.get(p,'')}  {p}" for p in pages]
    current_idx = 0
    for i, p in enumerate(pages):
        if p == current:
            current_idx = i
            break
    
    def on_page_change():
        selected_label = st.session_state.page_selector
        selected_page = selected_label.split("  ", 1)[1] if "  " in selected_label else selected_label
        st.session_state.page_nav = selected_page
    
    st.sidebar.selectbox("Select Page", labeled_pages, index=current_idx, key="page_selector", on_change=on_page_change)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"<div style='color:#888;text-align:center;'>Current: <strong style='color:#00FF85'>{current}</strong></div>", unsafe_allow_html=True)
    return st.session_state.page_nav


# Render custom nav and set `page`
page = render_sidebar_nav(nav_pages)

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='text-align: center; color: #888; font-size: 0.85rem;'>Powered by Machine Learning</p>", unsafe_allow_html=True)

# ============================================================================
# Helper Functions
# ============================================================================

def get_expected_input_columns(model):
    if hasattr(model, "feature_names_in_"):
        return list(model.feature_names_in_)
    if hasattr(model, "named_steps") and "preprocessor" in model.named_steps:
        pre = model.named_steps["preprocessor"]
        if hasattr(pre, "feature_names_in_"):
            return list(pre.feature_names_in_)
    return None

def prepare_input_for_model(model, input_df):
    expected = get_expected_input_columns(model)
    df = input_df.copy()
    if expected is None:
        return df
    missing = [c for c in expected if c not in df.columns]
    for col in missing:
        df[col] = np.nan
    df = df[expected]
    return df





def animated_counter(value, title=None, suffix=""):
        """Render a small animated counter using an embedded HTML snippet."""
        # sanitize
        try:
                num = int(round(float(value)))
        except Exception:
                num = value

        html = """
        <div style="text-align:center;padding:6px 0;">
            <div style="font-size:0.9rem;color:#64FF9E;font-weight:700;margin-bottom:6px;">__TITLE__</div>
            <div id="count" style="font-size:3.4rem;font-weight:900;color:#FFD700;">0__SUFFIX__</div>
        </div>
        <script>
            const target = __NUM__;
            const suffix = '__SUFFIX__';
            const el = document.getElementById('count');
            let current = 0;
            const step = Math.max(1, Math.round(target / 60));
            const intv = setInterval(function(){
                current += step;
                if (current >= target) { current = target; el.innerText = current + suffix; clearInterval(intv); }
                else { el.innerText = current + suffix; }
            }, 16);
        </script>
        """
        html = html.replace('__NUM__', str(num)).replace('__TITLE__', str(title or '')).replace('__SUFFIX__', str(suffix))
        # components.html runs in an iframe so document access is local
        components.html(html, height=120)

# ============================================================================
# PAGE: HOME
# ============================================================================

def render_home():
    st.markdown("<h1 class='main-title'>SCORESIGHT ANALYTICS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Football Prediction Engine</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    html = "<div class='card-container'>"
    html += "<h3 style='color: #00FF85; margin-top: 0;'>Welcome</h3>"
    html += "<p>Advanced ML models for football prediction. Choose a prediction type from the menu.</p>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
    
    st.markdown("### Available Predictions")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        html = "<div class='card-container'><h4>Goals Prediction</h4>"
        html += "<p>Predict player goals scored in matches.</p></div>"
        st.markdown(html, unsafe_allow_html=True)
        if st.button("Go to Goals", key='btn_goals', use_container_width=True):
            st.session_state.page_nav = "Goals Predicted"
            st.rerun()
    
    with col2:
        html = "<div class='card-container'><h4>Assists Prediction</h4>"
        html += "<p>Forecast player assists.</p></div>"
        st.markdown(html, unsafe_allow_html=True)
        if st.button("Go to Assists", key='btn_assists', use_container_width=True):
            st.session_state.page_nav = "Assists Predicted"
            st.rerun()
    
    with col3:
        html = "<div class='card-container'><h4>League Winner</h4>"
        html += "<p>Predict league champions.</p></div>"
        st.markdown(html, unsafe_allow_html=True)
        if st.button("Go to League", key='btn_league', use_container_width=True):
            st.session_state.page_nav = "League Winner"
            st.rerun()
    
    col4, col5, col6 = st.columns(3)
    with col4:
        html = "<div class='card-container'><h4>Match Winner</h4>"
        html += "<p>Predict match outcomes.</p></div>"
        st.markdown(html, unsafe_allow_html=True)
        if st.button("Go to Match", key='btn_match', use_container_width=True):
            st.session_state.page_nav = "Match Winner"
            st.rerun()
    
    with col5:
        html = "<div class='card-container'><h4>Total Points</h4>"
        html += "<p>Forecast season points.</p></div>"
        st.markdown(html, unsafe_allow_html=True)
        if st.button("Go to Points", key='btn_points', use_container_width=True):
            st.session_state.page_nav = "Total Points"
            st.rerun()
    
    with col6:
        html = "<div class='card-container'><h4>How to Use</h4>"
        html += "<p>Use the menu to select predictions.</p></div>"
        st.markdown(html, unsafe_allow_html=True)

# ============================================================================
# PAGE: GOALS
# ============================================================================

def render_goals():
    st.markdown("<h1 class='page-header'>Goals Prediction</h1>", unsafe_allow_html=True)
    
    with st.form("goals_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            position = st.selectbox("Position", ["Forward", "Midfielder", "Defender"], key='goals_pos')
            age = st.number_input("Age", 16, 50, 25, key='goals_age')
            matches = st.number_input("Matches", 0, 100, 10, key='goals_m')
        with col2:
            starts = st.number_input("Starts", 0, 100, 8, key='goals_s')
            minutes = st.number_input("Minutes", 0, 5000, 720, key='goals_min')
            nineties = st.number_input("90s", 0.0, 100.0, 8.0, key='goals_n')
        with col3:
            goals_90 = st.number_input("Goals/90", 0.0, 5.0, 0.5, key='goals_g90')
            assists_90 = st.number_input("Assists/90", 0.0, 2.0, 0.2, key='goals_a90')
            xg_90 = st.number_input("xG/90", 0.0, 2.0, 0.3, key='goals_xg90')
        
        if st.form_submit_button("Predict Goals", use_container_width=True):
            try:
                input_df = pd.DataFrame({
                    'Position': [position],
                    'Age': [age],
                    'Matches Played': [matches],
                    'Starts': [starts],
                    'Minutes': [minutes],
                    '90s Played': [nineties],
                    'Goals Per 90': [goals_90],
                    'Assists Per 90': [assists_90],
                    'xG Per 90': [xg_90],
                    'xAG Per 90': [0.1],
                    'Non-Penalty Goals Per 90': [goals_90 * 0.8]
                })
                
                with st.spinner("Analyzing..."):
                    prep_df = prepare_input_for_model(models['goals'], input_df)
                    pred = models['goals'].predict(prep_df)[0]
                    pred_int = int(round(float(pred)))
                    
                    animated_counter(pred_int, title='Predicted Goals')
                    
                    st.info(f"Based on {position}, age {age}: ~{pred_int} goals predicted")
            except Exception as e:
                st.error(f"Error: {e}")

# ============================================================================
# PAGE: ASSISTS
# ============================================================================

def render_assists():
    st.markdown("<h1 class='page-header'>Assists Prediction</h1>", unsafe_allow_html=True)
    
    with st.form("assists_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            position = st.selectbox("Position", ["Forward", "Midfielder", "Defender"], key='asst_pos')
            age = st.number_input("Age", 16, 50, 26, key='asst_age')
            matches = st.number_input("Matches", 0, 100, 12, key='asst_m')
        with col2:
            starts = st.number_input("Starts", 0, 100, 10, key='asst_s')
            minutes = st.number_input("Minutes", 0, 5000, 900, key='asst_min')
            nineties = st.number_input("90s", 0.0, 100.0, 10.0, key='asst_n')
        with col3:
            goals_90 = st.number_input("Goals/90", 0.0, 2.0, 0.3, key='asst_g90')
            assists_90 = st.number_input("Assists/90", 0.0, 2.0, 0.3, key='asst_a90')
            xag_90 = st.number_input("xAG/90", 0.0, 2.0, 0.2, key='asst_xag90')
        
        if st.form_submit_button("Predict Assists", use_container_width=True):
            try:
                input_df = pd.DataFrame({
                    'Position': [position],
                    'Age': [age],
                    'Matches Played': [matches],
                    'Starts': [starts],
                    'Minutes': [minutes],
                    '90s Played': [nineties],
                    'Goals Per 90': [goals_90],
                    'Assists Per 90': [assists_90],
                    'xAG Per 90': [xag_90],
                    'Non-Penalty Goals Per 90': [goals_90 * 0.8],
                    'npxG Per 90': [0.25]
                })
                
                with st.spinner("Analyzing..."):

                    prep_df = prepare_input_for_model(models['assists'], input_df)
                    pred = models['assists'].predict(prep_df)[0]
                    pred_int = int(round(float(pred)))

                    animated_counter(pred_int, title='Predicted Assists')

                    st.info(f"Based on {position}, age {age}: ~{pred_int} assists predicted")
            except Exception as e:
                st.error(f"Error: {e}")

# ============================================================================
# PAGE: LEAGUE
# ============================================================================

def render_league():
    st.markdown("<h1 class='page-header'>League Winner Prediction</h1>", unsafe_allow_html=True)
    
    tabs = st.tabs(["Champion", "Points"])
    
    with tabs[0]:
        with st.form("league_champ_form"):
            col1, col2 = st.columns(2)
            with col1:
                wins = st.number_input("Wins", 0, 40, 20, key='champ_w')
                draws = st.number_input("Draws", 0, 20, 5, key='champ_d')
                losses = st.number_input("Losses", 0, 20, 13, key='champ_l')
            with col2:
                gf = st.number_input("Goals For", 0, 150, 65, key='champ_gf')
                ga = st.number_input("Goals Against", 0, 150, 35, key='champ_ga')
            
            if st.form_submit_button("Predict Champion", use_container_width=True):
                try:
                    gd = gf - ga
                    input_df = pd.DataFrame({
                        'wins': [wins], 'draws': [draws], 'losses': [losses],
                        'goals_scored': [gf], 'goals_conceded': [ga],
                        'goal_difference': [gd]
                    })
                    prep_df = prepare_input_for_model(models['league_class'], input_df)
                    pred = models['league_class'].predict(prep_df)[0]

                    if pred == 1:
                        st.success(f"CHAMPION! Record: {wins}W-{draws}D-{losses}L, GD: +{gd}")
                    else:
                        st.warning(f"Not Champion. Record: {wins}W-{draws}D-{losses}L, GD: +{gd}")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tabs[1]:
        with st.form("league_pts_form"):
            col1, col2 = st.columns(2)
            with col1:
                wins = st.number_input("Wins", 0, 40, 18, key='pts_w')
                draws = st.number_input("Draws", 0, 20, 7, key='pts_d')
                losses = st.number_input("Losses", 0, 20, 13, key='pts_l')
            with col2:
                gf = st.number_input("Goals For", 0, 150, 60, key='pts_gf')
                ga = st.number_input("Goals Against", 0, 150, 40, key='pts_ga')
            
            if st.form_submit_button("Predict Points", use_container_width=True):
                try:
                    gd = gf - ga
                    input_df = pd.DataFrame({
                        'wins': [wins], 'draws': [draws], 'losses': [losses],
                        'goals_scored': [gf], 'goals_conceded': [ga],
                        'goal_difference': [gd]
                    })
                    prep_df = prepare_input_for_model(models['league_points'], input_df)
                    pred = models['league_points'].predict(prep_df)[0]

                    animated_counter(int(round(float(pred))), title='Predicted Points', suffix=' PTS')

                    base = wins * 3 + draws
                    st.metric("Base Points", base)
                    st.metric("Predicted", f"{pred:.0f}")
                except Exception as e:
                    st.error(f"Error: {e}")

# ============================================================================
# PAGE: MATCH
# ============================================================================

def render_match():
    st.markdown("<h1 class='page-header'>Match Winner Prediction</h1>", unsafe_allow_html=True)
    
    with st.form("match_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='team-card'><h3>Home Team</h3>", unsafe_allow_html=True)
            htgs = st.number_input("Home Goals For", 0, 10, 2, key='m_htgf')
            htgc = st.number_input("Home Goals Against", 0, 10, 1, key='m_htga')
            htp = st.number_input("Home Points", 0.0, 50.0, 5.0, key='m_htp')
            with st.expander("Last 5 Matches (Home)", expanded=False):
                hm1 = st.selectbox("M1", ["W", "D", "L"], key='m_hm1')
                hm2 = st.selectbox("M2", ["W", "D", "L"], key='m_hm2', index=1)
                hm3 = st.selectbox("M3", ["W", "D", "L"], key='m_hm3', index=1)
                hm4 = st.selectbox("M4", ["W", "D", "L"], key='m_hm4')
                hm5 = st.selectbox("M5", ["W", "D", "L"], key='m_hm5')
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='team-card' style='border-left-color: #FF6B9D;'><h3>Away Team</h3>", unsafe_allow_html=True)
            atgs = st.number_input("Away Goals For", 0, 10, 1, key='m_atgf')
            atgc = st.number_input("Away Goals Against", 0, 10, 2, key='m_atga')
            atp = st.number_input("Away Points", 0.0, 50.0, 2.0, key='m_atp')
            with st.expander("Last 5 Matches (Away)", expanded=False):
                am1 = st.selectbox("M1", ["W", "D", "L"], key='m_am1', index=1)
                am2 = st.selectbox("M2", ["W", "D", "L"], key='m_am2', index=1)
                am3 = st.selectbox("M3", ["W", "D", "L"], key='m_am3', index=2)
                am4 = st.selectbox("M4", ["W", "D", "L"], key='m_am4', index=1)
                am5 = st.selectbox("M5", ["W", "D", "L"], key='m_am5', index=2)
            st.markdown("</div>", unsafe_allow_html=True)
        
        if st.form_submit_button("Predict Match", use_container_width=True):
                try:
                    def pts(r):
                        return {'W': 3, 'D': 1, 'L': 0}.get(r, 0)
                    
                    h_form = pts(hm1) + pts(hm2) + pts(hm3) + pts(hm4) + pts(hm5)
                    a_form = pts(am1) + pts(am2) + pts(am3) + pts(am4) + pts(am5)
                    
                    input_df = pd.DataFrame({
                        'HTGS': [htgs], 'ATGS': [atgs],
                        'HTGC': [htgc], 'ATGC': [atgc],
                        'HTP': [htp], 'ATP': [atp],
                        'HM1': [hm1], 'HM2': [hm2], 'HM3': [hm3], 'HM4': [hm4], 'HM5': [hm5],
                        'AM1': [am1], 'AM2': [am2], 'AM3': [am3], 'AM4': [am4], 'AM5': [am5],
                        'HTGD': [htgs - htgc], 'ATGD': [atgs - atgc],
                        'DiffPts': [htp - atp], 'DiffFormPts': [h_form - a_form]
                    })
                    
                    prep_df = prepare_input_for_model(models['match'], input_df)

                    with st.expander("Debug: Match input / prepared / model", expanded=False):
                        st.write("Raw input_df:")
                        st.write(input_df)
                        st.write("Prepared df sent to model:")
                        st.write(prep_df)
                        st.write("Model expected features:")
                        st.write(get_expected_input_columns(models['match']))

                    pred = models['match'].predict(prep_df)[0]
                    conf = models['match'].predict_proba(prep_df)[0]
                    
                    if pred == 1:
                        st.success(f"HOME WIN! Confidence: {conf[1]*100:.1f}%")
                        # animated confidence
                        try:
                            animated_counter(conf[1]*100, title='Home Win Confidence', suffix='%')
                        except Exception:
                            pass
                    else:
                        st.warning(f"AWAY/DRAW. Confidence: {conf[0]*100:.1f}%")
                        try:
                            animated_counter(conf[0]*100, title='Away/Draw Confidence', suffix='%')
                        except Exception:
                            pass
                except Exception as e:
                    st.error(f"Error: {e}")

# ============================================================================
# PAGE: POINTS
# ============================================================================

def render_points():
    st.markdown("<h1 class='page-header'>Total Points Prediction</h1>", unsafe_allow_html=True)
    
    with st.form("points_form"):
        col1, col2 = st.columns(2)
        with col1:
            wins = st.number_input("Wins", 0, 40, 22, key='tp_w')
            draws = st.number_input("Draws", 0, 20, 6, key='tp_d')
            losses = st.number_input("Losses", 0, 20, 10, key='tp_l')
        with col2:
            gf = st.number_input("Goals For", 0, 150, 70, key='tp_gf')
            ga = st.number_input("Goals Against", 0, 150, 38, key='tp_ga')
        
        if st.form_submit_button("Predict Total Points", use_container_width=True):
            try:
                gd = gf - ga
                input_df = pd.DataFrame({
                    'wins': [wins], 'draws': [draws], 'losses': [losses],
                    'goals_scored': [gf], 'goals_conceded': [ga],
                    'goal_difference': [gd]
                })
                
                prep_df = prepare_input_for_model(models['league_points'], input_df)
                pred = models['league_points'].predict(prep_df)[0]
                
                html = "<div class='prediction-card'>"
                html += f"<h3>{pred:.0f} PTS</h3>"
                html += "<p>Predicted Season Points</p></div>"
                st.markdown(html, unsafe_allow_html=True)
                
                base = wins * 3 + draws
                st.metric("Record", f"{wins}W-{draws}D-{losses}L")
                st.metric("Base Points", base)
                st.metric("Predicted", f"{pred:.0f}")
            except Exception as e:
                st.error(f"Error: {e}")

# ============================================================================
# ROUTER
# ============================================================================

if page == "Home":
    render_home()
elif page == "Goals Predicted":
    render_goals()
elif page == "Assists Predicted":
    render_assists()
elif page == "League Winner":
    render_league()
elif page == "Match Winner":
    render_match()
elif page == "Total Points":
    render_points()
