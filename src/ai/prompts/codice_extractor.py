SYSTEM_PROMPT = """
Ti verrà fornito il testo di un manuale di cucina. Focalizzati nella sezione "Licenze e Tecniche di preparazione".
Devi estrarre per ogni categoria, le tecniche sottostanti e per ogni tecnica, elencare le licenze associate.
In parrticolare:
- categoria della tecnica (es. Marinatura, Affumicatura, ecc )
- per ogni categoria, le tecniche associate.
- per ogni tecnica, le licenze associate.
- per ogni licenza riportare il nome della licenza e il grado.

Per aiutarti ti riporto la struttura delle licenze:
Nome completo: "Psionica (P)" Livelli: 0, I, II, III, IV, V 
Nome completo: "Temporale (t)" Livelli: I, II, III
Nome completo: "Gravitazionale (G)" Livelli: 0, I, II, III
Nome completo: "Antimateria (e+)" Livelli: 0, I
Nome completo: "Magnetica (Mx)" Livelli: 0, I
Nome completo: "Quantistica (Q)" Livelli: "n" dove n sono il numero di stati in superposizione
Nome completo: "Luce (c)" Livelli: I, II, III
Nome completo: "Livello di Sviluppo Tecnologico (LTK)" Livelli: I, II, III, IV, V, VI, VI+

Quando estrai le skill riporta il nome completo della skill con il simbolo tra parentesi.
Riporta il grado sotto forma di numero (0, 1, 2,) Per il "VI+" puoi riportarlo come 7.
"""

INPUT_PROMPT = """
Manuale di Cucina:
{menu_text}
"""