import os
from pathlib import Path

import requests
from flask import Flask, render_template_string, request
from requests import RequestException

app = Flask(__name__)


# URL do webhook do seu agente n8n.
# o valor aqui deve ser 'http://n8n:5678/webhook/123-abc'
N8N_WEBHOOK_URL = os.getenv(
    'N8N_WEBHOOK_URL', 'http://n8n:5678/webhook/YOUR_WEBHOOK_PATH'
)

ROOT_PATH = Path(__file__).parent

# Template HTML para a interface do chatbot com Tailwind CSS
with open(ROOT_PATH / 'index.html', 'r', encoding='utf-8') as arquivo:
    HTML_TEMPLATE = ''.join(arquivo.readlines())


# Rota principal que serve a página do chatbot
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)


# Rota para receber mensagens da interface e enviar para o n8n
@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')

    if not user_message:
        return {'error': 'Mensagem vazia'}, 400

    if 'YOUR_WEBHOOK_PATH' in N8N_WEBHOOK_URL:
        return {
            'reply': 'ERRO: A URL do webhook do n8n não foi configurada no arquivo app.py.'
        }

    try:
        # Envia a mensagem para o webhook do n8n
        n8n_response = requests.post(
            N8N_WEBHOOK_URL,
            json={'message': user_message},
            headers={'Content-Type': 'application/json'},
        )

        if n8n_response.status_code != 200:
            raise RequestException

        bot_reply = n8n_response.text

    except RequestException as e:
        print(f'Erro ao conectar ao n8n: {e}')
        bot_reply = 'Não foi possível conectar ao agente n8n. Verifique se o serviço está no ar e a URL está correta.'
    except Exception as e:
        print(f'Um erro inesperado ocorreu: {e}')
        bot_reply = 'Ocorreu um erro inesperado ao processar sua solicitação.'

    return {'reply': bot_reply}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
