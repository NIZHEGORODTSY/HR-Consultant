from openai import OpenAI
from _back._MODELS import reader
from generate_prompt import get_final_prompt


def get_ai_answer():
    message_history = []
    cnt = 0
    is_first_message = True
    reader.read_config()
    API_KEY = reader.get_param_value('api-key')
    client = OpenAI(api_key=API_KEY, base_url="https://llm.t1v.scibox.tech/v1")
    ai_answer = ''
    user_input = input()
    cnt += 1
    if cnt >= 2:
        is_first_message = False
    message_history.append('user: ' + user_input)
    CONTEXT = get_final_prompt(username='Виктор Геннадьевич', message_history=message_history,
                               is_first_message=is_first_message)
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
                        ai_answer += event.chunk.choices[0].delta.content
                        # print(event.chunk.choices[0].delta.content, end="", flush=True)

                elif event.type == 'content.delta' and hasattr(event, 'delta'):
                    # Обрабатываем content.delta события
                    if event.delta and hasattr(event.delta, 'content') and event.delta.content:
                        pass
                        # print(event.delta.content, end="", flush=True)
            message_history.append('ai: ' + ai_answer)
        return ai_answer


    except Exception as e:
        print(f"Error: {e}")
