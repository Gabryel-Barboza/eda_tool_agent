import streamlit as st

from utils.api__tools import get_chart, post_message


def chat_section():
    st.markdown('### Converse com SophIA')

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    chat_holder = st.empty()
    lcol, rcol = st.columns(2)

    with lcol:
        st.chat_input(
            key='user_query',
            placeholder='Enviar mensagem para SophIA',
            max_chars=500,
            width=580,
        )

    if st.session_state['user_query']:
        st.session_state['chat_history'].append(
            {'role': 'user', 'content': st.session_state['user_query']}
        )

        with st.spinner('SophIA está pensando...'):
            user_input = st.session_state['user_query']

            content = post_message(user_input)

            st.session_state['chat_history'].append(
                {'role': 'bot', 'content': content[0], 'graph_id': content[1]}
            )

        st.session_user_query = None

    with chat_holder.container(height=450):
        for message in st.session_state['chat_history']:
            st.html(
                f'<div class="chat-message {message["role"]}-message">{message["content"]}</div>'
            )

            if 'graph_id' in message and message['graph_id']:
                try:
                    plotly_chart = get_chart(message['graph_id'])
                    st.plotly_chart(plotly_chart)
                except Exception:
                    pass
