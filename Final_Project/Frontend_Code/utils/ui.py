import streamlit as st
from pathlib import Path

def load_css():
    """Loads the global custom CSS."""
    css_path = Path(__file__).parent.parent / "style.css"
    if css_path.exists():
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def futuristic_card(title, value, subtext="", color="cyan", delay_class=""):
    """
    Creates a futuristic metric card.
    
    Args:
        title (str): The title of the card.
        value (str/int): The main value to display.
        subtext (str): Optional subtext.
        color (str): 'cyan', 'purple', or 'green' for neon accent.
        delay_class (str): Optional delay class for animation (e.g., 'delay-100').
    """
    colors = {
        "cyan": "#00f3ff",
        "purple": "#bc13fe",
        "green": "#0aff0a"
    }
    accent = colors.get(color, "#00f3ff")
    
    html = f"""
    <div class="metric-card animate-slide-up {delay_class}" style="border-color: {accent}40;">
        <h3 style="color: #e0e0e0;">{title}</h3>
        <h1 style="margin: 10px 0; font-size: 3rem; color: {accent}; text-shadow: 0 0 20px {accent}40;">{value}</h1>
        <p style="margin: 0; color: #a0a0a0; font-size: 0.9rem;">{subtext}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def futuristic_divider():
    """Creates a glowing futuristic divider."""
    st.markdown('<div class="futuristic-divider animate-fade-in"></div>', unsafe_allow_html=True)

def logo_container(image_path):
    """Creates a centered, glowing logo container."""
    # Using st.image inside a styled div for better control
    st.markdown('<div class="logo-container animate-fade-in">', unsafe_allow_html=True)
    st.image(image_path, width=150)
    st.markdown('</div>', unsafe_allow_html=True)

def futuristic_header(text):
    """Creates a glowing futuristic header."""
    html = f"""
    <h1 class="animate-fade-in" style="
        text-align: center; 
        font-size: 3.5rem; 
        margin-bottom: 1rem;
    ">{text}</h1>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_loading_overlay(placeholder):
    """
    Renders a full-screen football loading animation (V2) in the given placeholder.
    Includes a bouncing ball, shadow, and cycling text.
    
    Args:
        placeholder: Streamlit placeholder object (st.empty())
    """
    html = """
    <div class="loading-overlay">
        <div class="loading-content">
            <div class="football-container">
                <div class="football-bounce">⚽</div>
                <div class="football-shadow"></div>
            </div>
            <div class="loading-text" id="loading-text">Analyzing Match Data...</div>
        </div>
    </div>
    <script>
        const texts = [
            "Consulting VAR...",
            "Measuring Grass Height...",
            "Checking Wind Speed...",
            "Asking the Referee...",
            "Predicting the Unpredictable...",
            "Calculating xG...",
            "Warming Up the GPU..."
        ];
        let index = 0;
        const textElement = document.getElementById("loading-text");
        
        // Simple text cycler
        if (textElement) {
            setInterval(() => {
                index = (index + 1) % texts.length;
                textElement.innerText = texts[index];
            }, 800);
        }
    </script>
    """
    placeholder.markdown(html, unsafe_allow_html=True)
