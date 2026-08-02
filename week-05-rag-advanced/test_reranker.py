import os
import sys
from sentence_transformers import CrossEncoder

try:
    print("Loading local CrossEncoder BAAI/bge-reranker-v2-m3...")
    # Load cross-encoder. It will download the weights if not cached.
    # We set trust_remote_code=True if needed, but BAAI is a standard architecture
    model = CrossEncoder("BAAI/bge-reranker-v2-m3")
    print("CrossEncoder loaded successfully!")
    
    query = "Qu'est-ce que le protocole Raft ?"
    documents = [
        "Le protocole Raft décompose le consensus en l'élection du leader, la réplication des logs et la sécurité.",
        "Paxos est un autre algorithme de consensus distribué plus ancien et plus complexe.",
        "Le gâteau au chocolat contient de la farine, du sucre, des œufs et du chocolat fondu."
    ]
    
    # Prepare inputs: list of [query, document] pairs
    pairs = [[query, doc] for doc in documents]
    
    print("\nPredicting relevance scores...")
    scores = model.predict(pairs)
    print("Scores computed:", scores)
    
    # Sort docs by score
    sorted_results = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
    print("\nSorted results:")
    for doc, score in sorted_results:
        print(f"Score: {score:.4f} | Doc: {doc}")
        
except Exception as e:
    import traceback
    print("Error:")
    traceback.print_exc()
