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
import matplotlib.pyplot as plt
import numpy as np
from functions.backgound import set_background_theme, render_sidebar_logo
import random

# ====== Init Block ======
bg, text, border = set_background_theme(2)
render_sidebar_logo(2)

# load the data from the persistent storage into the session state
data_manager.load_user_data(
    session_state_key='data_df', 
    file_name='data.csv', 
    initial_value = pd.DataFrame(), 
    # parse_dates = ['timestamp']
    )

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


quotes = [
    "💡 'Innovation distinguishes between a leader and a follower.' – Steve Jobs",
    "🌱 'Learning never exhausts the mind.' – Leonardo da Vinci",
    "🎯 'The secret of getting ahead is getting started.' – Mark Twain",
    "📚 'Education is the most powerful weapon which you can use to change the world.' – Nelson Mandela",
    "🧠 'The beautiful thing about learning is that no one can take it away from you.' – B.B. King",
    "🔥 'Don’t watch the clock; do what it does. Keep going.' – Sam Levenson",
    "🌟 'Believe you can and you’re halfway there.' – Theodore Roosevelt",
    "🛠️ 'Opportunities don't happen. You create them.' – Chris Grosser",
    "🏔️ 'It always seems impossible until it's done.' – Nelson Mandela"
]

# ====== End Init Block ======

# === Top Title ===
st.markdown("### 📊 Dashboard")

st.divider()

# === Dashboard Layout ===

# Quote block
random_quote = random.choice(quotes)
st.html(f"""
    <div style="background-color: {bg}; border: 1px solid {border}; padding: 20px; border-radius: 12px; margin-bottom: 20px;">
        <h3 style="color: gray">Motivierendes Zitat </h3>
        <hr>
        <h4 style="color: {text}; font-style: italic; ">{random_quote}</h4>
    </div>
""")

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
            <div style="background-color: {bg}; border: 1px solid {border}; padding: 20px; border-radius: 12px; text-align: center;">
                <div style="font-size: 1.2em;">📐 Durchschnittsnote</div>
                <div style="font-size: 2.5em; font-weight: bold; margin-top: 10px;">{avg_grade}</div>
            </div>
            <div style="background-color: {bg}; border: 1px solid {border};  padding: 20px; border-radius: 12px; text-align: center;">
                <div style="font-size: 1.2em;">📝 Aufgaben</div>
                <div style="font-size: 2.5em; font-weight: bold; margin-top: 10px;">{len(aufgaben_df)}</div>
            </div>
            <div style="background-color: {bg}; border: 1px solid {border}; padding: 20px; border-radius: 12px; text-align: center;">
                <div style="font-size: 1.2em;">📚 Modulen</div>
                <div style="font-size: 2.5em; font-weight: bold; margin-top: 10px;">{len(modulen_df)}</div>
            </div>
                        <div style="background-color: {bg}; border: 1px solid {border};  padding: 20px; border-radius: 12px; text-align: center;">
                <div style="font-size: 1.2em;">✅ Leistungsnachweise</div>
                <div style="font-size: 2.5em; font-weight: bold; margin-top: 10px;">{len(bewertungen_df)}</div>
            </div>
        </div>
    """)

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
    <div style="background-color: {bg}; border: 1px solid {border}; padding: 20px; border-radius: 12px; margin-bottom: 20px;">
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
    <div style="background-color: {bg}; border: 1px solid {border}; padding: 20px; border-radius: 12px; margin-bottom: 20px;">
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
    <div style="background-color: {bg}; border: 1px solid {border}; padding: 20px; border-radius: 12px; margin-bottom: 20px;">
        <h3 style="color: {text};">⚠️ Disclaimer</h3>
        <p style="color: {text};">
            Diese App wurde im Rahmen der Moduls <strong>BMLD Informatik 2</strong> an der ZHAW (Zürcher Hochschule für Angewandte Wissenschaften) entwickelt.
        </p>
    </div>
""")
