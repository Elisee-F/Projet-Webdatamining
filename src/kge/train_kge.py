"""Lightweight KGE training entrypoint.
This script prepares train/valid/test (if not present) and runs a tiny PyKEEN training loop if pykeen is installed.
"""
import os
import csv


def ensure_splits(triples_tsv: str):
    # If train/valid/test already exist at repo root, do nothing
    root = os.getcwd()
    for name in ["train.txt", "valid.txt", "test.txt"]:
        if os.path.exists(os.path.join(root, name)):
            print(f"Found {name}, skipping split generation.")
            return

    # Otherwise, try to read triples from source and split (simple round-robin)
    if not os.path.exists(triples_tsv):
        print(f"Triples file not found: {triples_tsv}")
        return

    with open(triples_tsv, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    splits = {"train": [], "valid": [], "test": []}
    for i, line in enumerate(lines):
        if i % 10 == 8:
            splits["test"].append(line)
        elif i % 10 == 9:
            splits["valid"].append(line)
        else:
            splits["train"].append(line)

    for name in splits:
        out = os.path.join(root, f"{name}.txt")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write("\n".join(splits[name]))
        print(f"Wrote {out} ({len(splits[name])} triples)")


def run_pykeen_demo():
    try:
        from pykeen.pipeline import pipeline
    except Exception:
        print("pykeen not installed; to run training install pykeen or skip this step.")
        return

    if not os.path.exists("train.txt"):
        print("train.txt not found; run ensure_splits first.")
        return

    # Very small demo config
    result = pipeline(
        training="train.txt",
        validation="valid.txt" if os.path.exists("valid.txt") else None,
        testing="test.txt" if os.path.exists("test.txt") else None,
        model="TransE",
        training_kwargs={"num_epochs": 5, "batch_size": 128},
    )
    print("Training finished. Results keys:", list(result.metrics.keys()))


if __name__ == "__main__":
    triples_src = os.path.join("kg_artifacts", "td4_kb_final.ttl")
    # If a tsv/nt format exists, you might convert it. For now we attempt to use an existing train.txt
    ensure_splits(triples_src)  # will early-exit if train.txt exists
    run_pykeen_demo()
