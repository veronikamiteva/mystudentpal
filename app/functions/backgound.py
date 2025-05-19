from pathlib import Path
import base64
import time
import streamlit as st
from streamlit_theme import st_theme


@st.dialog("Loading...")
def spinner():
    with st.spinner():
        time.sleep(1) 

def set_background_theme(pathDepth):
    theme = st_theme()
    if theme and theme['base'] == "dark":
        bg = "#1e1e1e"
        text = "white"
        wallpaper = "msp-bg.png"
    elif theme and theme['base'] == "light":
        bg = "#f5f5f5"
        text = "black"
        wallpaper = "msp-bg-light.png"
    else:
        spinner()

    wallpaper_path = Path(__file__).resolve().parents[pathDepth] / "assets" / wallpaper
    with open(wallpaper_path, "rb") as image_file:
        encoded1 = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded1}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position-x: 310px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    return bg, text



def render_sidebar_logo(pathDepth):
    logo_path = Path(__file__).resolve().parents[pathDepth] / "assets" / "logo-msp.png"
    with open(logo_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    logo_html = f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{encoded}" width="150">
        </div>
    """
    st.sidebar.markdown(logo_html, unsafe_allow_html=True)
    