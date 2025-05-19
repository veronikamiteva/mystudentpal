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
import time
from datetime import datetime
from streamlit_theme import st_theme
from utils import helpers  # you can remove if no longer needed
from pathlib import Path
from functions.backgound import set_background_theme, render_sidebar_logo

bg, text = set_background_theme(pathDepth=2)
render_sidebar_logo(pathDepth=2)

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

modulen_df = st.session_state["modulen_df"]

if not modulen_df.empty:
    st.subheader("Existing Modules")

    # Allow deletion only via UI (no add/edit, no custom buttons)
    edited_df = st.data_editor(
        modulen_df,             # disables editing of cells
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic" ,
        disabled={
            "Modul": True,     # read-only
            "ECTS": True,      # read-only
            "Semester": True   # read-only
        }
    )

    # Detect if rows were deleted via trash icon
    if len(edited_df) < len(modulen_df):
        deleted_modules = set(modulen_df["Modul"]) - set(edited_df["Modul"])
        st.session_state["modulen_df"] = edited_df.reset_index(drop=True)
        data_manager.update_user_data("modulen_df")

        # Also delete from bewertungen_df
        if "bewertungen_df" in st.session_state:
            bewertungen_df = st.session_state["bewertungen_df"]
            bewertungen_df = bewertungen_df[~bewertungen_df["Modul"].isin(deleted_modules)]
            st.session_state["bewertungen_df"] = bewertungen_df
            data_manager.update_user_data("bewertungen_df")
       
        st.rerun()
else:
    st.info("Noch keine Module hinzugefügt.")
