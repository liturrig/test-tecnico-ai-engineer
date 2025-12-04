from pydantic import BaseModel
from src.ai.clients import get_client
from src.ai.models.extractor import Restaurant
from src.ai.prompts.simple_extractor import EXTRACTOR_INPUT_PROMPT, EXTRACTOR_SYSTEM_PROMPT


def extraction_call(text: str, 
                    model_name: str = "gpt-4.1-mini",
                    system_prompt: str = EXTRACTOR_SYSTEM_PROMPT,
                    input_prompt: str = EXTRACTOR_INPUT_PROMPT, 
                    output_cls: BaseModel = Restaurant):
    """Make a structured response call to the OpenAI client.

    Args:
        client (OpenAIClient): The OpenAI client instance.
        system_prompt (str): The system prompt for the extraction task.
        input_text (str): The input text to be processed.
        output_cls: The Pydantic model class for structured output.

    Returns:
        The structured response from the OpenAI client.
    """

    client = get_client(model_name=model_name)

    result = client.structured_response(
        system_prompt=system_prompt,
        output_cls=output_cls,
        input=input_prompt.format(menu_text=text)
    )

    return result

