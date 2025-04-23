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

st.title("Unsere erste Streamlit App")

st.write("Einheitenumrechner")

st.write("Diese App wurde von den folgenden Personen entwickelt:")

student_email_veroninka = "mitevver@students.zhaw.ch"
student_email_phiphi = "cungphi1@students.zhaw.ch"
st.write("Veronika Miteva - " + f"{student_email_veroninka}")
st.write("Phi Phi Cung - " + f"{student_email_phiphi}")

st.write("Diese App ermöglicht das mühelose Umrechnen von Länge, Volumen, Gewicht und Temperatur zwischen verschiedenen Masseinheiten.")