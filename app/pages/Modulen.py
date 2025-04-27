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
from datetime import datetime
from utils import helpers  # you can remove if no longer needed

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

if st.button("Modul hinzufügen"):
    course_dialog()

# Display existing courses
if not st.session_state["modulen_df"].empty:
    st.dataframe(st.session_state["modulen_df"])
else:
    st.info("Noch keine Module hinzugefügt.")
