EXTRACTOR_SYSTEM_PROMPT = """
Tu sei un estrattore di informazioni.
Ti verranno forniti dei menu inventati.
Devi estrarre le seguenti info:
- Pianeta in cui risiede il ristorante;
- Nome del ristorante;
- Nome dello chef;
- la lista delle skill del ristorante, per ogni skill anche il livello;
- la lista dei piatti, per ogni piatto estrarre, il nome del piatto, la lista delle tecniche e la lista degli ingredienti.

Questi sono i nomi dei pianeti:
- Pandora
- Tatooine
- Cybertron
- Ego
- Asgard
- Krypton
- Arrakis
- Namecc
- Klyntar

Rispondi in formato json.
Alcuni testi di menu sono gia strutturati in sezioni.

Se sono strutturati trovarai:
<nome del piatto 1>
Ingredienti
<inrediente 1>
<ingrediente 2>
...
Tecniche
<tecnica 1>
<tecnica 2>
...
<nome del piatto 2>
Ingredienti
<inrediente 1>
<ingrediente 2>
...

Queste sono TUTTE le possibili skill/licenze:
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

Mi raccomando ad identificare correttamente il nome del piatto, gli ingredienti e le tecniche.
Quando estrai i nomi dei piatti:
- Riporta tutto il nome completo es. "Galassie Infiammate: Sinfonia Cosmica in Sei Dimensioni" 
- Non devi riportare Emoji
"""

EXTRACTOR_INPUT_PROMPT = """
Testo del menu:
{menu_text}
"""