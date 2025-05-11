import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from utils.data_manager import DataManager
from utils.login_manager import LoginManager
import base64
from streamlit_theme import st_theme
from pathlib import Path

# ====== Init Block ======

# initialize the data manager
data_manager = DataManager(fs_protocol="webdav", fs_root_folder="MyStudentPal_DB")  # switch drive 

# initialize the login manager
login_manager = LoginManager(data_manager)
login_manager.login_register()  # open login/register page

# load the data from the persistent storage into the session state
data_manager.load_user_data(
    session_state_key='data_df', 
    file_name='data.csv', 
    initial_value = pd.DataFrame(), 
    # parse_dates = ['timestamp']
    )
# ====== End Init Block ======

# === Sidebar Navigation ===

# Load your image and encode it as base64

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

# Load data
data_manager.load_user_data(
    session_state_key='bewertungen_df',
    file_name='bewertungen.csv',
    initial_value=pd.DataFrame(columns=['Modul', 'Bewertung', 'Gewichtung', 'Note', 'Zeitstempel'])
)

data_manager.load_user_data(
    session_state_key='aufgaben_df',
    file_name='aufgaben.csv',
    initial_value=pd.DataFrame(columns=["Titel", "Fälligkeitsdatum", "Beschreibung"])
)

data_manager.load_user_data(
    session_state_key='modulen_df',
    file_name='modulen.csv',
    initial_value=pd.DataFrame(columns=["Modul", "ECTS", "Semester"])
)

bewertungen_df = st.session_state['bewertungen_df']
aufgaben_df = st.session_state['aufgaben_df']
modulen_df = st.session_state['modulen_df']

student_email_veroninka = "mitevver@students.zhaw.ch"
student_email_phiphi = "cungphi1@students.zhaw.ch"
student_email_melanie = "pomelmel@students.zhaw.ch"

theme = st_theme()
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

# === Top Title ===
st.markdown("### 📊 Dashboard")

st.divider()

# === Dashboard Layout ===
import matplotlib.pyplot as plt

# --- Quick Stats in Cards ---


# GPA calculation
avg_grade = "—"
if not bewertungen_df.empty and not modulen_df.empty:
    finals = []
    for modul, group in bewertungen_df.groupby("Modul"):
        weights = group["Gewichtung"].values
        grades = group["Note"].values
        score = np.dot(grades, weights) / 100.0
        ects = float(modulen_df.loc[modulen_df["Modul"] == modul, "ECTS"].iloc[0])
        finals.append({"Modul": modul, "ECTS": ects, "Endnote": round(score, 1)})
    finals_df = pd.DataFrame(finals)
    total_credits = finals_df["ECTS"].sum()
    weighted_sum = (finals_df["Endnote"] * finals_df["ECTS"]).sum()
    avg_grade = f"{(weighted_sum / total_credits):.2f}" if total_credits else "—"




# --- Quick Stats in Cards ---

with st.container():
    st.markdown("#### 📌 Kurzübersicht")
    st.html(f"""
  
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div style="background-color: {bg}; padding: 20px; border-radius: 12px; text-align: center;">
                <div style="font-size: 1.2em;">📐 Durchscnitt Note</div>
                <div style="font-size: 2.5em; font-weight: bold; margin-top: 10px;">{avg_grade}</div>
            </div>
            <div style="background-color: {bg}; padding: 20px; border-radius: 12px; text-align: center;">
                <div style="font-size: 1.2em;">📝 Aufgaben</div>
                <div style="font-size: 2.5em; font-weight: bold; margin-top: 10px;">{len(aufgaben_df)}</div>
            </div>
            <div style="background-color: {bg}; padding: 20px; border-radius: 12px; text-align: center;">
                <div style="font-size: 1.2em;">📚 Modulen</div>
                <div style="font-size: 2.5em; font-weight: bold; margin-top: 10px;">{len(modulen_df)}</div>
            </div>
                        <div style="background-color: {bg}; padding: 20px; border-radius: 12px; text-align: center;">
                <div style="font-size: 1.2em;">✅ Leistungsnachweise</div>
                <div style="font-size: 2.5em; font-weight: bold; margin-top: 10px;">{len(bewertungen_df)}</div>
            </div>
        </div>
    """)


import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import streamlit as st
import pandas as pd

st.markdown("#### 🏆 Top 5 Module nach Durchschnittsnote")

bewertungen_df = st.session_state.get("bewertungen_df", pd.DataFrame())

if not bewertungen_df.empty:
    top_courses = (
        bewertungen_df.groupby("Modul")["Note"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
    )

    fig, ax = plt.subplots()

    # Gradient colors (teal tones)
    colors = plt.cm.PuBuGn(np.linspace(0.4, 0.8, len(top_courses)))

    ax.bar(top_courses.index, top_courses.values, color=colors)
    ax.set_xlabel("Modul")
    ax.set_ylabel("Durchschnittsnote")
    ax.set_title("Top 5 Module nach Durchschnittsnote")
    ax.set_ylim(0, 6)  # Notenskala von 1 bis 6
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.info("Keine Noten vorhanden, um Top-Module anzuzeigen.")



# Section 1: About the App
st.html(f"""
    <div style="background-color: {bg}; padding: 20px; border-radius: 12px; margin-bottom: 20px;">
        <h3 style="color: {text};">ℹ️ Über MyStudentPal</h3>
        <p style="color: {text};">
            <strong>MyStudentPal</strong> ist ein digitaler Studienassistent, der Studierenden an Hochschulen und Universitäten hilft, ihr akademisches Leben zu organisieren.
            Die App zielt darauf ab, Stress zu reduzieren und die Produktivität zu steigern, indem sie klare und effiziente Werkzeuge für folgende Zwecke bereitstellt:
            <ul style="color: {text}; padding-left: 20px;">
                <li>Notenverwaltung</li>
                <li>Fristenmanagement</li>
                <li>Studienplanung</li>
            </ul>
            Die Hauptfunktionen legen den Fokus auf Einfachheit und Benutzerfreundlichkeit und helfen dabei, den Fortschritt zu visualisieren und Termine im Blick zu behalten.
            MyStudentPal ist ideal für Studierende, die eine zentrale Plattform suchen, um Aufgaben zu verwalten, Noten zu berechnen und akademische Aktivitäten strukturiert zu organisieren.
        </p>
    </div>
""")


# Section 2: Contributors
st.html(f"""
    <div style="background-color: {bg}; padding: 20px; border-radius: 12px; margin-bottom: 20px;">
        <h3 style="color: {text};">👥 Entwickelt von</h3>
        <ul style="color: {text}; padding-left: 20px;">
            <li>Veronika Miteva – <a href="mailto:{student_email_veroninka}" style="color: #1f77b4;">{student_email_veroninka}</a></li>
            <li>Phi Phi Cung – <a href="mailto:{student_email_phiphi}" style="color: #1f77b4;">{student_email_phiphi}</a></li>
            <li>Pomellitto Melanie – <a href="mailto:{student_email_melanie}" style="color: #1f77b4;">{student_email_melanie}</a></li>
        </ul>
    </div>
""")

# Section 3: Disclaimer
st.html(f"""
    <div style="background-color: {bg}; padding: 20px; border-radius: 12px; margin-bottom: 20px;">
        <h3 style="color: {text};">⚠️ Disclaimer</h3>
        <p style="color: {text};">
            Diese App wurde im Rahmen der Moduls <strong>BMLD Informatik 2</strong> an der ZHAW (Zürcher Hochschule für Angewandte Wissenschaften) entwickelt.
        </p>
    </div>
""")