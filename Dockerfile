FROM python:3.12.11-alpine

# Dependências de compilação
RUN apk add --no-cache build-base python3-dev

COPY backend /app

WORKDIR /app

# Instalando projeto
RUN pip install -qq --no-cache-dir -r requirements.txt

WORKDIR /app/src

CMD ["fastapi", "run", "main.py"]
