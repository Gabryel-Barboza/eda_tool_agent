import streamlit as st


def style():
    st.html("""
<style>
    p {
        font-size: 1.1em !important;
    }
    pre {
            white-space: pre-line;
    }
    input[placeholder='Enviar mensagem para SophIA'] {
        width: 420px;
    }
    .reportview-container .main {
        color: #f0f2f6;
        background-color: #0e1117;
    }
    .stApp {
        background-color: #0e1117;
    }
    .stSidebar {
        background-color: #1a1a2e;
        color: #f0f2f6;
    }
    .stElementContainer:has(.stImage) > div > div {
        width: 100%;        
    }
    .stAlertContainer {
        box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.3);
    }
    .stAlertContainer p {
        color: #fff;
    }
    .stFileUploader {
        background-color: #2b2b3b;
        border: 1px dashed #6a6a8a;
        padding: 1rem;
        border-radius: 0.5rem;
        color: #f0f2f6;
    }
    .stChatInput { 
        background-color: #2b2b3b;
        border-radius: 1.25rem;
        border: 1px solid #6a6a8a;
    }
    .stElementContainer:has(.chat-message) {
        width: fit-content;
        max-width: 65%;
    }
    .stElementContainer:has(.user-message) {
        align-self: flex-end;
    }
    .stElementContainer:has(.bot-message) {
        align-self: flex-start;
    }
    .stHtml:has(.chat-message) {
            padding: 10px;
    }
    .chat-message {
        width: fit-content;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 5px;
        box-shadow: 2px 2px 2px rgba(0,0,0,0.3)
    }
    .chat-message ul, .chat-message ol {
        list-style-position: inside;
    }
    .user-message {
        background-color: #3f51b5;
        color: white;
    }
    .bot-message {
        background-color: #1a1a2e;
        color: #f0f2f6;
        align-self: flex-start;
    }
    .stButton > button {
        background-color: #3f51b5;
        color: white;
        border-radius: 0.5rem;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stSpinner > div > div {
        margin: auto;
    }
</style>
""")
