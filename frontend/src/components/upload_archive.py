import streamlit as st

from utils.api__tools import post_file


def upload():
    file = st.file_uploader(
        'Arraste e solte seu arquivo Zip ou CSV aqui',
        type=['csv', 'zip'],
        key='uploaded_file',
    )

    separator = st.radio(
        'Separador do CSV', [', (vírgula)', '; (ponto e vírgula)', 'outro']
    )

    if separator == 'outro':
        separator = st.text_input('Insira o separador')

    file_upload = st.button('Enviar arquivo', icon='⬇️')

    if file:
        st.session_state['documents'].append(file.name)

        if file_upload:
            try:
                response = post_file(file, separator)

                st.success('O arquivo foi processado com sucesso!')
                st.dataframe(response)
            except Exception as e:
                st.error(f'Erro ao ler o arquivo CSV: {e}')
