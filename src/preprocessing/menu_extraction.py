
from src.ai.agents.extractor import extraction_call
from src.ai.prompts.menu_advanced_extractor import EXTRACTOR_SYSTEM_PROMPT


def extract_structured_info_from_menus(documents: dict, model_name: str = "gpt-4.1") -> list:
    """
    Extract information from a set of menu documents.

    Args:
        documents (dict): A dictionary where keys are document identifiers and values are menu texts.
        model_name (str, optional): The name of the model to use for extraction. Defaults to "grok-4-1-fast-reasoning".

    Returns:
        dict: A dictionary containing extracted information from the menus.
    """
    restaurants = []

    for key, menu_text in documents.items():
        result = extraction_call(text=menu_text, model_name=model_name)
        print(f"Info from document: {key} has been extracted.")
        restaurants.append(result.structured_data[0].model_dump())
    
    return restaurants


def extract_unstructured_info_from_menus(documents: dict, ingredients: list[str], techniques: list[str], model_name: str = "gpt-4.1") -> dict:
    """
    Extract information from a set of menu documents using provided ingredients and techniques.
    Args:
        documents (dict): A dictionary where keys are document identifiers and values are menu texts.
        ingredients (list[str]): A list of ingredients to consider during extraction.
        techniques (list[str]): A list of techniques to consider during extraction.
        model_name (str, optional): The name of the model to use for extraction. Defaults to "gpt-4.1".
    Returns:
        dict: A dictionary containing extracted information from the menus.
    """

    restaurants = []

    list_ingredients_str = "\n".join(f"- {ingredient}" for ingredient in ingredients)
    list_techniques_str = "\n".join(f"- {technique}" for technique in techniques)

    system_prompt = EXTRACTOR_SYSTEM_PROMPT.format(
        list_ingredients_str=list_ingredients_str,
        list_techniques_str=list_techniques_str
    )

    for key, menu_text in documents.items():
        result = extraction_call(text=menu_text,system_prompt=system_prompt, model_name=model_name)
        print(f"Info from document: {key} has been extracted.")
        restaurants.append(result.structured_data[0].model_dump())
    
    return restaurants

def filter_structured_or_unstructured_menus(documents: dict, classifications: dict, structured: bool = True) -> dict:
    """
    Filter menus based on their classification as structured or unstructured.

    Args:
        documents (dict): A dictionary where keys are document identifiers and values are menu texts.
        classifications (dict): A dictionary where keys are document identifiers and values are their classifications ("structured" or "unstructured").
        structured (bool, optional): If True, filter for structured menus; if False, filter for unstructured menus. Defaults to True.       
    Returns:
        list[dict]: A list of dictionaries containing filtered menu texts.
    """
    filtered_menus = {}
    target_classification = "structured" if structured else "unstructured"

    for doc_name, classification in classifications.items():
        if classification == target_classification:
            filtered_menus[doc_name] = documents[doc_name]
    
    return filtered_menus

def extract_ingredients_and_techniques_from_menus(documents: list) -> tuple[list[str], list[str]]:
    """
    Extract unique ingredients and techniques from a set of menu documents.

    Args:
        documents (dict): A dictionary where keys are document identifiers and values are menu texts.

    Returns:
        tuple[list[str], list[str]]: A tuple containing two lists - one for unique ingredients and another for unique techniques.
    """
    list_ingredients = []
    list_techniques = []

    for menu_text in documents:
        for dish in menu_text.get("dishes", []):
            list_ingredients.extend(dish.get("ingredients", []))
            list_techniques.extend(dish.get("techniques", []))

    list_ingredients = list(set(list_ingredients))
    list_techniques = list(set(list_techniques))

    return list_ingredients, list_techniques

def extract_info_from_menus(documents: dict, classifications: dict, model_name: str = "gpt-4.1") -> dict:
    """
    Extract information from menus based on their classification.

    Args:
        documents (dict): A dictionary where keys are document identifiers and values are menu texts.
        classifications (dict): A dictionary where keys are document identifiers and values are their classifications ("structured" or "unstructured").
        model_name (str, optional): The name of the model to use for extraction. Defaults to "grok-4-1-fast-reasoning".

    Returns:
        dict: A dictionary containing extracted information from the menus.
    """
    structured_menus = filter_structured_or_unstructured_menus(documents, classifications, structured=True)
    unstructured_menus = filter_structured_or_unstructured_menus(documents, classifications, structured=False)

    extracted_info = []

    if structured_menus:
        print("Extracting info from structured menus...")
        extracted_info = extract_structured_info_from_menus(structured_menus, model_name=model_name)
    
    ingredients, techniques = extract_ingredients_and_techniques_from_menus(extracted_info)

    if unstructured_menus:
        print("Extracting info from unstructured menus...") 
        extracted_unstructured_info = extract_unstructured_info_from_menus(
            unstructured_menus,
            ingredients=ingredients,
            techniques=techniques,
            model_name=model_name
        )
        extracted_info.extend(extracted_unstructured_info)

    return extracted_info   


    