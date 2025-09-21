from _MODELS.conn.conn import client
from _MODELS.tools.generate_prompt import get_final_prompt



def get_ai_answer(user_input: str, message_history: list = []) -> str:
    is_first_message = True
    cnt = 0
    ai_answer = ''
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
            message_history.append('ai: ' + ai_answer)
        return ai_answer


    except Exception as e:
        print(f"Error: {e}")

# print(get_ai_answer(input()))
