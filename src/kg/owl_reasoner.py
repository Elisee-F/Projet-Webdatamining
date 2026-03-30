"""Simple OWLReady2-based reasoner that loads an ontology + data and runs a reasoner.
This is optional and requires `owlready2` installed. It demonstrates how to expand the KG via class/property inferences.
"""
import os

try:
    from owlready2 import get_ontology, sync_reasoner_pellet
except Exception:
    get_ontology = None
    sync_reasoner_pellet = None


def do_reasoning(ontology_path: str, output_path: str):
    if get_ontology is None:
        raise RuntimeError("owlready2 is not installed. Install it with `pip install owlready2` to use this script.")
    onto = get_ontology(ontology_path).load()
    # Use pellet reasoner if available; Owlready2 ships a HermiT wrapper sometimes.
    try:
        sync_reasoner_pellet([onto], infer_property_values=True, infer_data_property_values=True)
    except Exception:
        # Fallback to default reasoner
        from owlready2 import sync_reasoner
        sync_reasoner()

    # Save inferred ontology (includes asserted + inferred axioms)
    onto.save(file=output_path, format="rdfxml")


if __name__ == "__main__":
    ontology = os.path.join("kg_artifacts", "ontology.ttl")
    out = os.path.join("kg_artifacts", "ontology_inferred.rdf")
    if not os.path.exists(ontology):
        print(f"Ontology not found: {ontology}")
    else:
        print("Running OWL reasoning (may require additional packages). This could take several seconds...")
        do_reasoning(ontology, out)
        print(f"Inferred ontology written to: {out}")
