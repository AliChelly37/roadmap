"""Éval de retrieval du capstone — garde-fou anti-régression.

Reprend le principe de la Semaine 5 (jeu d'éval + mesure) et de la Semaine 7
(éval en CI qui échoue sur régression). Chaque cas associe une question à la
semaine de la roadmap qui doit apparaître dans le top-k.

Usage :
    python test_retrieval.py            # échoue si recall < SEUIL
    pytest test_retrieval.py            # même chose, via pytest
"""
import sys

from core.rag import (
    index_roadmap_files,
    search_roadmap,
    EMBED_MODEL,
    DEFAULT_N_RESULTS,
)

# (question, fragment attendu dans le nom du fichier source)
CASES = [
    # Questions telles que l'utilisateur les pose.
    ("Qu'est-ce que LiteLLM ?", "07-semaine-7"),
    ("Comment fonctionne le reranking ?", "05-semaine-5"),
    ("Qu'est-ce qu'un embedding ?", "03-semaine-3"),
    ("Comment parser un PDF pour du RAG ?", "04-semaine-4"),
    ("C'est quoi LangGraph ?", "06-semaine-6"),
    ("Comment fonctionne la tokenisation d'un LLM ?", "01-semaine-1-fondations-llm"),
    ("Comment faire du prompt engineering avec du few-shot ?", "02-semaine-2-prompt"),
    ("Comment déployer sur Hugging Face Spaces ?", "08-semaine-8"),

    # Requêtes telles que l'AGENT les reformule : il ajoute des méta-mots
    # ("semaine", "roadmap", "formation") qui, eux, matchent surtout la table
    # des matières. C'est le cas réel en production, il doit être couvert.
    ("reranking semaine 5 AI Engineering Roadmap", "05-semaine-5"),
    ("LangGraph agents semaine 6 formation", "06-semaine-6"),
    ("observabilité Langfuse semaine 7 roadmap", "07-semaine-7"),
    ("chunking RAG semaine 4 formation AI Engineering", "04-semaine-4"),
]

# Le pipeline atteint 100 % ; on garde une marge pour ne pas casser la CI sur
# une variation mineure du modèle d'embeddings.
SEUIL_RECALL = 0.85


def evaluate(n_results: int = DEFAULT_N_RESULTS):
    """Retourne (recall, échecs) sur le jeu d'éval.

    Par défaut on mesure au `n_results` réellement utilisé par l'outil de l'agent :
    évaluer à k=3 alors que la production tourne à k=5 revient à noter une
    configuration qui n'existe pas. On affiche quand même k=3 comme signal plus
    strict — utile pour voir une dégradation avant qu'elle n'atteigne k=5.
    """
    index_roadmap_files()

    failures = []
    for question, expected in CASES:
        if expected not in search_roadmap(question, n_results=n_results):
            failures.append((question, expected))

    recall = (len(CASES) - len(failures)) / len(CASES)
    return recall, failures


def test_recall_production():
    """Garde-fou pytest : la config qui part en production doit tenir le seuil."""
    recall, failures = evaluate()
    assert recall >= SEUIL_RECALL, (
        f"Recall@{DEFAULT_N_RESULTS} = {recall:.0%} < seuil {SEUIL_RECALL:.0%}. "
        f"Échecs : {failures}"
    )


if __name__ == "__main__":
    recall, failures = evaluate()
    strict_recall, strict_failures = evaluate(n_results=3)

    print(f"Modèle              : {EMBED_MODEL}")
    print(f"Recall@{DEFAULT_N_RESULTS} (production) : {recall:.0%} "
          f"({len(CASES) - len(failures)}/{len(CASES)})")
    print(f"Recall@3 (strict)   : {strict_recall:.0%} "
          f"({len(CASES) - len(strict_failures)}/{len(CASES)})")

    for question, expected in failures:
        print(f"  MISS  {question}  (attendu ~{expected})")
    for question, expected in strict_failures:
        if (question, expected) not in failures:
            print(f"  (k=3 seulement)  {question}  (attendu ~{expected})")

    if recall < SEUIL_RECALL:
        print(f"\nÉCHEC : sous le seuil de {SEUIL_RECALL:.0%}.")
        sys.exit(1)

    print("\nOK : retrieval au-dessus du seuil.")
