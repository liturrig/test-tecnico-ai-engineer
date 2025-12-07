
from datapizza.clients.openai import OpenAIClient
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

def get_grok_client(model_name: str = "grok-4-1-fast-reasoning") -> OpenAIClient:
    """Get an OpenAI client instance with the specified model.

    Args:
        model_name (str, optional): The name of the model to use. Defaults to "grok-4-1-fast-reasoning".
    Returns:
        OpenAIClient: An instance of OpenAIClient configured with the specified model.
    """
    grok_api_key = os.getenv("GROK_API_KEY")
    client = OpenAIClient(api_key=grok_api_key, model=model_name, base_url="https://api.x.ai/v1")
    return client


def get_openai_client(model_name: str = "gpt-4.1") -> OpenAIClient:
    """Get an OpenAI client instance with the specified model.

    Args:
        model_name (str, optional): The name of the model to use. Defaults to "gpt-4.1".
    Returns:
        OpenAIClient: An instance of OpenAIClient configured with the specified model.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAIClient(api_key=openai_api_key, model=model_name)
    return client