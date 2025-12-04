from datapizza.clients.openai import OpenAIClient
from datapizza.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

@tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"

client = OpenAIClient(api_key=openai_api_key)
agent = Agent(name="assistant", client=client, tools = [get_weather])

response = agent.run("What is the weather in Rome?")