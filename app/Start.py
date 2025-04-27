import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

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
st.title("MyStudentPal")


st.write("MyStudentPal ist ein digitaler Studienassistent, der Universitäts- und Hochschulstudierende dabei unterstützt, ihr akademisches Leben zu organisieren. Die App zielt darauf ab, Stress zu reduzieren und die Produktivität zu steigern, indem sie klare und effiziente Tools zur Notenverfolgung, Fristenverwaltung und Studienplanung bereitstellt.")

st.write("Die Kernfunktionen konzentrieren sich auf Einfachheit und Benutzerfreundlichkeit und helfen den Nutzenden, ihren Fortschritt zu visualisieren und Fristen im Blick zu behalten. Die App eignet sich besonders für Studierende, die eine zentrale Plattform benötigen, um ihre Aufgaben zu verwalten, Noten zu berechnen und akademische Tätigkeiten strukturiert zu organisieren.")

st.write("Diese App wurde von den folgenden Personen entwickelt:")

student_email_veroninka = "mitevver@students.zhaw.ch"
student_email_phiphi = "cungphi1@students.zhaw.ch"
student_email_melanie = "pomelmel@students.zhaw.ch"
st.write("Veronika Miteva - " + f"{student_email_veroninka}")
st.write("Phi Phi Cung - " + f"{student_email_phiphi}")
st.write("Pomellitto Melanie -" + f"{student_email_melanie}")

st.write("Diese App wurde im Rahmen der Moduls 'BMLD Informatik 2' an der ZHAW entwickelt.")







