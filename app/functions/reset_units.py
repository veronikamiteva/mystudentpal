import streamlit as st
from utils import helpers

# Function to reset unit selections when category changes
def reset_units():
    st.session_state.from_unit = helpers.categories[st.session_state.category][0]
    st.session_state.to_unit = helpers.categories[st.session_state.category][1]