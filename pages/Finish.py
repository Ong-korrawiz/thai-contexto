import streamlit as st
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(page_title="Finish", page_icon="💯")
replay = st.button("Play Again ↺")
if replay:
    switch_page("Home")