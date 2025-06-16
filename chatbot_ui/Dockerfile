FROM python:3.12-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código da aplicação para o diretório de trabalho
COPY src .

# Exporta variáveis ambiente
# Troque a URL para o seu webhook, se localhost use n8n:5678 como host
ENV N8N_WEBHOOK_URL=http://n8n:5678/webhook/user_messages


# Define o comando para iniciar a aplicação quando o contêiner for executado
# O '-u' garante que os logs do Python apareçam sem buffer no console do Docker
CMD ["python", "-u", "app.py"]
