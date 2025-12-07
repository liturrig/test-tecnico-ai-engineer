from collections import defaultdict
from pathlib import Path
from typing import Optional
from llama_index.core import SimpleDirectoryReader



def parse_documents_in_directory(document_path: Optional[Path] = None, file_path: Optional[Path] = None) -> list:
    """
    Parse documents in the given directory and save the concatenated output as a JSON file.

    Args:
        document_path (Path): Path to the directory containing the documents.
    Returns:
        list: List of parsed document objects. Each element is a page of a specific document.
    """
    if file_path:
        reader = SimpleDirectoryReader(input_files=file_path)
    else:
        reader = SimpleDirectoryReader(input_dir=document_path)
    documents = reader.load_data()
    
    return documents


def group_and_concatenate_documents(documents: list) -> dict:
    """
    Group documents by file name, concatenate their text content, and save the result as a JSON file.

    Args:
        documents (list): List of document objects to be processed.
    
    Returns:
        dict: A dictionary where keys are file names and values are concatenated text content.
    """
    docs_by_file = defaultdict(list)
    final_output = {}   

    for doc in documents:
        file_name = doc.metadata.get('file_name', 'unknown_file')
        docs_by_file[file_name].append(doc)

    for file_name, pages_list in docs_by_file.items():
        pages_list.sort(key=lambda x: int(x.metadata.get('page_label', 0)))
        full_text = "\n".join([page.text for page in pages_list])
        final_output[file_name] = full_text
    
    return final_output