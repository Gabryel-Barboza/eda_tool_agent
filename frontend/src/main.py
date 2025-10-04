import streamlit as st

from components import api_key_section, chat_section, sidebar, style, title, upload

st.set_page_config(
    page_title='SophIA - EDA Tool',
    page_icon='🧠',
    layout='wide',
    initial_sidebar_state='expanded',
)

# Page Components
style()

with st.sidebar:
    sidebar()

title()
st.divider()
api_key_section()
st.divider()
upload()
chat_section()
