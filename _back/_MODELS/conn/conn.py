from openai import OpenAI
from _MODELS.reader import reader

reader.read_config()
API_KEY = reader.get_param_value('api-key')
client = OpenAI(api_key=API_KEY, base_url="https://llm.t1v.scibox.tech/v1")
