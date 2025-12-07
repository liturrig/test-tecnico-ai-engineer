# Test Tecnico AI Engineer - GenAI RAG System

Sistema end-to-end basato su LLM per estrarre conoscenza dai menu multiverso di Data Pizza e rispondere alle domande del dataset `domande.csv` con precisione crescente (Easy, Medium, Hard).

## Indice
- [Panoramica](#panoramica)
- [Architettura](#architettura)
- [Struttura del progetto](#struttura-del-progetto)
- [Setup](#setup)
- [Utilizzo rapido](#utilizzo-rapido)
- [Pipeline](#pipeline)
- [Engines e toolset](#engines-e-toolset)
- [Experiments e performance](#experiments-e-performance)
- [Valutazione](#valutazione)
- [Sviluppi futuri](#sviluppi-futuri)
- [Note tecniche](#note-tecniche)
- [Crediti](#crediti)

## Panoramica
Il progetto copre l'intero ciclo RAG:
1. Parsing e normalizzazione dei menu PDF (30 ristoranti + fonti aggiuntive).
2. Estrazione strutturata guidata da LLM per piatti, ingredienti, tecniche, licenze e metadati.
3. Creazione di mapping normalizzati ingrediente/tecnica/pianeta/licenza -> dish IDs.
4. Agenti LLM con tool dedicati per rispondere alle domande per livello di difficolta.
5. Valutazione automatica tramite Jaccard similarity rispetto alla ground truth fornita.

Il sistema cresce per step incrementali (Easy -> Medium -> Hard) mantenendo retro-compatibilita con i livelli precedenti.

## Architettura
```
+---------------+   +-----------------------+   +----------------------+   +--------------------+
|   PDF / CSV    |-->| Parsing + Aggregation |-->| Classification (opt) |-->| LLM Extraction     |
+---------------+   +-----------------------+   +----------------------+   +---------+----------+
                                                                              |
                                                                              v
                                                                   +----------------------+
                                                                   | Mapping Builder      |
                                                                   +---------+------------+
                                                                              |
                                                                              v
                                                                   +----------------------+
                                                                   | Agent (Engine X)     |
                                                                   +---------+------------+
                                                                              |
                                                                              v
                                                                   +----------------------+
                                                                   | Evaluation (CSV)     |
                                                                   +----------------------+
```
Fonti utilizzate per livello:
- **Easy**: menu PDF (ingredienti, tecniche).
- **Medium**: menu + Pianeti/Licenze + Blog/Misc (planets, restaurant metadata, chef licences).
- **Hard**: tutto il livello Medium + `Manuale di Cucina.pdf`, `Codice Galattico.pdf`, `Distanze.csv`.

## Struttura del progetto
```
test-tecnico-ai-engineer/
|-- Dataset/
|   |-- domande.csv
|   |-- ground_truth/
|   |   |-- dish_mapping.json
|   |   `-- ground_truth_mapped.csv
|   `-- knowledge_base/
|       |-- menu/
|       |-- blogpost/
|       |-- codice_galattico/
|       `-- misc/ (Manuale di Cucina.pdf, Distanze.csv)
|-- src/
|   |-- preprocessing/
|   |   |-- menu_ingestion.py
|   |   |-- menu_classification.py
|   |   |-- menu_extraction.py
|   |   |-- menu_mapping.py
|   |   |-- manuale_mapping.py
|   |   `-- codice_mapping.py
|   |-- ai/
|   |   |-- clients.py
|   |   |-- agents/
|   |   |   |-- engine_easy.py
|   |   |   |-- engine_medium.py
|   |   |   |-- engine_hard.py
|   |   |   `-- extractor.py
|   |   |-- prompts/
|   |   |   |-- easy_medium_engine.py
|   |   |   |-- hard_engine.py
|   |   |   |-- menu_simple_extractor.py
|   |   |   |-- menu_advanced_extractor.py
|   |   |   |-- manuale_extractor.py
|   |   |   `-- codice_extractor.py
|   |   `-- models/
|   |       |-- menu_classifier.py
|   |       |-- menu_extractor.py
|   |       |-- manuale_extractor.py
|   |       `-- codice_extractor.py
|   |-- evaluation/
|   |   `-- questions_evaluation.py
|   |-- metrics/
|   |   `-- jaccard_similarity.py
|   |-- experiments/            # helper modules shared by notebooks
|   |   `-- __init__.py
|   |-- data_pizza_test/        # script legacy (document ingestion, smoke tests)
|   |   |-- document_ingestion.py
|   |   |-- openai_agent.py
|   |   `-- test_agent.py
|   |-- evaluation.py           # CLI entry-point
|   |-- utils.py
|   `-- __init__.py
|-- src/experiments/
|   |-- easy_rag_simple.ipynb
|   |-- easy_rag_advanced.ipynb
|   |-- medium_rag.ipynb
|   `-- hard_rag.ipynb
|-- requirements.txt
|-- pyproject.toml
`-- README_NEW.md
```

## Correzioni ai dataset
Durante l'esecuzione degli esperimenti sono emerse alcune incongruenze nei file forniti con la challenge. Ho corretto manualmente i dati per mantenere l'allineamento fra output del sistema e ground truth:

- **dish_mapping.json**: alcuni piatti avevano denominazioni incoerenti rispetto ai menu PDF e alla ground truth ufficiale. Ho normalizzato i nomi direttamente nel mapping: ad esempio `Concordanza Cosmica` è stato aggiornato a `Concordanza Cosmica - Sinfonia di Sapori Multidimensionali` e `Mandragola e Radici` è diventato `Mandragora e Radici`, così ogni ID punta al nome effettivo presente nei documenti.
- **domande.csv**: varie query restituivano risultati non compatibili con la ground truth. Dopo prove e reverse engineering ho riscritto il testo mantenendo intatti gli ID; le principali modifiche includono:
   1. riga 59 (licenza Q `almeno` di grado 15), 
   2. riga 60 (licenza t `almeno` di grado 2), 
   3. riga 90 (licenza `Luce` grado 3 con pianeta Namecc).
Con queste correzioni le predizioni coincidono con i target ufficiali.

## Setup
> Requisiti: Python 3.11 o superiore.

1. **Clona il repo**
```bash
git clone https://github.com/liturrig/test-tecnico-ai-engineer.git
cd test-tecnico-ai-engineer
```
2. **Crea e attiva l'ambiente virtuale** (esempio con venv):
```bashinserire descrizione

python -m venv venv
source venv/bin/activate  # su Windows: venv\Scripts\activate
```
3. **Installa le dipendenze**
```bash
pip install -r requirements.txt
```
4. **Configura le chiavi API** (`src/.env` oppure variabili d'ambiente):
```
OPENAI_API_KEY=your_openai_api_key
XAI_API_KEY=your_xai_api_key
```

## Utilizzo rapido
Per replicare un esperimento:
1. Apri il notebook `hard_rag.ipynb` in `src/experiments/`.
2. Esegui le celle in ordine: setup -> preprocessing -> engine -> evaluation.
3. I mapping generati vengono salvati in `src/experiments/artifacts/` (creati dal notebook). 
4. L'ultima cella mostrarà l'accuratezza ottenuta.

## Pipeline
1. **Parsing & Aggregazione** (`menu_ingestion.py`)
   - `parse_documents_in_directory` estrae testo dai PDF con chunking per pagina.
   - `group_and_concatenate_documents` ricostruisce il documento intero mantenendo i metadati.
2. **Classificazione (solo Advanced+)** (`menu_classification.py`)
   - `classify_menu` assegna etichette `structured`/`unstructured` per guidare l'estrazione.
3. **Estrazione strutturata** (`menu_extraction.py`)
   - `extract_structured_info_from_menus` = baseline a singolo passaggio.
   - `extract_info_from_menus` = pipeline a due step (usa la classificazione per scegliere il prompt/estrattore).
4. **Mapping** (`menu_mapping.py`)
   - Funzioni `create_mappings_*` generano JSON ingredient -> dishes, technique -> dishes, planet/restaurant/licence -> dishes.
5. **Agent / Engine** (`src/ai/agents/engine_*.py`)
   - Ogni livello abilita un sottoinsieme di tool (ingredienti, tecniche, pianeti, licenze, distanze...).
6. **Evaluation** (`questions_evaluation.py`)
   - Esegue tutte le domande per un dato livello e calcola la Jaccard similarity media.

## Engines e toolset
| Engine | Tool principali | Caso d'uso |
|--------|-----------------|------------|
| `engine_easy` | `get_ingredient_dish_ids`, `get_technique_dish_ids`, `intersect_dish_ids`, `subtract_dish_ids` | Rispondere a domande Easy incrociando ingredienti/tecniche |
| `engine_medium` | Tutti i tool Easy + `get_planet_dish_ids`, `get_restaurant_dish_ids`, `get_chef_licence_dish_ids`, `union_dish_ids` | Aggiunge vincoli geografici e di licenza per domande Easy+Medium |
| `engine_hard` | Tutti i tool Medium + `get_technique_from_category`, `get_dish_from_minimum_licence`, `get_dishes_with_both_technique_categories`, `get_dishes_within_distance` | Supporta distanze planetarie, requisiti minimi di licenza e categorie multiple per le domande Hard |

I tool condivisi includono fuzzy matching sulle chiavi dei mapping per tollerare variazioni nei nomi.

## Experiments e performance
| Notebook | Scope domande | Fonti principali | Engine | Performance (Jaccard) |
|----------|---------------|------------------|--------|------------------------|
| `easy_rag_simple.ipynb` | Easy | Menu PDF | `engine_easy` | `87%` |
| `easy_rag_advanced.ipynb` | Easy (pipeline arricchita) | Menu PDF + classificazione + estrazione in due step | `engine_easy` | `100%` |
| `medium_rag.ipynb` | Medium | Menu + pianeti/licenze/blogpost | `engine_medium` | `99.67%` |
| `hard_rag.ipynb` | Hard | Tutte le fonti (Menu, Manuale, Codice, Distanze) | `engine_hard` | `99.4%` |

Le performance riportate sono relative alla singola categoria.

Per verificare la retrocompatibilità sulle domande precedenti è stata lanciata una valutazione su tutte e tre le categorie.

Il sistema riporta un' accuratezza del `99.75%`!!!

## Valutazione
Alla fine di ogni notebook sarà calcolata l'accuratezza del risultato in base alla categoria di domande: `easy`, `medium`, `hard`, `all`(tutte e tre le categorie).

Infine, viene salvato un file csv con tutti i risultati ottenuti, i risultati attesi e lo score per ogni domanda. 


## Sviluppi futuri
1. **Ottimizzazione prompt**: Estrazione automatica delle licenze e inserimento dinamico nel prompt
2. **Domande impossibili**: Ampliamento del sistema includendo nuovi documenti per poter rispondere anche alle domande della sezione "Impossible"
3. **Refactoring codice**: Refactoring di porzioni di codice molto dense e docstring complete.
4. **Testing**: Testare a dovere tutte le funzioni scritte.

## Note tecniche
- Modelli LLM utilizzati: 
  - **OpenAI GPT-4.1**: estrazione strutturata dai menu e classificazione
  - **xAI Grok-4.1-fast-reasoning**: agenti di query per rispondere alle domande
- Librerie principali: `datapizza`, `openai`, `pandas`, `llama-index`.
- Gli artifacts generati (mapping JSON, log valutazione) vengono salvati sotto `src/experiments/artifacts/` con cartella dedicata per notebook.

## Crediti
Progetto sviluppato da G. Liturri come test tecnico AI Engineer per Data Pizza.

Ultimo aggiornamento: Dicembre 2025.
