
# Agente de Chat Inteligente com LangChain - SophIA 🧠

Este projeto apresenta uma **solução de Análise Exploratória de Dados (EDA) baseada em agentes**, permitindo que usuários interajam com seus arquivos CSV/ZIP por meio de um **chatbot inteligente**.

A arquitetura utiliza **LangChain** para orquestração de Agentes especializados, **FastAPI** para o backend de processamento de IA, **Streamlit** para o frontend de chat intuitivo e **Plotly/SQLite** para visualização de dados eficiente e com pouco consumo de tokens.

Toda a aplicação é empacotada e executada através do **Docker Compose**, garantindo um *setup* rápido e confiável.

### Índice
* [Instalação e Inicialização](https://github.com/Gabryel-Barboza/eda_tool_agent/tree/main?tab=readme-ov-file#-instala%C3%A7%C3%A3o-e-inicializa%C3%A7%C3%A3o)
* [Principais Funcionalidades](https://github.com/Gabryel-Barboza/eda_tool_agent/tree/main?tab=readme-ov-file#-principais-funcionalidades)
* [Endpoints da Aplicação](https://github.com/Gabryel-Barboza/eda_tool_agent/tree/main?tab=readme-ov-file#-endpoints-da-aplica%C3%A7%C3%A3o)
* [Estrutura de Arquivos](https://github.com/Gabryel-Barboza/eda_tool_agent/tree/main?tab=readme-ov-file#-endpoints-da-aplica%C3%A7%C3%A3o)
* [Detalhes Técnicos](https://github.com/Gabryel-Barboza/eda_tool_agent/tree/main?tab=readme-ov-file#-endpoints-da-aplica%C3%A7%C3%A3o)

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
    # API Keys (necessário pelo menos uma)
    GROQ_API_KEY=sua-chave-api
    GEMINI_API_KEY=sua-chave-api
    # Adicione ou altere outras variáveis de ambiente necessárias para a sua aplicação
    ```

### **Inicialização da aplicação**

Para subir todos os serviços (**Streamlit** e **FastAPI**), execute o seguinte comando (ainda no diretório raiz):

```bash
docker compose up --build
```

O argumento `--build` é opcional, incorporando quaisquer atualizações no código para o container.

-----

## ✨ Principais Funcionalidades

| Funcionalidade | Detalhe Técnico |
| :--- | :--- |
| **Análise Conversacional** | Chatbot que responde perguntas sobre os dados, chama ferramentas de análise e gera gráficos sob demanda. |
| **Arquitetura de Agentes** | Dois Agentes orquestrados (`AnswerAgent` e `DataAnalystAgent`) para separar a lógica de conversação da análise de dados. |
| **Eficiência de Tokens** | Agente especialista acessa o DataFrame apenas internamente nas ferramentas, otimizando o consumo de tokens. |
| **Visualização Inteligente** | Geração de gráficos Plotly dinâmicos (Histogramas, Scatter Plots, etc.) sob comando do usuário. |
| **Cache de Gráficos** | Gráficos são serializados como JSON e armazenados em um banco de dados **SQLite** para evitar o reprocessamento e o envio do JSON/imagem no contexto da LLM. |
| **Suporte a Arquivos** | Permite upload de arquivos **CSV** e **ZIP** (com descompactação automática). |

----

### 🌐 Endpoints da Aplicação

| Serviço | URL |
| :--- | :--- |
| **Frontend (Streamlit)** | `http://localhost:8501` |
| **API Docs (FastAPI - Swagger UI)** | `http://localhost:8000/api/docs` |

----


### 📂 Estrutura de arquivos

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

O projeto utiliza uma hierarquia de agentes para otimizar o fluxo de trabalho:

1.  **`AnswerAgent` (Orquestrador):** Recebe o *prompt* do usuário. Decide se a pergunta é geral (responde diretamente) ou de dados. Se for de dados, chama o `DataAnalystAgent` como uma **ferramenta**.
2.  **`DataAnalystAgent` (Especialista):** Usa ferramentas especializadas (como `create_histogram`, `create_scatter_plot`) que:
      * Chamada a função **`get_dataframe()`** internamente para acessar os dados.
      * Geram a figura Plotly (`fig`).
      * Calculam e geram um **`metadata`** (resumo textual da análise) e salvam o gráfico via **`_save_graph_to_db(fig, metadata)`**.
3.  **Processamento de Gráficos:** A resposta do `DataAnalystAgent` contém o **`graph_id`** e o **`metadata`**. O *metadata* é injetado no contexto do `AnswerAgent` para ele poder comentar o gráfico, enquanto o Frontend usa o `graph_id` para buscar o JSON do Plotly no SQLite e renderizá-lo.


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
  - [x] Criar DataAnalystAgent para gerar resposta com os dados
- [x] Criar ferramentas dos agentes
  - [x] Criar ferramenta para interação com banco de dados
  - [x] Criar ferramenta para obter tempo e data
  - [x] Fazer DataAnalystAgent ser uma ferramenta de AnswerAgent
  - [x] Criar ferramenta ou meio para restringir o formato de saída do agente
- [x] Criar serviços para utilizar os agentes e inserir dados
  - [x] Criar serviço para instanciar o agente de chat
  - [x] Criar serviço para inserir os dados de arquivos csv
  - [x] Possibilitar alteração do modelo com método do chat
  - [x] Atualizar o serviço de dados para descompactar arquivos zip
- [x] Mover arquivo .env para raiz
- [] Criar documentação
  - [ ] Criar docstrings e organizar projeto
  - [x] atualizar `docs/`
- [x] Atualizar requirements.txt e .env.example
- [ ] Analisar possibilidade para atualização com bancos de dados vetoriais
- [x] Atualizar método de criação de gráficos com AnswerAgent para eficiência do uso do agente.
- [x] Recuperar gráficos de bancos de dados para mais eficiência.
- [x] Aprimorar resposta do agente e reduzir erros com engenharia de prompt
- [ ] Publicar projeto em Cloud para acesso externo ou ngrok

