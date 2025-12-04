
from datapizza.clients.openai import OpenAIClient
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

def get_client(model_name: str = "gpt-4.1-mini") -> OpenAIClient:
    """Get an OpenAI client instance with the specified model.

    Args:
        model_name (str, optional): The name of the model to use. Defaults to "gpt-4.1-mini".

    Returns:
        OpenAIClient: An instance of OpenAIClient configured with the specified model.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAIClient(api_key=openai_api_key, model=model_name)
    return client