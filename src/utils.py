import json
from pathlib import Path

def read_json(file_path: Path) -> dict:
    """
    Read a JSON file and return its content as a dictionary.

    Args:
        file_path (Path): Path to the JSON file. 
    
    Returns:
        dict: The content of the JSON file as a dictionary.
    """

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def write_json(data: dict, file_path: Path) -> None:
    """
    Write a dictionary to a JSON file.

    Args:
        data (dict): The data to write to the JSON file.
        file_path (Path): Path to the JSON file.
    """

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)