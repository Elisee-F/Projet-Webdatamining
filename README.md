# Projet-Webdatamining

This repository refactors and organizes the original coursework code into a modular project structure suitable for submission. The code has been grouped under `src/` and artifacts under `kg_artifacts/` and `data/`.

Below you will find installation instructions and how to run each module in the intended order.

## Installation

Requirements are listed in `requirements.txt`. Recommended: use a Python 3.10+ virtual environment.

Example (macOS / zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# For spaCy model
python -m spacy download en_core_web_sm
```

## Project layout (important files)

- `src/crawl/crawler.py` - web crawler, saves HTML to `data/raw`
- `src/clean/clean_data.py` - cleans HTML into `data/cleaned`
- `src/ie/extract_entities.py` - runs NER and stores CSV/XLSX under `data/entities`
- `src/kg/build_kg.py` - builds a minimal RDF KG and stores `kg_artifacts/td4_kb_final.ttl`
- `src/kge/prepare_kge.py` - prepares `train.txt`, `valid.txt`, `test.txt` for KGE
- `src/rag/rag_demo.py` - small RAG demo (NL -> template SPARQL -> KG answers)

## How to run each module

All commands assume you're at project root and virtualenv is activated. Run these in sequence for a full pipeline.

- Crawl:

```bash
python src/crawl/crawler.py
```

- Clean:

```bash
python src/clean/clean_data.py
```

- Entity extraction:

```bash
python src/ie/extract_entities.py
```

- Build KG:

```bash
python src/kg/build_kg.py
```

- Prepare KGE datasets:

```bash
python src/kge/prepare_kge.py
```

- RAG demo:

```bash
python src/rag/rag_demo.py
```

## RAG demo

Run the RAG demo after the knowledge graph has been built. The demo uses a simple template SPARQL and prints example QA outputs.

## Hardware requirements

- Small project: typical laptop (4+ CPU cores, 8GB RAM) suffices.
- For KGE training (if you extend): GPU recommended but not required for small toy datasets.

## Screenshot

![Directory screenshot](Graph/Graph%201.png)

## Reproducibility

- `requirements.txt` contains Python packages used. If original data is large, include `data/samples/` and provide a download link to full data in the README.

## Notes

- This refactor groups scripts under `src/` for clarity. Replace placeholder KG building with your ontology/alignment steps as needed.
