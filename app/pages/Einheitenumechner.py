# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py')
# ====== End Login Block ======

import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils import helpers

st.title('🎓 Uni Grade Calculator')
st.markdown('Verwalte Kurse, Leistungen und berechne deinen gewichteten Notendurchschnitt.')

# --- Load or initialize courses metadata ---
courses_key = 'courses_df'
if courses_key not in st.session_state:
    st.session_state[courses_key] = DataManager().load_user_data(
        session_state_key=courses_key,
        file_name='courses.csv',
        initial_value=pd.DataFrame(columns=['course', 'credits'])
    )
courses_df = st.session_state[courses_key]

# Sidebar: Add or select course
st.sidebar.header('Kursverwaltung')
with st.sidebar.form('course_form'):
    new_course = st.text_input('Neuer Kursname')
    new_credits = st.number_input('Credits (ECTS)', min_value=1.0, step=0.5, format='%.1f')
    add_course = st.form_submit_button('Kurs hinzufügen')

if add_course and new_course:
    if new_course in courses_df['course'].values:
        st.sidebar.warning('Kurs bereits vorhanden.')
    else:
        DataManager().append_record(
            session_state_key=courses_key,
            record_dict={'course': new_course, 'credits': new_credits}
        )
        st.sidebar.success(f'Kurs {new_course} wurde hinzugefügt.')
        # refresh local df
        courses_df = st.session_state[courses_key]

# If no courses yet, prompt to add
if courses_df.empty:
    st.info('Bitte füge zuerst einen Kurs in der Seitenleiste hinzu.')
    st.stop()

# Select course for assessment entry
selected_course = st.selectbox('Kurs auswählen', courses_df['course'].tolist())
course_credits = float(courses_df.loc[courses_df['course']==selected_course, 'credits'].iloc[0])

# --- Load or initialize assessment records ---
records_key = 'grades_df'
if records_key not in st.session_state:
    st.session_state[records_key] = DataManager().load_user_data(
        session_state_key=records_key,
        file_name='grades.csv',
        initial_value=pd.DataFrame(columns=['course', 'credits', 'assessment', 'weight', 'grade', 'timestamp'])
    )
grades_df = st.session_state[records_key]

# Assessment entry
st.subheader('Leistung hinzufügen')
with st.form('assessment_form'):
    assessment_name = st.text_input('Bezeichnung der Leistung (z.B. Klausur, Mitarbeit)')
    weight = st.number_input('Anteil an der Endnote (%)', min_value=0.0, max_value=100.0, step=1.0, format='%.0f')
    grade = st.number_input('Note', min_value=1.0, max_value=6.0, step=0.1, format='%.1f')
    submit = st.form_submit_button('Leistung speichern')

if submit:
    if weight <= 0 or weight > 100:
        st.error('Gewicht muss zwischen 1 und 100 liegen.')
    else:
        rec = {
            'course': selected_course,
            'credits': course_credits,
            'assessment': assessment_name,
            'weight': weight,
            'grade': grade,
            'timestamp': helpers.ch_now(),
        }
        DataManager().append_record(session_state_key=records_key, record_dict=rec)
        st.success(f'Leistung für {selected_course} gespeichert.')
        grades_df = st.session_state[records_key]

# Display
st.subheader('Übersicht')
if grades_df.empty:
    st.info('Noch keine Leistungen erfasst.')
    st.stop()

# Group by course and compute final course grade
grouped = grades_df.groupby('course')
finals = []
for course, df in grouped:
    total_weight = df['weight'].sum()
    # normalize if weights don't sum to 100
    norm_factor = 100.0 / total_weight if total_weight != 100 else 1.0
    df['adj_weight'] = df['weight'] * norm_factor / 100.0
    course_final = (df['grade'] * df['adj_weight']).sum()
    credits = df['credits'].iloc[0]
    finals.append({'course': course, 'credits': credits, 'final_grade': round(course_final, 2)})

finals_df = pd.DataFrame(finals)

st.write('### Endnoten pro Kurs')
st.dataframe(finals_df)

# Overall GPA
total_credits = finals_df['credits'].sum()
weighted_sum = (finals_df['credits'] * finals_df['final_grade']).sum()
overall_gpa = weighted_sum / total_credits if total_credits else 0
st.metric('Gewichteter Notendurchschnitt (GPA)', f'{overall_gpa:.2f}')
