from typing import List

from tenacity import retry, stop_after_attempt

from src.ai.models.menu_classifier import ClassificationResult
from src.ai.prompts.menu_classifier import INPUT_PROMPT, SYSTEM_PROMPT
from src.ai.clients import get_openai_client


@retry(stop=stop_after_attempt(3))
def classify_menu(text_extracted: dict, 
                  model_name: str = "gpt-4.1", 
                  system_prompt: str = SYSTEM_PROMPT, 
                  input_prompt: str = INPUT_PROMPT) -> List[str]:
    menus = {}

    client = get_openai_client(model_name=model_name)
    for file_name, menu_text in text_extracted.items():
        result = client.structured_response(system_prompt=system_prompt,
                                            output_cls=ClassificationResult,
                                            input=input_prompt.format(menu_text=menu_text))
        menus[file_name] = result.structured_data[0].menu_classification

    return menus
