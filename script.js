function showTypingAnimation() {
    const chatbox = document.getElementById('chatbox');
    const typing = document.createElement('p');
    typing.id = 'typing';
    typing.innerHTML = '<i>AI is typing...</i>';
    chatbox.appendChild(typing);
    chatbox.scrollTop = chatbox.scrollHeight;
  }
  
  function removeTypingAnimation() {
    const typing = document.getElementById('typing');
    if (typing) typing.remove();
  }
  
  async function sendMessage() {
    const input = document.getElementById('userInput');
    const chatbox = document.getElementById('chatbox');
    const userText = input.value.trim();
  
    if (!userText) return;
  
    chatbox.innerHTML += `<p><strong>You:</strong> ${userText}</p>`;
    input.value = "";
    showTypingAnimation();
  
    const response = await fetch('/ask', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ message: userText })
    });
  
    const result = await response.json();
    removeTypingAnimation();
    chatbox.innerHTML += `<p><strong>AI:</strong> ${result.reply}</p>`;
    chatbox.scrollTop = chatbox.scrollHeight;
  }
  