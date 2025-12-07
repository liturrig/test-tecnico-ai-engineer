import json
import csv
from difflib import SequenceMatcher
from pathlib import Path
from typing import Callable, Literal, TypeVar

from datapizza.agents import Agent
from datapizza.tools import tool
from tenacity import retry, stop_after_attempt

from src.evaluation import MAPPINGS_DIR
from src.ai.clients import get_grok_client
from src.ai.prompts.hard_engine import SYSTEM_PROMPT

DISTANCES_FILE = Path(__file__).parent.parent.parent.parent / "Dataset" / "knowledge_base" / "misc" / "Distanze.csv"


T = TypeVar("T")


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


def _lookup_values(
    mapping: dict[str, list[T]],
    name: str,
    *,
    find_most_similar_feature: bool = True,
) -> list[T]:
    normalized = name.strip().lower()
    for key, values in mapping.items():
        if key.lower() == normalized:
            return values

    if find_most_similar_feature:
        similar_key = _find_most_similar_key(mapping, normalized)
        if similar_key is not None:
            return mapping[similar_key]
    return []


def _lookup_ids(
    mapping: dict[str, list[int]], name: str, find_most_similar_feature: bool = True
) -> list[int]:
    return _lookup_values(
        mapping, name, find_most_similar_feature=find_most_similar_feature
    )


def _build_dish_ids_response(label: str, value: str, mapping_filename: str) -> str:
    mapping = _load_mapping(mapping_filename)
    ids = _lookup_ids(mapping, value)
    return json.dumps({label: value, "dish_ids": ids})


def _match_mapping_entry(
    mapping: dict[str, T], name: str
) -> tuple[str | None, T | None]:
    normalized = name.strip().lower()
    for key, value in mapping.items():
        if key.lower() == normalized:
            return key, value

    similar_key = _find_most_similar_key(mapping, normalized)
    if similar_key is not None:
        return similar_key, mapping[similar_key]

    return None, None


def _operation_matches(operation: str, left: int, right: int) -> bool:
    comparators: dict[str, Callable[[int, int], bool]] = {
        "eq": lambda candidate, reference: candidate == reference,
        "ne": lambda candidate, reference: candidate != reference,
        "g": lambda candidate, reference: candidate > reference,
        "ge": lambda candidate, reference: candidate >= reference,
        "l": lambda candidate, reference: candidate < reference,
        "le": lambda candidate, reference: candidate <= reference,
    }

    try:
        return comparators[operation](left, right)
    except KeyError as exc:
        raise ValueError(
            f"Unsupported operation: {operation}. Use: eq, ne, g, ge, l, le"
        ) from exc


def _collect_dish_ids_for_techniques(
    techniques: list[str],
    technique_mapping: dict[str, list[int]],
    *,
    allow_fuzzy_lookup: bool = True,
) -> set[int]:
    dish_ids: set[int] = set()
    for technique in techniques:
        technique_ids = _lookup_ids(
            technique_mapping,
            technique,
            find_most_similar_feature=allow_fuzzy_lookup,
        )
        dish_ids.update(technique_ids)
    return dish_ids


@tool
def get_ingredient_dish_ids(ingredient: str) -> str:
    """Return dish ids associated with the provided ingredient."""

    return _build_dish_ids_response("ingredient", ingredient, "ingredient_to_dishes.json")


@tool
def get_technique_dish_ids(technique: str) -> str:
    """Return dish ids associated with the provided technique."""

    return _build_dish_ids_response("technique", technique, "technique_to_dishes.json")


@tool
def get_planet_dish_ids(planet: str) -> str:
    """Return dish ids associated with the provided planet name."""

    return _build_dish_ids_response("planet", planet, "planet_to_dishes.json")


@tool
def get_restaurant_dish_ids(restaurant: str) -> str:
    """Return dish ids associated with the provided restaurant name."""

    return _build_dish_ids_response(
        "restaurant", restaurant, "restaurant_to_dishes.json"
    )


def _lookup_list(
    mapping: dict[str, list[str]], name: str, find_most_similar_feature: bool = True
) -> list[str]:
    """Lookup a list of strings (e.g., technique names) from a mapping."""

    return _lookup_values(
        mapping, name, find_most_similar_feature=find_most_similar_feature
    )


