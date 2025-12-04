import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple, Union

def _collect_dishes(extracted_info: object) -> Iterable[Dict]:
    """
    Normalize the raw extracted info into a flat iterable of dish dictionaries.
    Supports both the legacy dict format ({dish_name: {...}}) and
    the current format (list of restaurants with "dishes" entries).
    """
    if isinstance(extracted_info, dict):
        for dish_name, info in extracted_info.items():
            yield {
                "dish_name": dish_name,
                "ingredients": info.get("ingredients", []),
                "techniques": info.get("techniques", []),
            }
    elif isinstance(extracted_info, list):
        for restaurant in extracted_info:
            for dish in restaurant.get("dishes", []):
                yield dish
    else:
        raise ValueError("Unsupported extracted_info format. Expected dict or list.")


def create_mappings(extracted_info: Union[list,dict], dish_mapping: dict) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """Create technique and ingredient mappings from extracted_info.json"""
    
    # Initialize dictionaries with automatic list creation
    technique_to_dishes: Dict[str, List[str]] = defaultdict(list)
    ingredient_to_dishes: Dict[str, List[str]] = defaultdict(list)
    
    # Iterate through dishes regardless of the input structure
    for dish in _collect_dishes(extracted_info):
        dish_name = dish.get("dish_name")
        if not dish_name:
            continue
        dish_id = dish_mapping.get(dish_name, dish_name)
        
        for technique in dish.get("techniques", []):
            if dish_id not in technique_to_dishes[technique]:
                technique_to_dishes[technique].append(dish_id)
        
        for ingredient in dish.get("ingredients", []):
            if dish_id not in ingredient_to_dishes[ingredient]:
                ingredient_to_dishes[ingredient].append(dish_id)
    
    print(f"Created mappings:")
    print(f"- Techniques: {len(technique_to_dishes)} unique techniques")
    print(f"- Ingredients: {len(ingredient_to_dishes)} unique ingredients")

    return ingredient_to_dishes, technique_to_dishes