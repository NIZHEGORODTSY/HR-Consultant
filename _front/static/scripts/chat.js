document.addEventListener('DOMContentLoaded', function() {
            const chatMessages = document.getElementById('chatMessages');
            const messageInput = document.getElementById('messageInput');
            const sendButton = document.getElementById('sendButton');

            // Функция отправки сообщения
            async function sendMessage() {
                const message = messageInput.value.trim();
                if (message) {
                    // Добавляем сообщение пользователя
                    addMessage(message, 'user');

                    // Очищаем поле ввода
                    messageInput.value = '';

                    const data = {
                        "message": message
                    }
                    console.log(message)
                    try {
                        const response = await fetch('http://127.0.0.1:5001/get_answer', {
                          method: 'POST',
                          headers: {
                            'Content-Type': 'application/json',
                          },
                          body: JSON.stringify(data)
                        });

                        const result = await response.json();
                        console.log(result);
                        addMessage(result.answer, 'ai');
                        
                    } catch (error) {
                        addMessage(error, 'ai');
                      }

                }
            }

            // Функция добавления сообщения в чат
            function addMessage(text, sender) {
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message');
                messageDiv.classList.add(sender + '-message');

                const messageText = document.createElement('p');
                messageText.innerHTML = text;

                const messageTime = document.createElement('div');
                messageTime.classList.add('message-time');

                // Текущее время
                const now = new Date();
                const time = now.getHours() + ':' + (now.getMinutes() < 10 ? '0' : '') + now.getMinutes();
                messageTime.textContent = time;

                messageDiv.appendChild(messageText);
                messageDiv.appendChild(messageTime);

                chatMessages.appendChild(messageDiv);

                // Прокрутка к последнему сообщению
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            // Обработчики событий
            sendButton.addEventListener('click', sendMessage);

            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            });

            // Быстрые действия
            document.querySelectorAll('.quick-action').forEach(action => {
                action.addEventListener('click', function() {
                    const text = this.textContent;
                    messageInput.value = text;
                    sendMessage();
                });
            });
        });