@tool
def get_technique_from_category(category: str) -> str:
    """Return technique names associated with the provided category name."""

    mapping = _load_mapping("category_to_techniques.json")
    techniques = _lookup_list(mapping, category)
    return json.dumps({"category": category, "techniques": techniques})


@tool
def get_chef_licence_dish_ids(licence_name: Literal["Psionica (P)", "Temporale (t)", "Gravitazionale (G)", "Antimateria (e+)", "Magnetica (Mx)", "Quantistica (Q)", "Luce (c)", "Livello di Sviluppo Tecnologico (LTK)"], licence_value: int, operation: str) -> str:
    """
    Return dish ids for chefs having a licence name and value based on the operation.
    
    Args:
        licence_name: Name of the licence (e.g., "Psionica (P)", "Quantistica (Q)")
        licence_value: The licence level value to compare
        operation: Comparison operation - "eq" (equal), "ne" (not equal), 
                   "g" (greater than), "ge" (greater or equal), 
                   "l" (less than), "le" (less or equal)
    
    Returns:
        JSON string with licence_name, licence_value, operation, and matching dish_ids
    """
    mapping = _load_mapping("skill_to_dishes.json")

    _, licence_data = _match_mapping_entry(mapping, licence_name)

    if licence_data is None:
        return json.dumps({
            "licence_name": licence_name, 
            "licence_value": licence_value, 
            "operation": operation,
            "dish_ids": []
        })
    
    # Collect dish IDs based on operation
    result_ids = set()
    
    for level_str, dish_ids in licence_data.items():
        level = int(level_str)

        if _operation_matches(operation, level, licence_value):
            result_ids.update(dish_ids)
    
    return json.dumps({
        "licence_name": licence_name,
        "licence_value": licence_value,
        "operation": operation,
        "dish_ids": sorted(list(result_ids))
    })


@tool
def get_dish_from_minimum_licence(licence_name: Literal["Psionica (P)", "Temporale (t)", "Gravitazionale (G)", "Antimateria (e+)", "Magnetica (Mx)", "Quantistica (Q)", "Luce (c)", "Livello di Sviluppo Tecnologico (LTK)"], licence_value: int, operation: str) -> str:
    """
    Data una determinata licenza e grado, restituisce gli identificativi dei piatti che richiedono tale licenza in base all'operazione specificata.
    
    Args:
        licence_name: Name of the licence (e.g., "Psionica (P)", "Quantistica (Q)")
        licence_value: The licence level value to compare
        operation: Comparison operation - "eq" (equal), "ne" (not equal), 
                   "g" (greater than), "ge" (greater or equal), 
                   "l" (less than), "le" (less or equal)
    
    Returns:
        JSON string with licence_name, licence_value, operation, techniques, and matching dish_ids
    """
    licence_mapping = _load_mapping("licence_to_techniques.json")
    technique_mapping = _load_mapping("technique_to_dishes.json")

    _, licence_data = _match_mapping_entry(licence_mapping, licence_name)

    if licence_data is None:
        return json.dumps({
            "licence_name": licence_name, 
            "licence_value": licence_value, 
            "operation": operation,
            "techniques": [],
            "dish_ids": []
        })
    
    # Collect techniques based on operation
    matching_techniques = []
    
    for level_str, techniques in licence_data.items():
        level = int(level_str)
        
        if _operation_matches(operation, level, licence_value):
            matching_techniques.extend(techniques)
    
    # Now lookup dish IDs for each technique
    result_ids = _collect_dish_ids_for_techniques(
        matching_techniques,
        technique_mapping,
        allow_fuzzy_lookup=False,
    )
    
    return json.dumps({
        "licence_name": licence_name,
        "licence_value": licence_value,
        "operation": operation,
        #"techniques": matching_techniques,
        "dish_ids": sorted(list(result_ids))
    })


