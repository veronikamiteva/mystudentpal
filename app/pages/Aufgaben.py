import streamlit as st
import pandas as pd
import calendar
from datetime import datetime, date, timedelta

# ====== Set FULL PAGE before any Streamlit commands ======
st.set_page_config(layout="wide")

# ====== Start Login Block ======
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# Initialize managers
data_manager = DataManager(fs_protocol="webdav", fs_root_folder="MyStudentPal_DB")
login_manager = LoginManager(data_manager)
login_manager.login_register()
# ====== End Login Block ======

# --- Remove padding and spacing ---
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-left: 0rem;
        padding-right: 0rem;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 0rem !important;
    }
    .tooltip {
        position: relative;
        cursor: default;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 220px;
        background-color: #1e1e1e;
        color: #fff;
        text-align: left;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -110px;
        opacity: 0;
        transition: opacity 0.3s;
        border: 1px solid #ccc;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
""", unsafe_allow_html=True)

# --- Load or initialize Tasks ---
tasks_schema = ["Titel", "Fälligkeitsdatum", "Beschreibung"]

data_manager.load_user_data(
    session_state_key='aufgaben_df',
    file_name='aufgaben.csv',
    initial_value=pd.DataFrame(columns=tasks_schema)
)

aufgaben_df = st.session_state["aufgaben_df"]

# --- Normalize Dates ---
if not aufgaben_df.empty:
    aufgaben_df['Fälligkeitsdatum'] = pd.to_datetime(aufgaben_df['Fälligkeitsdatum']).dt.date

# --- Add Assignment Dialog ---
@st.dialog("➕ Neue Aufgabe hinzufügen")
def add_task_dialog():
    st.subheader("Neue Aufgabe erstellen")
    with st.form("task_form"):
        title = st.text_input("Aufgabentitel")
        due_date = st.date_input("Fälligkeitsdatum", min_value=date.today())
        description = st.text_area("Beschreibung (optional)")
        save_task = st.form_submit_button("Aufgabe speichern")

        if save_task:
            if title:
                data_manager.append_record(
                    session_state_key='aufgaben_df',
                    record_dict={
                        "Titel": title,
                        "Fälligkeitsdatum": due_date,
                        "Beschreibung": description
                    }
                )
                st.success(f"Aufgabe '{title}' hinzugefügt!")
                st.rerun()
            else:
                st.error("Bitte gib einen Aufgabentitel ein.")

# --- Main Interface ---
st.title("📅 Assignment Deadline Tracker")

if st.button("➕ Neue Aufgabe"):
    add_task_dialog()

# Select month/year
today = date.today()
selected_month = st.selectbox("Monat auswählen", list(calendar.month_name)[1:], index=today.month - 1)
selected_year = st.number_input("Jahr auswählen", min_value=2023, max_value=2100, value=today.year, step=1)

st.subheader(f"{selected_month} {selected_year}")

# Build calendar
month_number = list(calendar.month_name).index(selected_month)
month_calendar = calendar.monthcalendar(selected_year, month_number)

# Days Header
day_labels = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
cols = st.columns(7)
for idx, day_label in enumerate(day_labels):
    with cols[idx]:
        st.markdown(f"<div style='text-align: center; font-weight: bold;'>{day_label}</div>", unsafe_allow_html=True)

st.markdown("---")

# Calendar Weeks
for week in month_calendar:
    cols = st.columns(7)
    for idx, day in enumerate(week):
        with cols[idx]:
            if day != 0:
                day_date = date(selected_year, month_number, day)
                day_tasks = aufgaben_df[aufgaben_df['Fälligkeitsdatum'] == day_date]

                task_buttons_html = ""
                for i, task in day_tasks.iterrows():
                    tooltip_text = task['Beschreibung'] or "Keine Beschreibung"
                    task_buttons_html += f"<div class='tooltip' style='font-size: 0.75em; margin-top: 4px;'>📝 {task['Titel']}<span class='tooltiptext'><strong>Fälligkeit:</strong> {task['Fälligkeitsdatum'].strftime('%d.%m.%Y')}<br><strong>Beschreibung:</strong> {tooltip_text}</span></div>"

                st.markdown(f"""
                    <div style="
                        border: 1px solid #aaaaaa;
                        border-radius: 0px;
                        padding: 6px;
                        min-height: 120px;
                        background-color: #1e1e1e;
                        display: flex;
                        flex-direction: column;
                        justify-content: flex-start;
                        position: relative;
                    ">
                        <div style="text-align: right; font-weight: bold;">{day}</div>
                        <div style="text-align: left;">{task_buttons_html}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style='border: 1px solid transparent; padding: 6px; min-height: 120px;'></div>
                """, unsafe_allow_html=True)

