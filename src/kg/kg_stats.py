"""Compute simple statistics for an RDF knowledge graph (triples, classes, properties, distinct subjects/objects)."""
from rdflib import Graph
import os


def compute_stats(ttl_path: str):
    g = Graph()
    g.parse(ttl_path, format="ttl")
    triples = len(g)
    classes = set()
    properties = set()
    subjects = set()
    objects = set()

    for s, p, o in g:
        subjects.add(s)
        objects.add(o)
        properties.add(p)
        if str(p).endswith("type") or p.endswith("#type"):
            classes.add(o)

    stats = {
        "triples": triples,
        "distinct_subjects": len(subjects),
        "distinct_objects": len(objects),
        "distinct_properties": len(properties),
        "distinct_classes_estimate": len(classes),
    }
    return stats


if __name__ == "__main__":
    ttl = os.path.join("kg_artifacts", "td4_kb_final.ttl")
    if not os.path.exists(ttl):
        print(f"KG file not found: {ttl}")
    else:
        s = compute_stats(ttl)
        for k, v in s.items():
            print(f"{k}: {v}")
