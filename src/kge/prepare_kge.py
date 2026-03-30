#!/usr/bin/env python3
"""
Adapted from TD5 notebook: load the TTL KG (td4_kb_final.ttl), split triples into
train/valid/test (80/10/10) and save as `train.txt`, `valid.txt`, `test.txt`.
"""
from rdflib import Graph
import random
from pykeen.triples import TriplesFactory
import os
import pandas as pd

# --------------------------
# Step 1: Load TD4 Knowledge Graph
# --------------------------
def save_txt(data, path):
    with open(path, "w", encoding="utf-8") as f:
        for s,p,o in data:
            f.write(f"{s}\t{p}\t{o}\n")

def main():
    ttl_path = os.path.join("kg_artifacts", "td4_kb_final.ttl")
    if not os.path.exists(ttl_path):
        raise FileNotFoundError(f"KG file not found: {ttl_path}. Run src/kg/build_kg.py first.")
    g = Graph()
    g.parse(ttl_path, format="turtle")

    triples = []
    for s, p, o in g:
        triples.append((str(s), str(p), str(o)))

    # --------------------------
    # Step 2: Split Train / Valid / Test (8:1:1)
    # --------------------------
    random.shuffle(triples)
    n = len(triples)
    train_triples = triples[:int(0.8 * n)]
    valid_triples = triples[int(0.8 * n):int(0.9 * n)]
    test_triples = triples[int(0.9 * n):]

    save_txt(train_triples, "train.txt")
    save_txt(valid_triples, "valid.txt")
    save_txt(test_triples, "test.txt")
    print("Saved train.txt, valid.txt, test.txt")

    # --------------------------
    # Optional: quick PyKEEN load check (if pykeen installed)
    # --------------------------
    try:
        train = TriplesFactory.from_path("train.txt")
        valid = TriplesFactory.from_path("valid.txt")
        test = TriplesFactory.from_path("test.txt")
        print(f"Triples loaded: train={len(train.triples)} valid={len(valid.triples)} test={len(test.triples)}")
    except Exception:
        print("PyKEEN not available or parsing failed; skipping PyKEEN quick check.")

if __name__ == "__main__":
    main()
