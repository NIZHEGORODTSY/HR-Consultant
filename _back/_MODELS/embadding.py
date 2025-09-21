from openai import OpenAI
from conn.conn import client


def get_embadding():
    emb = client.embeddings.create(
        model="bge-m3",
        input=[
            "Что такое квантовая запутанность?",
            "Квантовая запутанность — это корреляция состояний частиц",
        ],
        temperatue=0.7
    )

    answer = emb.data[0].embedding
    return answer


def form_prompt_for_bge():
    pass
