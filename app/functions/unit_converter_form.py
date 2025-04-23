import streamlit as st 

def unit_converter_form():
    with st.form(key="unit_converter"):
        value = st.number_input("Wert eingeben", min_value=0.0, format="%.2f")
        submit_button = st.form_submit_button(label="Umrechnen")
        return value, submit_button
