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
import calendar
import base64
import time
from streamlit_theme import st_theme
from datetime import datetime, date, timedelta
from pathlib import Path
from functions.backgound import set_background_theme, render_sidebar_logo

# --- Style only calendar area (not selectboxes/titles) ---
st.html("""
    <style>
    .block-container {
        padding-left: 0rem;
        padding-right: 0rem;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 0rem !important;
    }
    .st-emotion {
        gap: 0 !important;
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
""")


# --- Load or initialize Tasks ---
tasks_schema = ["Titel", "Fälligkeitsdatum", "Beschreibung", "Priorität"]

data_manager.load_user_data(
    session_state_key='aufgaben_df',
    file_name='aufgaben.csv',
    initial_value=pd.DataFrame(columns=tasks_schema)
)

aufgaben_df = st.session_state["aufgaben_df"]

# --- Normalize Dates ---
if not aufgaben_df.empty:
    aufgaben_df['Fälligkeitsdatum'] = pd.to_datetime(aufgaben_df['Fälligkeitsdatum']).dt.date

if "Priorität" not in aufgaben_df.columns:
    aufgaben_df["Priorität"] = "Niedrig"  # Default value

bg, text = set_background_theme(2)

render_sidebar_logo(2)

# --- Add Assignment Dialog ---
@st.dialog("➕ Neue Aufgabe hinzufügen")
def add_task_dialog():
    st.subheader("Neue Aufgabe erstellen")
    with st.form("task_form"):
        title = st.text_input("Aufgabentitel")
        due_date = st.date_input("Fälligkeitsdatum", min_value=date.today())
        description = st.text_area("Beschreibung (optional)")
        priority = st.selectbox("Priorität auswählen", ["Niedrig", "Mittel", "Hoch"])
        save_task = st.form_submit_button("Aufgabe speichern")
        if save_task:
            if title:
                data_manager.append_record(
                    session_state_key='aufgaben_df',
                    record_dict={
                        "Titel": title,
                        "Fälligkeitsdatum": due_date,
                        "Beschreibung": description,
                        "Priorität": priority
                    }
                )
                st.success(f"Aufgabe '{title}' hinzugefügt!")
                st.rerun()
            else:
                st.error("Bitte gib einen Aufgabentitel ein.")

# --- Main Interface ---
st.title("📅 Fristentracker")

st.divider()

# Form inside box
with st.form("add"):
    # Layout inside the box
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f'<p style="color: {text}; font-size: 16px; margin-top: 8px;">Neue Aufgabe hinzufügen</p>', unsafe_allow_html=True)
    with col2:
        if st.form_submit_button("➕ Neue Aufgabe"):
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
        st.html(f"<div style='text-align: center; font-weight: bold; color: {text};'>{day_label}</div>")

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
                    prio = task.get("Priorität", "Niedrig")  # <- prio must be inside the loop

                    # Farbwahl basierend auf Priorität
                    if prio == "Niedrig":
                        color = "#d4edda"  # grünlich
                    elif prio == "Mittel":
                        color = "#fff3cd"  # gelblich
                    elif prio == "Hoch":
                        color = "#f8d7da"  # rötlich
                    else:
                        color = bg  # fallback

                    # Create unique delete ID
                    task_id = f"{task['Titel']}_{task['Fälligkeitsdatum']}_{i}".replace(" ", "_")

                    task_buttons_html += f"""
                        <div class='tooltip' style='font-size: 0.75em; padding: 4px; margin-top: 4px; color: black; background: {color}; border-radius: 9px; position: relative;'>
                            📝 {task['Titel']}
                            <span class='tooltiptext'>
                                <strong>Fälligkeit:</strong> {task['Fälligkeitsdatum'].strftime('%d.%m.%Y')}<br>
                                <strong>Priorität:</strong> {prio}<br>
                                <strong>Beschreibung:</strong> {tooltip_text}
                            </span>
                        </div>
                    """


                st.html(f"""
                    <div style="
                        border: 1px solid #aaaaaa;
                        border-radius: 0px;
                        padding: 6px;
                        min-height: 120px;
                        background-color: {bg};
                        display: flex;
                        flex-direction: column;
                        justify-content: flex-start;
                        position: relative;
                        color: {text};
                        gap: 0px;
                    ">
                        <div style="text-align: right; font-weight: bold;">{day}</div>
                        <div style="text-align: left;">{task_buttons_html}</div>
                    </div>
                """)

            else:
                st.html("""
                    <div style='border: 1px solid transparent; padding: 6px; min-height: 120px;'></div>
                """)