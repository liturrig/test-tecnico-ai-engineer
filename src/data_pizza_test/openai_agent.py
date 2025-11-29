from datapizza.clients.openai import OpenAIClient
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAIClient(api_key=openai_api_key)
result = client.invoke("Hi, how are u?")
print(result.text)