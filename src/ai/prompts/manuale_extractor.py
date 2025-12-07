SYSTEM_PROMPT = """
Ti verrà fornito il testo di un manuale di cucina. Focalizzati nella sezione "Licenze e Tecniche di preparazione".
Devi estrarre per ogni categoria, le tecniche sottostanti e per ogni tecnica, elencare le licenze associate.
In parrticolare:
- categoria della tecnica (es. Marinatura, Affumicatura, ecc )
- per ogni categoria, le tecniche associate.
"""

INPUT_PROMPT = """
Manuale di Cucina:
{menu_text}
"""