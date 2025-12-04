from typing import List

from src.ai.models.classifier import ClassificationResult
from src.ai.prompts.classifier import INPUT_PROMPT, SYSTEM_PROMPT
from src.ai.clients import get_client


def classify_menu(text_extracted: dict, 
                  model_name: str = "gpt-4.1-mini", 
                  system_prompt: str = SYSTEM_PROMPT, 
                  input_prompt: str = INPUT_PROMPT) -> List[str]:
    menus = {}

    client = get_client(model_name=model_name)
    for file_name, menu_text in text_extracted.items():
        result = client.structured_response(system_prompt=system_prompt,
                                            output_cls=ClassificationResult,
                                            input=input_prompt.format(menu_text=menu_text))
        menus[file_name] = result.structured_data[0].menu_classification

    return menus
