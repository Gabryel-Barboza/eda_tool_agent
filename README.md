
# Agente de Chat Inteligente com LangChain 🧠

Este projeto apresenta um **agente inteligente** que utiliza a biblioteca **LangChain** para processar e analisar dados de arquivos CSV. O backend, construído com **FastAPI**, gerencia a lógica de processamento e a comunicação com um banco de dados **MySQL**, enquanto o frontend, feito com **Streamlit**, oferece uma interface de chat intuitiva para interagir com o agente.

Toda a aplicação é orquestrada de forma eficiente com o **Docker Compose**, garantindo um ambiente de desenvolvimento e produção consistente e fácil de configurar.

### Índice
* [Instalação e Inicialização](https://github.com/Gabryel-Barboza/rag_chatbot_agent/tree/main?tab=readme-ov-file#-instala%C3%A7%C3%A3o-e-inicializa%C3%A7%C3%A3o)
* [Endpoints](https://github.com/Gabryel-Barboza/rag_chatbot_agent?tab=readme-ov-file#-endpoints-da-aplica%C3%A7%C3%A3o)
* [Estrutura de Arquivos](https://github.com/Gabryel-Barboza/rag_chatbot_agent?tab=readme-ov-file#-endpoints-da-aplica%C3%A7%C3%A3o)
* [Detalhes Técnicos](https://github.com/Gabryel-Barboza/rag_chatbot_agent?tab=readme-ov-file#-endpoints-da-aplica%C3%A7%C3%A3o)

## 🚀 Instalação e Inicialização

### **Pré-requisitos**

Para executar este projeto, você só precisa ter o **Docker** e o **Docker Compose** instalados na sua máquina e 3 GB de armazenamento livre. Se ainda não os tem, você pode seguir os links abaixo para a instalação oficial:

  * [**Instalação do Docker no Windows**](https://docs.docker.com/desktop/install/windows-install/)
  * [**Instalação do Docker no Linux**](https://docs.docker.com/engine/install/ubuntu/)

### **Configuração do ambiente**

1.  **Clone o repositório do GitHub:**
    ```bash
    git clone https://github.com/Gabryel-Barboza/rag_chatbot_agent.git
    cd rag_chatbot_agent
    ```
    > Ou baixe o `.zip` clicando no botão **Code <>** acima.

2.  **Configurar variáveis de ambiente:**
    Dentro do diretório raiz do projeto, copie o arquivo de exemplo `.env.example` e renomeie-o para `.env`. Em seguida, preencha as variáveis com as suas credenciais.
    ```bash
    cp .env.example .env
    ```
    
    O arquivo `.env` deve conter, no mínimo, as seguintes variáveis:
    ```env
    # Variáveis para o banco de dados MySQL
    MYSQL_DATABASE=data_csv
    MYSQL_USER=langchain_agent
    MYSQL_PASSWORD=mypassword
    MYSQL_ROOT_PASSWORD=myrootpassword

    # API Keys (necessário pelo menos uma)
    GROQ_API_KEY=sua-chave-api
    GEMINI_API_KEY=sua-chave-api
    # Adicione outras variáveis de ambiente necessárias para a sua aplicação
    ```

### **Inicialização da aplicação**

Para subir todos os serviços (**Streamlit**, **FastAPI** e **MySQL**), execute o seguinte comando (ainda no diretório raiz):

```bash
docker compose up --build
```

O argumento `--build` é opcional, incorporando quaisquer atualizações no código para o container.

-----

## 🌐 Endpoints da Aplicação

### **Acesso à interface (Streamlit)**

Após a inicialização, a interface web estará disponível em:

  * **URL:** `http://localhost:8501`

### **API (FastAPI)**

A API do backend pode ser acessada através da porta `8000`. A documentação interativa (Swagger UI) está disponível em:

  * **URL:** `http://localhost:8000/api/docs`

-----

## 📂 Estrutura de arquivos

A estrutura do projeto está organizada da seguinte forma:

```
.
├── .env.example              # Exemplo de arquivo com as variáveis de ambiente
├── compose.yml        # Orquestração dos serviços Docker
├── Dockerfile                # Dockerfile para o backend (FastAPI)
├── Dockerfile.streamlit      # Dockerfile para o frontend (Streamlit)
├── init.sql                  # Script de inicialização do banco de dados MySQL
├── backend/                  # Código fonte do backend (FastAPI)
│   ├── src/
|   |   ├── agents/
|   |   ├── controllers/
|   |   ├── tools/
│   │   ├── services/
│   │   ├── schemas/
|   |   ├── utils/
│   │   ├── main.py
│   │   └── settings.py       # Configurações recebidas das variáveis de ambiente
│   ├── requirements.txt      # Arquivo de instalação das dependências
│   └── ...                   # Arquivos de configurações do projeto
├── frontend/                 # Código fonte do frontend (Streamlit)
│   ├── src/
|   |   ├── components/       # Componentes para a página Streamlit 
│   │   ├── main.py
|   |   ├── README.md         # Documentação específica da interface
│   │   └── ...
│   └── requirements.txt
└── README.md                 # Esta documentação
```

### **Detalhes técnicos**

  * **Backend (FastAPI)**: Recebe os prompts e gerencia a comunicação com o agente LangChain para processar os dados armazenados no banco de dados.
  * **Frontend (Streamlit)**: Oferece a interface de chat para os usuários interagirem com o agente.
  * **MySQL**: Armazena os dados processados dos arquivos CSV, servindo como a fonte de dados para o agente.
  * **LangChain**: A biblioteca principal utilizada para construir o agente inteligente, permitindo o processamento e a análise dos dados de forma conversacional.

Se precisar de ajuda ou tiver alguma dúvida, sinta-se à vontade para abrir uma **issue** no repositório do GitHub ou entrar em contato.

### TODO:

- [x] Criar projeto com POO
- [x] Criar interface do projeto
  - [x] Analisar uso do Streamlit como framework
  - [x] Possibilitar upload de CSV ou zip e uma interface de chat
  - [x] Possibilitar a troca de modelos no agente
- [x] Criar API para integração
  - [x] Criar controladores para separar endpoints
  - [x] Configurar endpoints FastAPI
  - [x] Configurar endpoint para mudar modelo LLM utilizado
  - [x] Configurar tratamento de erros
- [x] Criar agentes
  - [x] Criar BaseAgent para generalização entre agentes
  - [x] Adicionar métodos para troca entre modelos e provedores de agente (Gemini, gemini-2.5-flash...)
  - [x] Criar AnswerAgent para orquestrador da resposta ao usuário
  - [x] Criar SQLAgent para interação com banco de dados
- [x] Criar ferramentas dos agentes
  - [x] Criar ferramenta para interação com banco de dados
  - [x] Criar ferramenta para obter tempo e data
  - [x] Fazer SQLAgent ser uma ferramenta de AnswerAgent
  - [x] Criar ferramenta ou meio para restringir o formato de saída do agente
- [x] Criar serviços para utilizar os agentes e inserir dados
  - [x] Criar serviço para instanciar o agente de chat
  - [x] Criar serviço para inserir os dados de arquivos csv
  - [x] Possibilitar alteração do modelo com método do chat
  - [x] Atualizar o serviço de dados para descompactar arquivos zip
  - [x] Possibilitar inserção dos dados em banco de dados MySQL
  - [x] Alterar método de inserção para eficiência de tokens
- [x] Mover arquivo .env para raiz
- [] Criar documentação
  - [ ] Criar docstrings e organizar projeto
  - [ ] atualizar `docs/`
- [x] Atualizar requirements.txt e .env.example
- [ ] Analisar possibilidade para atualização com bancos de dados vetoriais
- [ ] Atualizar método de criação de gráficos com AnswerAgent para eficiência do uso do agente.
- [ ] Aprimorar resposta do agente e reduzir erros com engenharia de prompt
- [ ] Publcar projeto em Cloud para acesso externo ou ngrok
