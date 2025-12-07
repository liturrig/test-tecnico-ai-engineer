import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple, Union
from difflib import SequenceMatcher


def _find_most_similar_dish(dish_mapping: dict, dish_name: str) -> str | None:
    """Find the most similar dish name in dish_mapping using fuzzy matching."""
    if not dish_name:
        return None
    
    normalized_name = dish_name.strip().lower()
    best_match = None
    best_score = 0.0
    
    for key in dish_mapping.keys():
        score = SequenceMatcher(None, normalized_name, key.lower()).ratio()
        if score > best_score:
            best_match = key
            best_score = score
    
    # Return the match only if similarity is above a threshold (e.g., 0.6)
    return best_match if best_score > 0.6 else None

def _collect_technique_ingredient(extracted_info: object) -> Iterable[Dict]:
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




def create_mappings_technique_ingredient(extracted_info: Union[list,dict], dish_mapping: dict) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """Create technique and ingredient mappings from extracted_info.json"""
    
    # Initialize dictionaries with automatic list creation
    technique_to_dishes: Dict[str, List[str]] = defaultdict(list)
    ingredient_to_dishes: Dict[str, List[str]] = defaultdict(list)
    
    # Iterate through dishes regardless of the input structure
    for dish in _collect_technique_ingredient(extracted_info):
        dish_name = dish.get("dish_name").replace('’', "'")
                                                  
        if not dish_name:
            continue
        
        dish_id = dish_mapping.get(dish_name, None)
        
        # If no exact match, try fuzzy matching
        if dish_id is None:
            similar_dish = _find_most_similar_dish(dish_mapping, dish_name)
            if similar_dish:
                dish_id = dish_mapping[similar_dish]
                print(f"Fuzzy match: '{dish_name}' -> '{similar_dish}' (ID: {dish_id})")
            else:
                continue  # Skip dishes that can't be matched
        
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


def _collect_dishes_planets_restaurant_skills(extracted_info: object) -> Iterable[Dict]:
    """
    Normalize the raw extracted info into a flat iterable of dish dictionaries
    with planet_name, restaurant_name and skills information.
    Supports list format with restaurant-level metadata.
    """
    if isinstance(extracted_info, list):
        for restaurant in extracted_info:
            planet_name = restaurant.get("planet_name")
            restaurant_name = restaurant.get("restaurant_name")
            skills = restaurant.get("skills", [])
            for dish in restaurant.get("dishes", []):
                yield {
                    **dish,
                    "planet_name": planet_name,
                    "restaurant_name": restaurant_name,
                    "skills": skills
                }
    else:
        raise ValueError("Unsupported extracted_info format. Expected list of restaurants.")
    
def create_mappings_planets_restaurant_skills(extracted_info: Union[list,dict], dish_mapping: dict) -> Tuple[Dict[str, List[int]], Dict[str, List[int]], Dict[str, Dict[int, List[int]]]]:
    """
    Create planet, restaurant and skill mappings from extracted_info.json
    
    Returns:
        - planet_to_dishes: Dict[str, List[int]] - planet_name -> list of dish IDs
        - restaurant_to_dishes: Dict[str, List[int]] - restaurant_name -> list of dish IDs
        - skill_to_dishes: Dict[str, Dict[int, List[int]]] - skill_name -> {skill_level: [dish IDs]}
    """
    
    # Initialize dictionaries with automatic list creation
    planet_to_dishes: Dict[str, List[int]] = defaultdict(list)
    restaurant_to_dishes: Dict[str, List[int]] = defaultdict(list)
    skill_to_dishes: Dict[str, Dict[int, List[int]]] = defaultdict(lambda: defaultdict(list))
    
    # Iterate through dishes with metadata
    for dish_data in _collect_dishes_planets_restaurant_skills(extracted_info):
        dish_name = dish_data.get("dish_name").replace('’', "'")
        if not dish_name:
            continue

        dish_id = dish_mapping.get(dish_name, None)
        
        # If no exact match, try fuzzy matching
        if dish_id is None:
            similar_dish = _find_most_similar_dish(dish_mapping, dish_name)
            if similar_dish:
                dish_id = dish_mapping[similar_dish]
                print(f"Fuzzy match: '{dish_name}' -> '{similar_dish}' (ID: {dish_id})")
            else:
                continue  # Skip dishes that can't be matched
        
        # Map planet -> dishes
        planet_name = dish_data.get("planet_name")
        if planet_name and dish_id not in planet_to_dishes[planet_name]:
            planet_to_dishes[planet_name].append(dish_id)
        
        # Map restaurant -> dishes
        restaurant_name = dish_data.get("restaurant_name")
        if restaurant_name and dish_id not in restaurant_to_dishes[restaurant_name]:
            restaurant_to_dishes[restaurant_name].append(dish_id)
        
        # Map skill -> {level: dishes}
        skills = dish_data.get("skills", [])
        for skill in skills:
            skill_name = skill.get("skill_name")
            skill_level = skill.get("skill_level")
            if skill_name and skill_level is not None:
                if dish_id not in skill_to_dishes[skill_name][skill_level]:
                    skill_to_dishes[skill_name][skill_level].append(dish_id)
    
    # Convert defaultdict to regular dict for cleaner serialization
    skill_to_dishes_dict = {
        skill_name: dict(levels) 
        for skill_name, levels in skill_to_dishes.items()
    }
    
    print(f"Created mappings:")
    print(f"- Planets: {len(planet_to_dishes)} unique planets")
    print(f"- Restaurants: {len(restaurant_to_dishes)} unique restaurants")
    print(f"- Skills: {len(skill_to_dishes_dict)} unique skills")
    total_skill_levels = sum(len(levels) for levels in skill_to_dishes_dict.values())
    print(f"  Total skill-level combinations: {total_skill_levels}")

    return planet_to_dishes, restaurant_to_dishes, skill_to_dishes_dict