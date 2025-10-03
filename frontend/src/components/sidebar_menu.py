from pathlib import Path

import streamlit as st

from utils.api__tools import MODELS, change_model

ROOT_PATH = Path(__file__).parent.parent
documents = []


def sidebar():
    st.markdown('## Documentos Anexados')

    if 'documents' not in st.session_state:
        st.session_state.documents = []

    for document in st.session_state['documents']:
        if document not in documents:
            st.write(document)
            documents.append(document)

    st.write('---')
    st.selectbox(
        '### Modelo Utilizado',
        options=[*[model for modelList in MODELS.values() for model in modelList]],
        key='model',
    )

    st.button('Alterar', on_click=change_model, args=[st.session_state['model']])

    st.write('### Sobre SophIA')
    st.image(image=ROOT_PATH / 'static/sophia.png', width=150)
    st.info(
        'SophIA é um agente de dados inteligente, criada utilizando o framework Langchain e integrada a ferramentas para análise de dados, permitindo a geração de insights para qualquer planilha de dados.',
    )
