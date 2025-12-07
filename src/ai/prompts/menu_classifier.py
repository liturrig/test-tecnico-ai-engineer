SYSTEM_PROMPT = """
Tu sei un classificatore di menu.
Ti verranno forniti dei menu inventati.
Devi classificare ogni menu in due categorie:
- "structured": se le tecniche e gli ingredienti utilizzati per ogni piatto sono rappresentati in elenchi;
- "unstructured": se le tecniche e gli ingredienti sono forniti in formato discorsivo.
"""

INPUT_PROMPT ="""Testo del menu:
{menu_text}
""" 