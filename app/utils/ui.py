import streamlit as st
from pathlib import Path

def load_css():
    """Loads the global custom CSS."""
    css_path = Path("app/style.css")
    if css_path.exists():
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # Fallback CSS if file is missing
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f8fafc;
        }
        </style>
        """, unsafe_allow_html=True)
