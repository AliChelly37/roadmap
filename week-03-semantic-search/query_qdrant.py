import sys
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models

MODEL_NAME = "intfloat/multilingual-e5-base"
COLLECTION_NAME = "second_brain_obsidian"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

# Initialisation du client Qdrant et de l'encodeur sémantique
q_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
encoder = SentenceTransformer(MODEL_NAME)

# Vérifier si la collection existe dans Qdrant
if not q_client.collection_exists(collection_name=COLLECTION_NAME):
    print(f"❌ Erreur : La collection '{COLLECTION_NAME}' n'existe pas. Lance d'abord 'build_qdrant_index.py'.")
    sys.exit(1)

def run_qdrant_search(query_text, k=3, category_filter=None):
    # CRITIQUE : Le modèle E5 exige le préfixe "query: "
    formatted_query = f"query: {query_text}"
    query_vector = encoder.encode(formatted_query).tolist()
    
    # Construction du filtre de métadonnées si demandé (S3-J5-T2 bonus)
    qdrant_filter = None
    if category_filter:
        print(f"\n🏷️ Application du filtre Qdrant: [source contient '{category_filter}']")
        qdrant_filter = models.Filter(
            must=[
                models.FieldCondition(
                    key="source",
                    match=models.MatchText(text=category_filter)
                )
            ]
        )
        
    print(f"\n🔍 Recherche sémantique Qdrant pour : '{query_text}'...")
    
    # Recherche vectorielle dans Qdrant (utilisation de query_points)
    search_results = q_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=qdrant_filter,
        limit=k
    )
    
    if not search_results.points:
        print("🤷 Aucun résultat trouvé.")
        return
        
    print("\n📝 --- RÉSULTATS DE LA RECHERCHE (QDRANT) ---")
    for idx, hit in enumerate(search_results.points):
        print(f"\n[{idx+1}] 🎯 Score de Similarité Cosinus : {hit.score:.4f}")
        print(f"    📄 Fichier source : {hit.payload['source']} (Morceau #{hit.payload['chunk_idx']})")
        print(f"    🆔 Point ID (UUID v5) : {hit.id}")
        print(f"    --------------------------------------------------")
        
        # Nettoyage et indentation pour l'affichage console
        raw_doc = hit.payload["document"]
        clean_doc = raw_doc.replace("\r\n", "\n").replace("\r", "\n").replace("\t", "    ")
        indented_doc = "\n".join([f"    {line}" for line in clean_doc.split("\n")])
        print(indented_doc)
        print(f"    --------------------------------------------------")

if __name__ == "__main__":
    # Permet de passer le filtre en second argument
    # Ex: python query_qdrant.py "transformers" "memos"
    query = "Système d'exploitation LLM et RAM"
    filter_val = None
    
    if len(sys.argv) > 1:
        query = sys.argv[1]
    if len(sys.argv) > 2:
        filter_val = sys.argv[2]
        
    if len(sys.argv) == 1:
        print("💡 Astuce : python query_qdrant.py \"requête\" \"filtre_de_source\"\n")
        
    run_qdrant_search(query, k=3, category_filter=filter_val)
