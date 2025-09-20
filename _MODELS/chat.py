from openai import OpenAI
from _MODELS import reader
from generate_prompt import get_final_prompt

reader.read_config()
API_KEY = reader.get_param_value('api-key')
client = OpenAI(api_key="sk-E0EfpcLN3QLegOcEozZBJA", base_url="https://llm.t1v.scibox.tech/v1")

CONTEXT = get_final_prompt(username='Виктор Геннадьевич')
while True:
    user_input = input()
    try:
        with client.chat.completions.stream(
                model="Qwen2.5-72B-Instruct-AWQ",
                messages=[
                    {"role": "system", "content": CONTEXT},
                    {"role": "user", "content": user_input},
                ],
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

            print()

    except Exception as e:
        print(f"Error: {e}")
