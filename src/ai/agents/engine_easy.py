import json
from difflib import SequenceMatcher
from pathlib import Path

from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient
from datapizza.tools import tool
from tenacity import retry, stop_after_attempt

from src.evaluation import MAPPINGS_DIR
from src.ai.clients import get_grok_client
from src.ai.prompts.easy_medium_engine import SYSTEM_PROMPT




def _load_mapping(filename: str) -> dict:
    with open(MAPPINGS_DIR / filename, "r", encoding="utf-8") as mapping_file:

        return json.load(mapping_file)


def _find_most_similar_key(mapping: dict, normalized_name: str) -> str | None:
    """Return the key whose normalized form is closest to normalized_name."""

    best_key = None
    best_score = 0.0
    for key in mapping:
        score = SequenceMatcher(None, normalized_name, key.lower()).ratio()
        if score > best_score:
            best_key = key
            best_score = score
    return best_key


def _lookup_ids(mapping: dict, name: str) -> list[int]:
    normalized = name.strip().lower()
    for key, values in mapping.items():
        if key.lower() == normalized:
            return values

    similar_key = _find_most_similar_key(mapping, normalized)
    if similar_key is not None:
        return mapping[similar_key]
    return []


@tool
def get_ingredient_dish_ids(ingredient: str) -> str:
    """Return dish ids associated with the provided ingredient."""

    mapping = _load_mapping("ingredient_to_dishes.json")
    ids = _lookup_ids(mapping, ingredient)
    return json.dumps({"ingredient": ingredient, "dish_ids": ids})


@tool
def get_technique_dish_ids(technique: str) -> str:
    """Return dish ids associated with the provided technique."""

    mapping = _load_mapping("technique_to_dishes.json")
    ids = _lookup_ids(mapping, technique)
    return json.dumps({"technique": technique, "dish_ids": ids})


def _parse_ids(candidate, argument_name: str) -> list[int]:
    """Ensure the provided candidate is a list of integers."""

    if not isinstance(candidate, list) or any(
        not isinstance(item, int) for item in candidate
    ):
        raise ValueError(
            f"Il parametro '{argument_name}' deve essere una lista di numeri interi."
        )

    return candidate


@tool
def intersect_dish_ids(first_list: list[int], second_list: list[int]) -> str:
    """Return the intersection of two lists of dish ids."""

    base_ids = _parse_ids(first_list, "first_list")
    compare_ids = set(_parse_ids(second_list, "second_list"))

    intersection = [dish_id for dish_id in base_ids if dish_id in compare_ids]
    return json.dumps({"intersection": intersection})


@tool
def subtract_dish_ids(first_list: list[int], second_list: list[int]) -> str:
    """Remove the ids of the second list from the first list."""

    base_ids = _parse_ids(first_list, "first_list")
    to_remove = set(_parse_ids(second_list, "second_list"))

    difference = [dish_id for dish_id in base_ids if dish_id not in to_remove]
    return json.dumps({"difference": difference})





def extract_dish_ids_from_response(response: str) -> set[int]:
    """Estrae gli identificativi dei piatti dalla risposta dell'agente."""

    start_index = response.find("[")
    end_index = response.rfind("]")

    if start_index == -1 or end_index == -1 or end_index <= start_index:
        raise ValueError(
            "Impossibile trovare una lista tra parentesi quadre nella risposta "
            f"dell'agente: {response}"
        )

    raw_list = response[start_index : end_index + 1]

    try:
        dish_ids = json.loads(raw_list)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Impossibile interpretare la lista estratta come JSON: {raw_list}"
        ) from exc

    if not isinstance(dish_ids, list):
        raise ValueError(f"La risposta dell'agente non contiene una lista valida: {raw_list}")

    normalized_ids: list[int] = []
    for item in dish_ids:
        if isinstance(item, int):
            normalized_ids.append(item)
            
        elif isinstance(item, str):
            normalized_ids.append(int(item.strip()))

    return set(normalized_ids)

def get_agent(system_prompt: str = SYSTEM_PROMPT, model_name: str = "grok-4-1-fast-reasoning")-> Agent:
    """Crea e restituisce l'agente configurato."""

    agent = Agent(
        name="assistant",
        client=get_grok_client(model_name=model_name),
        system_prompt=system_prompt,
        tools=[
            get_ingredient_dish_ids,
            get_technique_dish_ids,
            intersect_dish_ids,
            subtract_dish_ids,
        ]
    )
    return agent

@retry(stop=stop_after_attempt(3))
def query_dish_ids(question: str, agent: Agent) -> set[int]:
    """Esegue la domanda con l'agente e restituisce il set di identificativi."""

    response = agent.run(question)

    raw_output = getattr(response, "text", response)
    if not isinstance(raw_output, str):
        raw_output = str(raw_output)

    extracted_ids = extract_dish_ids_from_response(raw_output)

    return extracted_ids




