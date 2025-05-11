# ====== Start Login Block ======
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Initialize managers
# uses WebDAV backend to persist data
data_manager = DataManager(fs_protocol="webdav", fs_root_folder="MyStudentPal_DB")
login_manager = LoginManager(data_manager)
login_manager.login_register()
# ====== End Login Block ======

import streamlit as st
import pandas as pd
import numpy as np
import base64
from datetime import datetime
from streamlit_theme import st_theme
from utils import helpers  # you can remove if no longer needed
from pathlib import Path

# Build absolute path reliably
logo_path = Path(__file__).resolve().parent.parent / "assets" / "logo-msp.png"

with open(logo_path, "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode()

# Create the HTML for the image
logo_html = f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{encoded}" width="150">
    </div>
"""

# Display the logo in the sidebar
st.sidebar.markdown(logo_html, unsafe_allow_html=True)

theme = st_theme() # or your st_theme() function

# Provide a fallback if theme is None
if theme and theme['base'] == "dark":
    bg = "#1e1e1e"
    text = "white"
elif theme and theme['base'] == "light":
    bg = "#f5f5f5"
    text = "black"
else:
    # Fallback if theme is not yet available
    bg = "#e0e0e0"  # Light gray
    text = "#202020"  # Very dark gray

data_manager.load_user_data(
    session_state_key='modulen_df',
    file_name='modulen.csv',
    initial_value=pd.DataFrame(columns=["Modul", "ECTS", "Semester"])
)

@st.dialog("Modul hinzufügen")
def course_dialog():
    st.subheader('Modul hinzufügen')
    with st.form('course_form'):
        course_name = st.text_input('Modulname')
        credits = st.number_input('ECTS-Punkte', min_value=0.5, step=0.5, format='%.1f')
        semester = st.text_input('Semester (optional)')
        add_course = st.form_submit_button('Modul hinzufügen')
        
        if add_course:
            if course_name and course_name not in st.session_state["modulen_df"]['Modul'].values:
                data_manager.append_record(
                    session_state_key='modulen_df',
                    record_dict={'Modul': course_name, 'ECTS': credits, 'Semester': semester}
                )
                st.success(f'Modul "{course_name}" hinzugefügt.')
                st.rerun()
            else:
                st.error('Ungültiger oder doppelter Modulname.')

# Main interface
st.title("📚 Modulmanager")
st.divider()


# Form inside box
with st.form("add"):
    # Layout inside the box
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<p style="color: {text}; font-size: 16px; margin-top: 8px;">Neue Modul hinzufügen</p>', unsafe_allow_html=True)
    with col2:
        if st.form_submit_button("➕ Neue Modul"):
            course_dialog()

# Display existing courses
if not st.session_state["modulen_df"].empty:
    st.dataframe(st.session_state["modulen_df"])
else:
    st.info("Noch keine Module hinzugefügt.")
