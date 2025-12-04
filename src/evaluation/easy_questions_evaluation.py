import csv
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
from datapizza.agents import Agent
import pandas as pd

from src.ai.agents.engine import query_dish_ids




def _parse_result(result_value: str) -> Set[int]:
    """Parse a comma-separated string of integers into a set of integers.

    Args:
        result_value (str): A string containing comma-separated integers.   

    Returns:
        Set[int]: A set of integers parsed from the input string.
    """
    if not result_value:
        return set()
    return {int(part.strip()) for part in result_value.split(",") if part.strip()}


def _load_domande(question_path: Path) -> List[Tuple[int, str, str]]:
    """
    Load questions from the specified CSV file.
    Args:
        question_path (Path): Path to the CSV file containing questions.

    Raises:
        ValueError: If the CSV file lacks a header.

    Returns:
        List[Tuple[int, str, str]]: A list of tuples containing question index, question text, and difficulty.
    """     
    with question_path.open(encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if not reader.fieldnames:
            raise ValueError("Domande CSV privo di intestazione.")
        difficulty_key = reader.fieldnames[1]
        rows: List[Tuple[int, str, str]] = []
        for idx, row in enumerate(reader, start=1):
            question = row["domanda"].strip()
            difficulty = row[difficulty_key].strip()
            rows.append((idx, question, difficulty))
        return rows


def _load_ground_truth(ground_truth_path: Path) -> Dict[int, Set[int]]:
    """
    Load ground truth data from the specified CSV file.
    Args:
        ground_truth_path (Path): Path to the CSV file containing ground truth data.

    Returns:
        Dict[int, Set[int]]: A dictionary mapping row IDs to sets of expected dish IDs
    """
    with ground_truth_path.open(encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        ground_truth: Dict[int, Set[int]] = {}
        for row in reader:
            row_id = int(row["row_id"])
            ground_truth[row_id] = _parse_result(row["result"].strip())
        return ground_truth

def jaccard_score(set1: Set[int], set2: Set[int]) -> float:
    """
    Calculate the Jaccard similarity score between two sets.

    Args:
        set1 (Set[int]): The first set of integers.
        set2 (Set[int]): The second set of integers.

    Returns:
        float: The Jaccard similarity score between the two sets.
    """

    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0.0

def evaluate_easy_questions(agent: Agent, question_path: Path, ground_truth_path: Path) -> pd.DataFrame:
    """
    Evaluate the agent on easy questions and return a DataFrame with predictions.

    Args:
        agent (Agent): The agent to evaluate.
        question_path (Path): Path to the CSV file containing questions.
        ground_truth_path (Path): Path to the CSV file containing ground truth data.

    Returns:
        pd.DataFrame: A DataFrame containing the predictions for easy questions.
    """ 

    domande = _load_domande(question_path)
    ground_truth = _load_ground_truth(ground_truth_path)

    easy_questions = [
        (idx, question) for idx, question, difficulty in domande if difficulty.lower() == "easy"
    ]

    total = len(easy_questions)
    predictions = []
    scores = 0.0
    for idx, question in easy_questions:

        expected = ground_truth.get(idx)
        predicted = query_dish_ids(agent=agent, question=question)
        score = jaccard_score(expected, predicted)
        scores += score
        predictions.append([idx, expected, predicted, score])

        print(f"  atteso:    {sorted(expected)}")
        print(f"  predetto:  {sorted(predicted)}")
        print(f"[{idx:03d}] {score:.2f} - {question}")
        print("--------------------\n")

    accuracy = (scores / total) * 100
    print(f"\nAccuratezza Easy: ({accuracy:.2f}%)")

    predictions_df = pd.DataFrame(
        predictions, columns=["row_id", "expected", "predicted", "score"], index=False
    )
    return predictions_df