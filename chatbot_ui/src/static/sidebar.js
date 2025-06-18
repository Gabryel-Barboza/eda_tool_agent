const sidebar = document.getElementById('sidebar');
const openSidebarBtn = document.getElementById('open-sidebar-btn');
const closeSidebarBtn = document.getElementById('close-sidebar-btn');
const historyList = document.getElementById('history-list');

let sessionChatHistory = [];

/**
 * Adiciona uma mensagem de usuário e a resposta do bot ao histórico da barra lateral.
 * O item de histórico exibido na barra lateral é o resumo da mensagem do usuário.
 * @param {string} userMessage - A mensagem enviada pelo usuário.
 * @param {string} botReply - A resposta recebida do bot.
 */
window.updateSidebarHistory = (userMessage, botReply) => {
  // Armazena a troca completa de mensagens
  const conversationTurn = {
    user: userMessage,
    bot: botReply,
    timestamp: new Date().toLocaleTimeString('pt-BR')
  };
  sessionChatHistory.unshift(conversationTurn); // Adiciona ao início do array para os mais recentes aparecerem primeiro

  const listItem = document.createElement('li');
  listItem.classList.add('history-item');

  // Cria um elemento de parágrafo para a mensagem do usuário
  const userMsgText = document.createElement('p');
  userMsgText.textContent = userMessage.length > 30 ? userMessage.substring(0, 30) + '...' : userMessage;
  userMsgText.classList.add('font-medium');
  listItem.appendChild(userMsgText);

  // Adiciona um texto menor para a resposta do bot para contexto
  const botReplyPreview = document.createElement('p');
  botReplyPreview.textContent = botReply.length > 40 ? botReply.substring(0, 40) + '...' : botReply;
  botReplyPreview.classList.add('text-gray-400', 'text-xs', 'mt-1');
  listItem.appendChild(botReplyPreview);


  // Adiciona um atributo de dados para vincular ao índice completo do histórico
  // Se o array for sempre adicionado no início (unshift), o índice precisaria ser ajustado ou o array invertido.
  // Por simplicidade, vamos usar o índice do unshift (0 para o mais recente).
  listItem.dataset.index = 0; // O item mais recente estará sempre no índice 0 após unshift

  // Adiciona um evento de clique para (simular) o carregamento da conversa completa
  listItem.addEventListener('click', (event) => {
    const index = parseInt(event.currentTarget.dataset.index, 10);
    const selectedConversation = sessionChatHistory[index];

    if (selectedConversation) {
      console.log('Carregando histórico da conversa:', selectedConversation);
      alert(`Você: ${selectedConversation.user}\nAgente: ${selectedConversation.bot}`);
    }
  });

  historyList.prepend(listItem); // Adiciona o item mais recente ao topo da lista de exibição
};

// Função para abrir a barra lateral
openSidebarBtn.addEventListener('click', () => {
  sidebar.classList.remove('translate-x-full');
  sidebar.classList.add('open');
});

// Função para fechar a barra lateral
closeSidebarBtn.addEventListener('click', () => {
  sidebar.classList.add('translate-x-full');
  sidebar.classList.remove('open');
});

// Fecha a barra lateral se clicar fora dela
document.addEventListener('click', (event) => {
  if (!sidebar.contains(event.target) && !openSidebarBtn.contains(event.target) && sidebar.classList.contains('open')) {
    sidebar.classList.add('translate-x-full');
    sidebar.classList.remove('open');
  }
});

// Impede o fechamento ao clicar dentro da barra lateral
sidebar.addEventListener('click', (event) => {
  event.stopPropagation();
});
