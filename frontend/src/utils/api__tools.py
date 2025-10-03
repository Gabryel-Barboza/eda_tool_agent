import json
import os

import plotly.io as pl
import requests
import streamlit as st

API_URL = os.environ.get('FASTAPI_URL', 'http://localhost:8000/api')
MODELS = {
    'groq': [
        'qwen/qwen3-32b',
        'llama-3.1-8b-instant',
        'llama-3.3-70b-versatile',
        'openai/gpt-oss-20b',
        'openai/gpt-oss-120b',
    ],
    'gemini': ['gemini-1.5-pro', 'gemini-2.5-flash', 'gemini-2.5-pro'],
}

model = 'qwen/qwen3-32b'


def post_file(file):
    if API_URL:
        file = {'file': (file.name, file, file.type)}
        url = API_URL + '/upload'
        response = requests.post(url, files=file)

        if response.ok:
            return response.json()

        else:
            st.error(f'{response.status_code} {response.reason} - {response.text}')

    else:
        st.error('No API URL found, add this variable to the environment first.')


def post_message(msg: str):
    if API_URL:
        url = API_URL + '/prompt'
        response = requests.post(url, json={'request': msg})

        if response.ok:
            content = response.json()

            if not content['response']:
                content['response'] = 'Response error, maybe try other model.'

            return content['response'], content['graph_id']

        else:
            st.error(f'{response.status_code} {response.reason} - {response.text}')

    else:
        st.error('No API URL found, add this variable to the environment first.')


def change_model(model_name: str):
    global model

    # Prevent request for same model
    if model == model_name:
        return

    if API_URL:
        provider = 'groq' if model_name in MODELS['groq'] else 'google'
        model = model_name
        url = API_URL + f'/change-model?provider={provider}&model={model_name}'

        response = requests.put(url)

        if response.ok:
            return
        else:
            st.error(f'{response.status_code} {response.reason} - {response.text}')
    else:
        st.error('No API URL found, add this variable to the environment first.')


def get_chart(graph_id: str):
    if API_URL:
        url = API_URL + f'/graphs/{graph_id}'

        response = requests.get(url)

        if response.ok:
            content = response.json()

            graph_json = content.get('graph')

            if graph_json:
                return pl.from_json(graph_json)
        else:
            st.error(f'{response.status_code} {response.reason} - {response.text}')
    else:
        st.error('No API URL found, add this variable to the environment first.')