@tool
def get_dishes_with_both_technique_categories(first_category: str, second_category: str) -> str:
    """
    Ritorna gli identificativi dei piatti che utilizzano almeno una tecnica da entrambe le categorie specificate.
    
    Args:
        first_category: First technique category name
        second_category: Second technique category name
    
    Returns:
        JSON string with both categories, their techniques, and dish_ids that have techniques from both
    """
    category_mapping = _load_mapping("category_to_techniques.json")
    technique_mapping = _load_mapping("technique_to_dishes.json")
    
    # Get techniques for first category
    first_techniques = _lookup_list(category_mapping, first_category)
    
    # Get techniques for second category
    second_techniques = _lookup_list(category_mapping, second_category)
    
    # Get dish IDs for each technique in both categories
    first_category_dishes = _collect_dish_ids_for_techniques(
        first_techniques, technique_mapping
    )
    second_category_dishes = _collect_dish_ids_for_techniques(
        second_techniques, technique_mapping
    )
    
    # Find intersection: dishes that have at least one technique from both categories
    dishes_with_both = first_category_dishes & second_category_dishes
    
    return json.dumps({
        "first_category": first_category,
        #"first_category_techniques": first_techniques,
        "second_category": second_category,
        #"second_category_techniques": second_techniques,
        "dish_ids": sorted(list(dishes_with_both))
    })


@tool
def get_dishes_within_distance(planet: str, max_distance: int) -> str:
    """
    Ritorna gli identificativi dei piatti provenienti da pianeti entro una distanza specificata (in anni luce) da un pianeta di riferimento.
    
    Args:
        planet: Reference planet name
        max_distance: Maximum distance in light years (inclusive)
    
    Returns:
        JSON string with planet, max_distance, nearby_planets, and dish_ids from those planets
    """
    # Load distances from CSV
    distances = {}
    with open(DISTANCES_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)[1:]  # Skip first column header "/"
        
        for row in reader:
            planet_name = row[0]
            distances[planet_name] = {}
            for i, distance_str in enumerate(row[1:]):
                distances[planet_name][headers[i]] = int(distance_str)
    
    # Find the reference planet (case-insensitive with fuzzy matching)
    planet_key, planet_distances = _match_mapping_entry(distances, planet)
    if planet_key is not None:
        planet = planet_key  # Use the original casing from the file
    
    if planet_distances is None:
        return json.dumps({
            "planet": planet,
            "max_distance": max_distance,
            "nearby_planets": [],
            "dish_ids": []
        })
    
    # Find planets within the distance range (including the reference planet itself)
    nearby_planets = [planet]  # Include the reference planet
    for other_planet, distance in planet_distances.items():
        if distance <= max_distance and other_planet != planet:
            nearby_planets.append(other_planet)
    
    # Load planet to dishes mapping
    planet_mapping = _load_mapping("planet_to_dishes.json")
    
    # Get dish IDs for all nearby planets
    result_ids = set()
    for nearby_planet in nearby_planets:
        planet_ids = _lookup_ids(planet_mapping, nearby_planet)
        result_ids.update(planet_ids)
    
    return json.dumps({
        "planet": planet,
        "max_distance": max_distance,
        #"nearby_planets": sorted(nearby_planets),
        "dish_ids": sorted(list(result_ids))
    })


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


@tool
def union_dish_ids(first_list: list[int], second_list: list[int]) -> str:
    """Return the union of two lists of dish ids (all unique ids from both lists)."""

    first_ids = set(_parse_ids(first_list, "first_list"))
    second_ids = set(_parse_ids(second_list, "second_list"))

    union = sorted(list(first_ids | second_ids))
    return json.dumps({"union": union})




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



def get_agent(system_prompt: str, model_name: str = "grok-4-1-fast-reasoning")-> Agent:
    """Crea e restituisce l'agente configurato."""

    agent = Agent(
        name="assistant",
        client=get_grok_client(model_name=model_name),
        system_prompt=system_prompt,
        tools=[
            get_technique_from_category,
            get_ingredient_dish_ids,
            get_technique_dish_ids,
            get_planet_dish_ids,
            get_restaurant_dish_ids,
            get_chef_licence_dish_ids,
            get_dish_from_minimum_licence,
            get_dishes_with_both_technique_categories,
            get_dishes_within_distance,
            intersect_dish_ids,
            subtract_dish_ids,
            union_dish_ids,
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




