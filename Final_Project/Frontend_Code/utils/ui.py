import streamlit as st
from pathlib import Path

def load_css():
    """Loads the global custom CSS."""
    css_path = Path(__file__).parent.parent / "style.css"
    if css_path.exists():
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def futuristic_card(title, value, subtext="", color="cyan"):
    """
    Creates a futuristic metric card.
    
    Args:
        title (str): The title of the card.
        value (str/int): The main value to display.
        subtext (str): Optional subtext.
        color (str): 'cyan', 'purple', or 'green' for neon accent.
    """
    colors = {
        "cyan": "#00f3ff",
        "purple": "#bc13fe",
        "green": "#0aff0a"
    }
    accent = colors.get(color, "#00f3ff")
    
    html = f"""
    <div class="metric-card" style="border-color: {accent}40;">
        <h3 style="margin: 0; color: #e0e0e0; font-size: 1rem; text-transform: uppercase; letter-spacing: 2px;">{title}</h3>
        <h1 style="margin: 10px 0; font-size: 3rem; color: {accent}; text-shadow: 0 0 20px {accent}40;">{value}</h1>
        <p style="margin: 0; color: #a0a0a0; font-size: 0.9rem;">{subtext}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def futuristic_divider():
    """Creates a glowing futuristic divider."""
    st.markdown('<div class="futuristic-divider"></div>', unsafe_allow_html=True)

def logo_container(image_path):
    """Creates a centered, glowing logo container."""
    html = f"""
    <div class="logo-container">
        <img src="data:image/jpg;base64,{image_path}" class="logo-img" width="150">
    </div>
    """
    # Note: For local files in Streamlit, simple <img> tags with paths might not work directly without base64 encoding or serving static files.
    # A safer approach for Streamlit is using st.image with custom CSS wrapper, or just relying on st.image but wrapping it in a div.
    # Let's use a simpler wrapper that works with st.image
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image(image_path, width=150)
    st.markdown('</div>', unsafe_allow_html=True)

def futuristic_header(text):
    """Creates a glowing futuristic header."""
    html = f"""
    <h1 style="
        text-align: center; 
        font-size: 3.5rem; 
        background: linear-gradient(180deg, #fff, #888);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(0, 243, 255, 0.3);
        margin-bottom: 1rem;
    ">{text}</h1>
    """
    st.markdown(html, unsafe_allow_html=True)
