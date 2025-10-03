import mistune
import streamlit as st

from utils.api__tools import get_chart, post_message


@st.fragment()
def chat_section():
    st.markdown('### Converse com SophIA')

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    chat_holder = st.empty()
    lcol, _ = st.columns([3, 1])  # Usando uma proporção para o input

    with lcol:
        st.chat_input(
            key='user_query',
            placeholder='Enviar mensagem para SophIA',
            max_chars=500,
            width=580,
        )

    with chat_holder.container(height=450):
        for message in st.session_state['chat_history']:
            if 'content' in message and message['content']:
                st.html(f"""
                    <pre class="chat-message {message['role']}-message">
                    {mistune.html(message['content'])}
                    </pre>""")

            if 'graph_id' in message and message['graph_id']:
                try:
                    plotly_chart = get_chart(message['graph_id'])
                    st.plotly_chart(plotly_chart)
                except Exception as e:
                    st.error(f'Não foi possível carregar o gráfico: {e}')

        if st.session_state['user_query']:
            st.session_state['chat_history'].append(
                {'role': 'user', 'content': st.session_state['user_query']}
            )
            msg_before = len(st.session_state['chat_history'])

            with st.spinner('SophIA está pensando...'):
                user_input = st.session_state['user_query']

                content = post_message(user_input)

                st.session_state['chat_history'].append(
                    {'role': 'bot', 'content': content[0], 'graph_id': content[1]}
                )

            msg_after = len(st.session_state['chat_history'])

            if msg_after > msg_before:
                st.rerun(scope='fragment')

            st.session_state['user_query'] = None
