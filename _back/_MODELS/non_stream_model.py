from openai import OpenAI
from _MODELS import reader

reader.read_config()
API_KEY = reader.get_param_value('api-key')
# Вариант с доменом без порта (HTTPS):
BASE_URL = "https://llm.t1v.scibox.tech/v1"
# Альтернатива с IP:порт
# BASE_URL = "http://176.119.5.23:4000/v1"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

resp = client.chat.completions.create(
    model="Qwen2.5-72B-Instruct-AWQ",
    messages=[
        {"role": "system", "content": "Ты авторитетный зек"},
        {"role": "user", "content": "Расскажи 3 тюремных анекдота"},
    ],
    temperature=0.7,
    top_p=0.9,
    max_tokens=256,
)

print(resp.choices[0].message.content)