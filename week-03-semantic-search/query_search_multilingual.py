import sys
import chromadb
from chromadb.utils import embedding_functions

DB_PATH = "chroma_db"
COLLECTION_NAME = "second_brain_multilingual"
MODEL_NAME = "intfloat/multilingual-e5-base"

# Initialisation du client persistant
client = chromadb.PersistentClient(path=DB_PATH)

# Utilisation du même modèle multilingue
sbert_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)

# Vérifier si la collection existe
if COLLECTION_NAME not in [c.name for c in client.list_collections()]:
    print(f"❌ Erreur : La collection '{COLLECTION_NAME}' n'existe pas. Lance d'abord 'build_search_index_multilingual.py'.")
    sys.exit(1)

collection = client.get_collection(
    name=COLLECTION_NAME,
    embedding_function=sbert_fn
)

def run_search(query_text, k=3):
    # CRITIQUE : Le modèle E5 exige que la requête commence par le préfixe "query: "
    formatted_query = f"query: {query_text}"
    
    print(f"\n🌍 Recherche Sémantique Multilingue pour : '{query_text}'...")
    
    results = collection.query(
        query_texts=[formatted_query],
        n_results=k
    )
    
    ids = results["ids"][0]
    documents = results["documents"][0]
    distances = results["distances"][0]
    metadatas = results["metadatas"][0]
    
    if not ids:
        print("🤷 Aucun résultat trouvé.")
        return
        
    print("\n📝 --- RÉSULTATS DE LA RECHERCHE (MULTILINGUE) ---")
    for i in range(len(ids)):
        # Retirer le préfixe "passage: " s'il est présent pour l'affichage
        raw_doc = documents[i]
        if raw_doc.startswith("passage: "):
            raw_doc = raw_doc[len("passage: "):]
            
        print(f"\n[{i+1}] 🎯 Match Score (Distance L2) : {distances[i]:.4f}")
        print(f"    📄 Fichier source : {metadatas[i]['source']} (Morceau #{metadatas[i]['chunk_idx']})")
        print(f"    --------------------------------------------------")
        
        # Nettoyage complet pour éviter le bug de terminal (retours chariots, tabulations)
        clean_doc = raw_doc.replace("\r\n", "\n").replace("\r", "\n").replace("\t", "    ")
        indented_doc = "\n".join([f"    {line}" for line in clean_doc.split("\n")])
        print(indented_doc)
        print(f"    --------------------------------------------------")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "Système d'exploitation LLM et RAM"
        print("💡 Astuce : Tu peux passer ta requête en argument dans le terminal.")
        print(f"   Exemple : python query_search_multilingual.py \"réseau de neurones\"\n")
        
    run_search(query)
