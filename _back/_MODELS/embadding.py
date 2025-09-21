from openai import OpenAI
from _MODELS import reader

reader.read_config()
API_KEY = reader.get_param_value('api-key')
client = OpenAI(api_key=API_KEY, base_url="https://llm.t1v.scibox.tech/v1")

emb = client.embeddings.create(
    model="bge-m3",
    input=[
        "Что такое квантовая запутанность?",
        "Квантовая запутанность — это корреляция состояний частиц",
    ],
)

print(len(emb.data), emb.data[0].embedding, sep='\n\n\n')


