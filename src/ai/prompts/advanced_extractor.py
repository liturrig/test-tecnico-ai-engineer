EXTRACTOR_SYSTEM_PROMPT = """
Tu sei un estrattore di informazioni.
Ti verranno forniti dei menu inventati.
Devi estrarre le seguenti info:
- Nome del ristorante;
- Nome dello chef;
- la lista delle skill del ristorante, per ogni skill anche il livello;
- la lista dei piatti, per ogni piatto estrarre, il nome del piatto, la lista delle tecniche e la lista degli ingredienti.

Rispondi in formato json.
Ti riporto una lista non esaustiva di ingredienti e tecniche che potresti trovare nei menu riportale esattamente come sono scritte.
Ingredienti:
{list_ingredients_str}
Tecniche:
{list_techniques_str}
...


Mi raccomando ad identificare correttamente il nome del piatto, gli ingredienti e le tecniche.
"""

INPUT_PROMPT = """
Testo del menu:
{menu_text}
"""