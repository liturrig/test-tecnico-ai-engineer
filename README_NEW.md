# Test Tecnico AI Engineer - Sistema di Estrazione e Interrogazione Menu Ristorante 🍕🤖

Un sistema end-to-end basato su LLM per estrarre informazioni strutturate da menu di ristoranti e rispondere a domande in linguaggio naturale sui piatti, ingredienti e tecniche culinarie.

## 📋 Indice

- [Panoramica](#-panoramica)
- [Architettura](#-architettura)
- [Struttura del Progetto](#-struttura-del-progetto)
- [Installazione](#-installazione)
- [Utilizzo](#-utilizzo)
- [Pipeline](#-pipeline)
- [Valutazione](#-valutazione)
- [Risultati](#-risultati)
- [Sviluppi Futuri](#-sviluppi-futuri)

## 🎯 Panoramica

Questo progetto implementa una soluzione completa per:

1. **Parsing e Aggregazione**: Estrazione del testo da documenti PDF di menu ristorante
2. **Estrazione Strutturata**: Utilizzo di LLM per identificare entità (ristoranti, piatti, ingredienti, tecniche)
3. **Creazione Mapping**: Costruzione di mappature normalizzate tra ingredienti/tecniche e piatti
4. **Interrogazione Intelligente**: Sistema basato su agenti LLM per rispondere a domande in linguaggio naturale
5. **Valutazione Automatica**: Confronto delle risposte con ground truth utilizzando metriche di similarità

### Caratteristiche Principali

- ✅ Estrazione automatica di informazioni strutturate da menu non strutturati
- ✅ Normalizzazione e mappatura di entità culinarie
- ✅ Agente conversazionale per query in linguaggio naturale
- ✅ Sistema di valutazione con metriche Jaccard similarity
- ✅ **Accuratezza del 100% sulle domande Easy**

## 🏗 Architettura

### Simple RAG - Pipeline Base

La pipeline semplice è organizzata in 4 fasi:

```
┌─────────────────────┐
│  1. PARSING         │
│  PDF → Testo        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  2. EXTRACTION      │
│  LLM → Struttura    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  3. MAPPING         │
│  Normalizzazione    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  4. QUERY AGENT     │
│  NL → Dish IDs      │
└─────────────────────┘
```

### Advanced RAG - Pipeline Avanzata

La pipeline avanzata aggiunge una fase di classificazione e estrazione adattiva:

```
┌─────────────────────┐
│  1. PARSING         │
│  PDF → Testo        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  2. CLASSIFICATION                      │
│  Structured vs Unstructured             │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  3. ADAPTIVE EXTRACTION                 │
│  ┌─────────────┐    ┌─────────────┐     │
│  │ Structured  │    │Unstructured │     │
│  │ Extractor   │    │ Extractor   │     │
│  └─────────────┘    └─────────────┘     │
│         │                   │           │
│         └───────┬───────────┘           │
│                 │                       │
│          Knowledge Transfer             │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  4. ENHANCED MAPPING                    │
│  Normalizzazione con dati arricchiti    │
└──────────┬──────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  5. QUERY AGENT WITH SET OPS            │
│  NL → Dish IDs                          │
└─────────────────────────────────────────┘
```

## 📁 Struttura del Progetto

```
test-tecnico-ai-engineer/
├── Dataset/
│   ├── domande.csv                    # Domande di valutazione
│   ├── ground_truth/
│   │   ├── dish_mapping.json          # Mapping piatti → IDs
│   │   └── ground_truth_mapped.csv    # Risposte corrette
│   └── knowledge_base/
│       ├── menu/                       # 30 menu PDF
│       ├── blogpost/                   # Blog HTML
│       ├── codice_galattico/          # PDF legislativo
│       └── misc/                       # Distanze.csv, Manuale di Cucina.pdf
├── src/
│   ├── preprocessing/
│   │   ├── menu_ingestion.py          # Parsing PDF
│   │   ├── menu_classification.py     # Classificazione menu (Advanced)
│   │   ├── menu_extraction.py         # Estrazione LLM (Simple + Advanced)
│   │   └── menu_mapping.py            # Creazione mapping
│   ├── ai/
│   │   ├── clients.py                 # Client OpenAI
│   │   ├── agents/
│   │   │   ├── engine.py              # Agente query con tool
│   │   │   └── extractor.py           # Agente extraction
│   │   ├── models/
│   │   │   ├── classifier.py          # Modello classificazione
│   │   │   └── extractor.py           # Modello estrazione
│   │   └── prompts/
│   │       ├── engine.py              # Prompt agente query
│   │       ├── classifier.py          # Prompt classificatore
│   │       ├── simple_extractor.py    # Prompt estrazione semplice
│   │       └── advanced_extractor.py  # Prompt estrazione avanzata
│   ├── evaluation/
│   │   └── easy_questions_evaluation.py # Valutazione automatica
│   ├── metrics/
│   │   └── jaccard_similarity.py      # Metriche Jaccard
│   ├── evaluation.py                  # Script valutazione CLI
│   └── utils.py                       # Utility functions (read/write JSON)
├── src/experiments/
│   ├── simple_rag.ipynb               # Pipeline base (87% accuracy)
│   ├── advanced_rag.ipynb             # Pipeline avanzata (100% accuracy)
│   └── artifacts/
│       ├── simple_rag/                # Output pipeline semplice
│       └── advanced_rag/              # Output pipeline avanzata
├── requirements.txt                   # Dipendenze Python
└── pyproject.toml                     # Configurazione progetto
```

## 🚀 Installazione

### Prerequisiti

- Python >= 3.9
- pip o poetry

### Setup

```bash
# Clone del repository
git clone https://github.com/liturrig/test-tecnico-ai-engineer.git
cd test-tecnico-ai-engineer

# Installazione dipendenze dal file requirements.txt
pip install -r requirements.txt
```

### Configurazione

**Importante**: Prima di eseguire il codice, creare un file `.env` nella cartella `src/` con la chiave API di OpenAI:

```env
OPENAI_API_KEY=your_api_key_here
```

## 💻 Utilizzo

### Due Approcci Disponibili

Il progetto offre due soluzioni con diversi livelli di complessità:

#### 1. Simple RAG (`simple_rag.ipynb`) - Accuratezza 87%

Approccio base che estrae informazioni da tutti i menu con un singolo estrattore:

#### 2. Advanced RAG (`advanced_rag.ipynb`) - Accuratezza 100%

Approccio avanzato che:
- Classifica i menu in strutturati/non strutturati prima dell'estrazione
- Usa estrattori specializzati per ciascun tipo di menu
- Riutilizza ingredienti/tecniche dai menu puliti per guidare l'analisi dei menu rumorosi

### Esecuzione Simple RAG

Il notebook `src/experiments/simple_rag.ipynb` contiene la pipeline base:

```python
# 1. Setup
from pathlib import Path
project_dir = Path.cwd().parent.parent
dataset_file_path = project_dir / "Dataset"
artifacts_file_path = Path.cwd() / "artifacts" / "simple_rag"

# 2. Parsing
from src.preprocessing.menu_ingestion import parse_documents_in_directory, group_and_concatenate_documents

documents_pages = parse_documents_in_directory(dataset_file_path / "Knowledge_base" / "menu")
documents = group_and_concatenate_documents(documents_pages)

# 3. Estrazione
from src.preprocessing.menu_extraction import extract_structured_info_from_menus

extracted_info = extract_structured_info_from_menus(documents, model_name="gpt-4.1-nano")

# 4. Mapping
from src.preprocessing.menu_mapping import create_mappings
from src.utils import read_json

dish_mapping = read_json(dataset_file_path / "ground_truth" / "dish_mapping.json")
ingredient_to_dishes, technique_to_dishes = create_mappings(extracted_info, dish_mapping)

# 5. Query
from src.ai.agents.engine import get_agent, query_dish_ids

agent = get_agent(model_name="gpt-4.1")
response = query_dish_ids("Quali piatti includono Chocobo Wings?", agent)
print(response)

# 6. Valutazione
from src.evaluation.easy_questions_evaluation import evaluate_easy_questions

eval_df = evaluate_easy_questions(
    agent=agent,
    question_path=dataset_file_path / "domande.csv",
    ground_truth_path=dataset_file_path / "ground_truth" / "ground_truth_mapped.csv"
)
print(f"Accuracy: {eval_df['correct'].mean()}")
```

### Esecuzione Advanced RAG

Il notebook `src/experiments/advanced_rag.ipynb` include passaggi aggiuntivi:

```python
# 1-2. Setup e Parsing (identici a simple_rag)

# 3. Classificazione dei menu
from src.preprocessing.menu_classification import classify_menu

classifications = classify_menu(text_extracted=documents)
write_json(classifications, artifacts_file_path / "menu_classifications.json")

# 4. Estrazione adattiva (usa classificazioni)
from src.preprocessing.menu_extraction import extract_info_from_menus

extracted_info = extract_info_from_menus(documents=documents, classifications=classifications)
write_json(extracted_info, artifacts_file_path / "extracted_menu_info.json")

# 5-6. Mapping e Query (identici a simple_rag ma con dati più completi)
```

### Utilizzo Programmatico

```python
from src.ai.agents.engine import get_agent, query_dish_ids

# Inizializza l'agente
agent = get_agent(model_name="gpt-4.1")

# Fai una domanda
question = "Quali sono i piatti che includono le Chocobo Wings come ingrediente?"
dish_ids = query_dish_ids(question, agent)
print(f"Dish IDs: {dish_ids}")
```

## 🔄 Pipeline

### 1. Parsing e Aggregazione

**Modulo**: `src/preprocessing/menu_ingestion.py`

```python
def parse_documents_in_directory(document_path: Path) -> list
def group_and_concatenate_documents(documents: list) -> dict
```

- Utilizza `llama-index` per parsare PDF
- Raggruppa pagine dello stesso documento
- Concatena testo mantenendo l'ordine delle pagine
- **Output**: `parsed_menus.json`

### 2. Classificazione Menu (solo Advanced RAG)

**Modulo**: `src/preprocessing/menu_classification.py`

```python
def classify_menu(text_extracted: dict, model_name: str = "gpt-4.1-mini") -> dict
```

- Classifica ogni menu come `structured` o `unstructured`
- Determina quale estrattore utilizzare
- **Output**: `menu_classifications.json`

### 3. Estrazione Strutturata

**Modulo**: `src/preprocessing/menu_extraction.py`

**Simple RAG**:
```python
def extract_structured_info_from_menus(documents: dict, model_name: str) -> dict
```

**Advanced RAG**:
```python
def extract_info_from_menus(documents: dict, classifications: dict) -> dict
```

- Utilizza LLM (gpt-4.1) per estrazione strutturata
- In Advanced RAG: estrattori specializzati basati su classificazione
- Identifica: `restaurant_name`, `dishes`, `ingredients`, `techniques`
- **Output**: `extracted_menu_info.json`

**Formato Output**:
```json
[
  {
    "restaurant_name": "Ristorante Esempio",
    "dishes": [
      {
        "dish_name": "Piatto 1",
        "ingredients": ["ingrediente1", "ingrediente2"],
        "techniques": ["tecnica1"]
      }
    ]
  }
]
```

### 3. Creazione Mapping

**Modulo**: `src/preprocessing/menu_mapping.py`

```python
def create_mappings(extracted_info: dict, dish_mapping: dict) -> Tuple[dict, dict]
```

- Normalizza nomi di ingredienti e tecniche
- Crea mappature bidirezionali: `ingredient → [dish_ids]` e `technique → [dish_ids]`
- **Output**: `ingredient_to_dishes.json`, `technique_to_dishes.json`

### 4. Agente Conversazionale

**Modulo**: `src/ai/agents/engine.py`

L'agente utilizza **function calling** con 4 tool:

```python
@tool
def get_ingredient_dish_ids(ingredient: str) -> str:
    """Ritorna dish IDs per l'ingrediente specificato"""

@tool
def get_technique_dish_ids(technique: str) -> str:
    """Ritorna dish IDs per la tecnica specificata"""

@tool
def intersect_dish_ids(first_list: list[int], second_list: list[int]) -> str:
    """Ritorna l'intersezione di due liste di dish IDs"""

@tool
def subtract_dish_ids(first_list: list[int], second_list: list[int]) -> str:
    """Rimuove gli IDs della seconda lista dalla prima"""
```

**Funzionalità**:
- Fuzzy matching per gestire variazioni nei nomi
- **Operazioni insiemistiche** (intersezione, sottrazione) per query complesse
- Combinazione logica di più criteri (AND/OR/NOT)
- Gestione di query complesse in linguaggio naturale

**Esempio query complesse**:
- "Piatti con ingrediente A E ingrediente B" → usa `intersect_dish_ids`
- "Piatti con tecnica X MA SENZA ingrediente Y" → usa `subtract_dish_ids`

## 📊 Valutazione

### Sistema di Valutazione

**Modulo**: `src/evaluation/easy_questions_evaluation.py`

```python
def evaluate_easy_questions(agent: Agent, question_path: Path, ground_truth_path: Path) -> pd.DataFrame
```

**Processo**:
1. Carica domande da `domande.csv`
2. Carica ground truth da `ground_truth_mapped.csv`
3. Per ogni domanda Easy:
   - Ottiene prediction dall'agente
   - Calcola Jaccard similarity con ground truth
   - Determina correttezza (threshold > 0.95)
4. Genera report con metriche aggregate

**Metrica Principale**: Jaccard Similarity

```python
def jaccard_score(set1: Set[int], set2: Set[int]) -> float:
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union != 0 else 0.0
```

## 📈 Risultati

### Performance sulle Domande Easy

| Approccio | Accuratezza | Note |
|-----------|-------------|------|
| **Simple RAG** | **87%** | Pipeline base con estrattore unico |
| **Advanced RAG** | **100%** | Pipeline con classificazione e estrazione adattiva |

- **Domande valutate**: 50 domande Easy
- **Threshold di correttezza**: Jaccard similarity  1.0

### Esempi di Output

**Domanda**: "Quali sono i piatti che includono le Chocobo Wings come ingrediente?"

**Risposta**: `[24]` (Galassia di Sapori: Il Viaggio Senza Tempo)

**Ground Truth**: `[24]`

**Jaccard Score**: `1.0` ✅

### Artifacts Generati

**Simple RAG** (`src/experiments/artifacts/simple_rag/`):
- `parsed_menus.json` - Menu parsati (30 ristoranti)
- `extracted_menu_info.json` - Informazioni strutturate estratte
- `ingredient_to_dishes.json` - Mapping ingredienti → piatti
- `technique_to_dishes.json` - Mapping tecniche → piatti
- `easy_questions_evaluation_results.csv` - Risultati valutazione

**Advanced RAG** (`src/experiments/artifacts/advanced_rag/`):
- Tutti i file di Simple RAG +
- `menu_classifications.json` - Classificazione menu (structured/unstructured)
- Mapping più completi grazie all'estrazione adattiva

## 🔮 Sviluppi Futuri

### Miglioramenti Pianificati

1. **Prompt Engineering**
   - Ottimizzazione dei prompt per ridurre allucinazioni
   - Few-shot learning per migliorare estrazione

2. **Normalizzazione Avanzata**
   - Fuzzy matching più robusto
   - Indicizzazione semantica degli ingredienti

3. **Scalabilità**
   - Parallelizzazione parsing ed estrazione
   - Batch processing per grandi dataset
   - Caching dei risultati intermedi

4. **Domande Medium/Hard/Impossible**
   - Integrazione con `Distanze.csv` per query geografiche
   - Parsing di `Manuale di Cucina.pdf` e `Codice Galattico.pdf`
   - Implementazione NoSQLBN o GraphDB per la gestion della knowledge base


## 📝 Note Tecniche

### Modelli Utilizzati

- **Estrazione**: `gpt-4.1` (più capace per ragionamento complesso)
- **Query Agent**: `gpt-4.1-mini` (veloce)

### Dipendenze Principali

- `llama-index`: Document parsing e chunking
- `datapizza`: Framework per agenti e tool calling
- `openai`: API LLM
- `pandas`: Data manipulation e analysis

## 🤝 Contributi

Progetto sviluppato per il test tecnico AI Engineer di Data Pizza.

**Autore**: G. Liturri  
**Repository**: https://github.com/liturrig/test-tecnico-ai-engineer

## 📄 Licenza

Proprietario - Data Pizza

---

*Ultima modifica: Dicembre 2025*
