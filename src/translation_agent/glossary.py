import json


# Discrete mathematics glossary: English → Armenian
# Fill in the Armenian translations for each term.
# Terms with "TODO" values will be skipped in prompt injection.
DISCRETE_MATH_GLOSSARY = {
    # Sets
    "Set": "TODO",
    "Subset": "TODO",
    "Superset": "TODO",
    "Empty set": "TODO",
    "Power set": "TODO",
    "Union": "TODO",
    "Intersection": "TODO",
    "Complement": "TODO",
    "Cartesian product": "TODO",
    "Element": "TODO",
    # Logic
    "Proposition": "TODO",
    "Predicate": "TODO",
    "Logical connective": "TODO",
    "Conjunction": "TODO",
    "Disjunction": "TODO",
    "Negation": "TODO",
    "Implication": "TODO",
    "Biconditional": "TODO",
    "Quantifier": "TODO",
    "Universal quantifier": "TODO",
    "Existential quantifier": "TODO",
    "Tautology": "TODO",
    "Contradiction": "TODO",
    "Truth table": "TODO",
    # Proofs
    "Proof": "TODO",
    "Theorem": "TODO",
    "Lemma": "TODO",
    "Corollary": "TODO",
    "Axiom": "TODO",
    "Mathematical induction": "TODO",
    "Contradiction (proof by)": "TODO",
    "Contrapositive": "TODO",
    # Functions and Relations
    "Function": "TODO",
    "Domain": "TODO",
    "Codomain": "TODO",
    "Range": "TODO",
    "Injective": "TODO",
    "Surjective": "TODO",
    "Bijective": "TODO",
    "Inverse function": "TODO",
    "Composition": "TODO",
    "Relation": "TODO",
    "Equivalence relation": "TODO",
    "Partial order": "TODO",
    # Graph Theory
    "Graph": "TODO",
    "Vertex": "TODO",
    "Edge": "TODO",
    "Directed graph": "TODO",
    "Undirected graph": "TODO",
    "Adjacency": "TODO",
    "Degree": "TODO",
    "Path": "TODO",
    "Cycle": "TODO",
    "Tree": "TODO",
    "Spanning tree": "TODO",
    "Planar graph": "TODO",
    "Bipartite graph": "TODO",
    "Complete graph": "TODO",
    "Connected graph": "TODO",
    "Chromatic number": "TODO",
    # Combinatorics
    "Permutation": "TODO",
    "Combination": "TODO",
    "Binomial coefficient": "TODO",
    "Pigeonhole principle": "TODO",
    "Inclusion-exclusion principle": "TODO",
    # Number Theory
    "Prime number": "TODO",
    "Divisibility": "TODO",
    "Greatest common divisor": "TODO",
    "Least common multiple": "TODO",
    "Modular arithmetic": "TODO",
    "Congruence": "TODO",
    # Sequences and Recursion
    "Sequence": "TODO",
    "Recurrence relation": "TODO",
    "Recursion": "TODO",
    "Closed-form expression": "TODO",
    # Algorithms
    "Algorithm": "TODO",
    "Complexity": "TODO",
    "Boolean algebra": "TODO",
}


def format_glossary_for_prompt(glossary=None):
    """Format the glossary dict into a string for prompt injection.

    Returns empty string if all values are "TODO" or glossary is empty.
    """
    if glossary is None:
        glossary = DISCRETE_MATH_GLOSSARY

    entries = [
        f"- {eng} → {arm}"
        for eng, arm in glossary.items()
        if arm != "TODO" and arm.strip()
    ]

    if not entries:
        return ""

    header = (
        "Use the following glossary for domain-specific terminology. "
        "Always use these exact translations for the listed terms:\n"
    )
    return header + "\n".join(entries)


def load_glossary_from_file(filepath):
    """Load a glossary from a JSON file.

    The JSON file should be a dict mapping English terms to Armenian translations.
    """
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)
