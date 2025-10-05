import streamlit as st

from utils.api__tools import send_key


def title():
    st.write('# Apresentamos SophIA 🧠')
    st.write(
        '> Um agente capaz de analisar dados, detectar padrões e responder a dúvidas.'
    )
    st.write('SophIA consegue:')
    st.write('* Receber dados de arquivos CSV.')
    st.write('* Armazenar em seu banco de dados.')
    st.write('* Gerar insights e respostas com base nos seus dados.')


def api_key_section():
    st.write(
        '**Primeiro, insira sua chave de API e selecione o provedor, depois de enviar escolha o modelo apropriado (opcional se `.env` já possuir uma).**'
    )
    lcol, rcol = st.columns(2)

    with rcol:
        st.selectbox(
            'Provedor', options=['Google', 'Groq'], key='api_key_provider', width=200
        )

    with lcol:
        st.text_input(
            'API Key', type='password', placeholder='Sua chave de API', key='api_key'
        )

    api_key = st.session_state['api_key']
    key_provider = st.session_state['api_key_provider'].lower()
    if st.button('Enviar', on_click=send_key, args=[api_key, key_provider]) and api_key:
        st.toast('Chave enviada com sucesso!')
