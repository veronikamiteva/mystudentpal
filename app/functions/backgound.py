from pathlib import Path
import base64
import time
import streamlit as st
from streamlit_theme import st_theme

@st.dialog("Loading...")
def spinner():
    with st.spinner("Loading Data..."):
        time.sleep(3)  # simulate some loading

def encoder(wallpaper, pathDepth):
    wallpaper_path = Path(__file__).resolve().parents[pathDepth] / "assets" / wallpaper
    with open(wallpaper_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    return encoded

def set_wallpaper(wallpaper, pathDepth):

    encoded = encoder(wallpaper, pathDepth)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-position: right;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )    
def set_background_theme(pathDepth):
    theme = st_theme()
    if theme and theme['base'] == "dark":
        bg = "#21283cff"
       # bg = '#333334'
        text = "white"
        border = "#a1a7b6"
        wallpaper = "msp-bg.png"
        set_wallpaper(wallpaper, pathDepth)
        return bg, text, border

    elif theme and theme['base'] == "light":
        bg = "#f0f2f6"
        text = "black"
        border = "#c1c1c1"
        wallpaper = "msp-bg-light.png"
        set_wallpaper(wallpaper, pathDepth)
        return bg, text, border
    else:
        spinner()
    
    
    return bg, text, border

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
    
