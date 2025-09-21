from openai import OpenAI
from _MODELS import reader

reader.read_config()
API_KEY = reader.get_param_value('api-key')
client = OpenAI(api_key=API_KEY, base_url="https://llm.t1v.scibox.tech/v1")

try:
    with client.chat.completions.stream(
            model="Qwen2.5-72B-Instruct-AWQ",
            messages=[{"role": "user", "content": "Сделай краткое резюме книги Война и мир"}],
            max_tokens=1000,
    ) as stream:
        for event in stream:
            if event.type == 'chunk' and hasattr(event, 'chunk'):
                # Обрабатываем chunk события
                if (event.chunk and
                        event.chunk.choices and
                        event.chunk.choices[0].delta and
                        event.chunk.choices[0].delta.content):
                    print(event.chunk.choices[0].delta.content, end="", flush=True)

            elif event.type == 'content.delta' and hasattr(event, 'delta'):
                # Обрабатываем content.delta события
                if event.delta and hasattr(event.delta, 'content') and event.delta.content:
                    print(event.delta.content, end="", flush=True)

            elif event.type == 'message.completed':
                # Событие завершения сообщения
                print("\n\nГенерация завершена")

except Exception as e:
    print(f"Error: {e}")
