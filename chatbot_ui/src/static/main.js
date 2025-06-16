const chatbox = document.getElementById('chatbox');
const messageForm = document.getElementById('message-form');
const messageInput = document.getElementById('message-input');
const typingIndicator = document.getElementById('typing-indicator');

function addMessage(message, sender) {
  const messageDiv = document.createElement('div');
  messageDiv.classList.add('flex', sender === 'user' ? 'justify-end' : 'justify-start');

  const messageBubble = document.createElement('div');
  messageBubble.classList.add('p-3', 'rounded-lg', 'max-w-md', 'text-sm');
  messageBubble.classList.add(sender === 'user' ? 'bg-gray-700' : 'bg-blue-500', 'text-white');

  if (sender === 'bot') {
    const htmlContent = marked.parse(message);
    messageBubble.innerHTML = htmlContent;
    messageBubble.classList.add('markdown-content');
  } else {
    messageBubble.textContent = message;
  }

  messageDiv.appendChild(messageBubble);
  chatbox.appendChild(messageDiv);
  chatbox.scrollTop = chatbox.scrollHeight;
}

// Lidar com o envio do formulário
messageForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const message = messageInput.value.trim();
  if (!message) return;

  addMessage(message, 'user');
  messageInput.value = '';
  typingIndicator.classList.remove('hidden');

  try {
    const response = await fetch('/send_message', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: message })
    });

    if (!response.ok) {
      throw new Error(`Erro na comunicação com o servidor: ${response.statusText}`);
    }

    const data = await response.json();

    addMessage(data.reply, 'bot');

    if (typeof window.updateSidebarHistory === 'function') {
      window.updateSidebarHistory(message, data.reply);
    }

  } catch (error) {
    console.error('Erro:', error);
    addMessage('Desculpe, não consegui me conectar ao agente. Verifique o console para mais detalhes.', 'bot');
  } finally {
    typingIndicator.classList.add('hidden');
  }
});