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
import base64
from datetime import datetime
from utils import helpers  # optional
from streamlit_theme import st_theme

# Load your image and encode it as base64
with open("../assets/logo-msp.png", "rb") as image_file:
    encoded = base64.b64encode(image_file.read()).decode()

# Create the HTML for the image
logo_html = f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{encoded}" width="150">
    </div>
"""

# Display the logo in the sidebar
st.sidebar.markdown(logo_html, unsafe_allow_html=True)

theme = st_theme() # or your st_theme() function

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

# --- Load or initialize settings DataFrame ---
data_manager.load_user_data(
    session_state_key='einstellungen_df',
    file_name='einstellungen.csv',
    initial_value=pd.DataFrame(columns=["Einstellung", "Wert"])
)

settings_df = st.session_state["einstellungen_df"]

# --- Load existing settings values ---
def get_setting(name, default_value):
    if name in settings_df['Einstellung'].values:
        return settings_df.loc[settings_df['Einstellung'] == name, 'Wart'].values[0]
    else:
        return default_value

# --- Main interface ---
st.title("🌍 Manager für globale Einstellungen")
st.divider()

st.html(f"""
    <div style="background-color: {bg}; padding: 15px; border-radius: 12px;">
        <p style="color: {text}; padding-top: 15px;">
            Konfiguriere deine Bewertungsparameter!
        </p>
    </div>
""")

with st.form('settings_form'):
    st.subheader('Bewertungseinstellungen')

    scale = st.selectbox(
        'Bewertungsskala',
        options=['1.0-6.0', '0.0-4.0', '0-100%'],
        index=['1.0-6.0', '0.0-4.0', '0-100%'].index(get_setting('scale', '1.0-6.0'))
    )

    rounding = st.selectbox(
        'Rundungsmethode',
        options=['Eine Dezimalstelle (Standard)', 'Immer aufrunden', 'Immer abrunden'],
        index=['Eine Dezimalstelle (Standard)', 'Immer aufrunden', 'Immer abrunden'].index(get_setting('rounding', 'Eine Dezimalstelle (Standard)'))
    )

    passing_threshold = st.number_input(
        'Bestehensgrenze',
        min_value=0.0,
        max_value=100.0,
        step=0.1,
        value=float(get_setting('passing_threshold', 4.0))
    )

    gpa_method = st.radio(
        'Durchschnittsmethode',
        options=['Gewichteter Durchschnitt', 'Gewichte normalisieren'],
        index=['Gewichteter Durchschnitt', 'Gewichte normalisieren'].index(get_setting('gpa_method', 'Gewichteter Durchschnitt'))
    )

    save_settings = st.form_submit_button('Einstellungen speichern')

    if save_settings:
        # Save or update each setting individually
        for setting_name, setting_value in {
            'Bewertungsskala': scale,
            'Rundungsmethode': rounding,
            'Bestehensgrenze': passing_threshold,
            'Durchschnittsmethode': gpa_method
        }.items():
            if setting_name in settings_df['Einstellung'].values:
                # Update existing
                settings_df.loc[settings_df['Einstellung'] == setting_name, 'Wert'] = setting_value
            else:
                # Add new setting
                data_manager.append_record(
                    session_state_key='einstellungen_df',
                    record_dict={'Einstellung': setting_name, 'Wert': setting_value}
                )
        
        st.success('Einstellungen gespeichert')
        st.rerun()

# --- Display settings table ---
if not st.session_state["einstellungen_df"].empty:
    st.write('### Aktuelle Einstellungen')
    st.dataframe(st.session_state["einstellungen_df"])
else:
    st.info("Noch keine Einstellungen gespeichert.")
