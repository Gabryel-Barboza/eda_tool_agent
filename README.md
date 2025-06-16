# Agente de Conversas com RAG

Este projeto consiste em um chatbot web que interage com um agente de automação rodando no **N8N**. A interface web permite aos usuários enviar mensagens que são processadas pelo N8N, e as respostas do agente são exibidas de volta no chat.

## Visão Geral

O chatbot é construído utilizando Flask (Python) para a interface web e se comunica com o n8n através de webhooks HTTP. A interface do usuário é estilizada com Tailwind CSS e inclui funcionalidades como histórico de mensagens (em uma barra lateral) e suporte básico para renderização de Markdown nas respostas do bot.

### Pré-requisitos

  * [Docker](https://www.docker.com/products/docker-desktop/) instalado na sua máquina.

### Instalação e Execução com Docker

Este projeto pode ser facilmente instanciado utilizando Docker e Docker Compose. Certifique-se de ter o Docker e o Docker Compose (é instalado por padrão junto ao Docker) instalados antes de prosseguir.

1. Download do projeto

Clique no botão em verde `<> Code` e faça o clone com Git utilizando a URL ou baixe o arquivo em `.zip` e extraía no local desejado.

2. Abra o diretório do projeto

No diretório raiz do seu projeto, onde está localizada a pasta `chatbot_ui` abra um terminal.
* Linux: Botão do mouse direito -> abrir no terminal ou `cd ~/caminho_projeto/rag_agent_chatbot`.
* Windows: Abrir pasta do projeto, na barra de endereços digite `CMD` ou abra um terminal e navegue até o diretório com `cd caminho_projeto\rag_agent_chatbot`.

**Antes de instalar o projeto, renomeie o arquivo `.env.example` para `.env` e altere as configurações de senha se desejado.**

3. Execute o Docker Compose

Agora, execute o seguinte comando no terminal, no mesmo diretório:

```bash
docker compose up -d
```

Para parar a execução do contêiner execute o comando no mesmo diretório:

```bash
docker compose down
```

Este comando irá construir a imagem Docker (se ainda não existir) e iniciar o container do chatbot em segundo plano.

4. Configure a URL do Webhook do N8N

Importante: Se o projeto não for usado em ambiente local, você precisa configurar a URL do webhook do seu agente n8n no arquivo em chatbot_ui/Dockerfile. As configurações padrão devem funcionar em `localhost`.

  * Abra o arquivo.

  * Localize a linha que define a variável N8N_WEBHOOK_URL:
  
  ```bash
    ENV N8N_WEBHOOK_URL=http://n8n:5678/webhook/user_messages
  ```

  * Substitua 'http://n8n:5678/webhook/user_messages' pela URL real do webhook do seu workflow no n8n. Certifique-se de que o serviço n8n esteja acessível a partir do container do chatbot (isso é geralmente resolvido pela rede Docker Compose). Se o seu serviço n8n estiver rodando no mesmo Docker Compose, http://n8n:5678/webhook/user_messages geralmente funcionará.

  * Se você alterou a configuração de qualquer arquivo, precisará reconstruir e reiniciar o container do chatbot:

    ```bash
    docker compose build  # Reconstruir imagem com novas configurações 
    docker compose up -d
    ```

### Endpoints de Acesso

Após a execução do Docker Compose, você poderá acessar o chatbot e o n8n nos seguintes endpoints:

  Interface Web do Chatbot: http://localhost:8000.

  ![Imagem do Chatbot]()

  Interface Web do n8n: http://localhost:5678.
  
  ![Imagem da interface N8N]()

## Utilização

  Acesse a interface web do N8N através do link fornecido acima. Se necessário crie sua conta do N8N e abra um novo workflow. Clique no botão ao lado de `save` e depois em `import file`, selecione o arquivo `agente_leitor_csv.json` no diretório do projeto.

  Configure as credenciais de cada Nó do agente, utilize uma chave de API para os modelos LLM (modelo gemini-flash 2.0 testado) e crie uma credencial de acesso ao banco de dados em um dos nós. No processo de criação, insira as seguintes informações para cada campo:

  * abc

  Agora, inicialize o fluxo de trabalho clicando em `active` ao lado de `save` e faça os testes na interface web. Lembre-se que o nó webhook deve possuir a mesma URL configurada no arquivo Dockerfile citado
  
  Digite sua mensagem na caixa de texto do chatbot e clique em "Enviar".
  A mensagem será enviada para o webhook do n8n.
  O n8n processará a mensagem e enviará uma resposta de volta para o chatbot, que será exibida na interface.
  Você pode usar o botão no canto superior direito para abrir a barra lateral com o histórico de mensagens.

## Estrutura de Código

A estrutura do código do projeto é a seguinte:

  ```bash
  # Contém a lógica do servidor Flask para a interface web do chatbot. Define as rotas para exibir a página inicial e receber mensagens do usuário, encaminhando-as para o n8n.
  app.py
  # Arquivo HTML que define a estrutura da interface do chatbot, incluindo a caixa de mensagens, a área de exibição do chat e o formulário de envio. Utiliza Tailwind CSS para estilização.
  index.html
  static/
    # Contém a lógica JavaScript para interagir com a interface do chatbot, enviar mensagens e atualizar a exibição do chat. Utiliza a biblioteca marked.js para renderizar Markdown nas mensagens do bot.
    main.js
    # Contém a lógica JavaScript para controlar a barra lateral do histórico de mensagens.
    sidebar.js 
    # Contém estilos CSS adicionais e customizações para a interface do chatbot.
    styles.css 
  ```

## Próximos Passos

    Melhorar a interface do usuário e a experiência do usuário.
    Adicionar mais funcionalidades ao chatbot, como suporte a diferentes tipos de mensagens ou interações mais complexas.
    Implementar persistência para o histórico de conversas.
    Adicionar testes unitários e de integração.
