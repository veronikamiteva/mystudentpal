# ====== Start Login Block ======
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Initialize managers
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
from pathlib import Path
from functions.backgound import set_background_theme, render_sidebar_logo

bg, text = set_background_theme(2)
render_sidebar_logo(2)

# --- Load or initialize persistent data ---
courses_schema = ["Modul", "ECTS", "Semester"]
assess_schema = ['Modul', 'Bewertung', 'Gewichtung', 'Note', 'Zeitstempel']
settings_schema = ["Einstellung", "Wert"]

data_manager.load_user_data(
    session_state_key='modulen_df',
    file_name='modulen.csv',
    initial_value=pd.DataFrame(columns=courses_schema)
)

data_manager.load_user_data(
    session_state_key='bewertungen_df',
    file_name='bewertungen.csv',
    initial_value=pd.DataFrame(columns=assess_schema)
)

data_manager.load_user_data(
    session_state_key='einstellungen_df',
    file_name='einstellungen.csv',
    initial_value=pd.DataFrame(columns=settings_schema)
)

# --- Access loaded data ---
courses_df = st.session_state["modulen_df"]
assess_df = st.session_state["bewertungen_df"]
settings_df = st.session_state["einstellungen_df"]

# --- Helper function to get a setting value ---
def get_setting(name, default_value):
    if name in settings_df['Einstellung'].values:
        return settings_df.loc[settings_df['Einstellung'] == name, 'Wert'].values[0]
    else:
        return default_value

# --- Add Assessment Dialog ---
@st.dialog('Bewertung hinzufügen')
def assessment_dialog():
    st.subheader('Bewertung hinzufügen')
    
    if courses_df.empty:
        st.info("Bitte füge zuerst ein Modul hinzu, bevor du Bewertungen erstellst.")
        st.stop()
    
    with st.form('assessment_form'):
        selected = st.selectbox('Modul auswählen', courses_df['Modul'].tolist())
        name = st.text_input('Bewertungsname (e.g. Midterm, Teilnahme)')
        weight = st.number_input('Gewichtung (% der Modulnote)', min_value=0.0, max_value=100.0, step=1.0, format='%.0f')
        grade = st.number_input('Note', min_value=0.0, max_value=100.0, step=0.1, format='%.1f')
        save = st.form_submit_button('Bewertung speichern')
        
        if save:
            if name and 0 < weight <= 100:
                data_manager.append_record(
                    session_state_key='bewertungen_df',
                        record_dict={
                        'Modul': selected,
                        'Bewertung': name,
                        'Gewichtung': weight,
                        'Note': grade,
                        'Zeitstempel': datetime.now().date()
                    }
                )
                st.success('Bewertung erfasst')
                st.rerun()  
            else:
                st.error('Bitte gib einen gültigen Bewertungsnamen und eine gültige Gewichtung an.')

# --- Main interface ---
st.title("🧮 Notenrechner")
st.divider()

with st.form("add"):
    # Layout inside the box
    col1, col2 = st.columns([6, 2])
    with col1:
        st.markdown(f'<p style="color: {text}; font-size: 16px; margin-top: 8px;">Neue Bewertung hinzufügen</p>', unsafe_allow_html=True)
    with col2:
        if st.form_submit_button("➕ Neue Bewertung"):
            assessment_dialog()

# --- Overview & GPA Calculation ---
st.html(f"""
    <div style="background-color: {bg}; padding: 20px; border-radius: 12px; margin-bottom: 20px;">
        <h3 style="color: {text};">Übersicht & Durchschnitt</h3>
    </div>
""")

if assess_df.empty:
    st.info('Noch keine Bewertungen erfasst.')
else:
    # Allow deletion only via UI (no add/edit, no custom buttons)
    edited_df = st.data_editor(
        assess_df,             # disables editing of cells
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic" ,
        disabled={
            "Modul": True,     # read-only
            'Bewertung' : True,
            'Gewichtung' : True, 
            'Note': True,
            'Zeitstempel' : True
        }
    )

    # Detect if rows were deleted via trash icon
    if len(edited_df) < len(assess_df):
        # Identify deleted rows by comparing entire rows
        deleted_rows = pd.concat([assess_df, edited_df]).drop_duplicates(keep=False)

        st.session_state["bewertungen_df"] = edited_df.reset_index(drop=True)
        data_manager.update_user_data("bewertungen_df")
  
        st.rerun()

    # --- Calculation of final grades per course ---
    finals = []
    for course, group in assess_df.groupby('Modul'):
        weights = group['Gewichtung'].values
        grades = group['Note'].values

        if get_setting('gpa_method', 'Gewichteter Durchschnitt') == 'Gewichte normalisieren':
            norm = 100.0 / weights.sum() if weights.sum() else 1.0
            weights = weights * norm
        
        course_score = np.dot(grades, weights) / 100.0
        credits = float(courses_df.loc[courses_df['Modul'] == course, 'ECTS'].iloc[0])
        finals.append({
            'Modul': course,
            'ECTS': credits,
            'Endnote': round(course_score, 1)
        })

    finals_df = pd.DataFrame(finals)
    st.write('### Endnoten pro Modul')
    st.dataframe(finals_df)