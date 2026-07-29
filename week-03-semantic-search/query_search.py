import sys
import chromadb
from chromadb.utils import embedding_functions

DB_PATH = "chroma_db"
COLLECTION_NAME = "second_brain_obsidian"

# Initialisation du client persistant
client = chromadb.PersistentClient(path=DB_PATH)

# Utilisation du même modèle d'embedding
sbert_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Vérifier si la collection existe
if COLLECTION_NAME not in [c.name for c in client.list_collections()]:
    print(f"❌ Erreur : La collection '{COLLECTION_NAME}' n'existe pas. Lance d'abord 'build_search_index.py' pour indexer tes notes.")
    sys.exit(1)

collection = client.get_collection(
    name=COLLECTION_NAME,
    embedding_function=sbert_fn
)

def run_search(query_text, k=3):
    print(f"\n🔍 Recherche sémantique dans ton Second Brain pour : '{query_text}'...")
    
    results = collection.query(
        query_texts=[query_text],
        n_results=k
    )
    
    ids = results["ids"][0]
    documents = results["documents"][0]
    distances = results["distances"][0]
    metadatas = results["metadatas"][0]
    
    if not ids:
        print("🤷 Aucun résultat trouvé.")
        return
        
    print("\n📝 --- RÉSULTATS DE LA RECHERCHE ---")
    for i in range(len(ids)):
        print(f"\n[{i+1}] 🎯 Match Score (Distance L2) : {distances[i]:.4f}")
        print(f"    📄 Fichier source : {metadatas[i]['source']} (Morceau #{metadatas[i]['chunk_idx']})")
        print(f"    --------------------------------------------------")
        # Nettoyer les retours chariots (\r\n et \r) pour éviter d'écraser la console Windows
        clean_doc = documents[i].replace("\r\n", "\n").replace("\r", "\n")
        indented_doc = "\n".join([f"    {line}" for line in clean_doc.split("\n")])
        print(indented_doc)
        print(f"    --------------------------------------------------")

if __name__ == "__main__":
    # Récupère la requête passée en paramètre dans le terminal
    # Ex: python query_search.py "transformers"
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        # Requête de test par défaut
        query = "Système d'exploitation LLM et RAM"
        print("💡 Astuce : Tu peux passer ta requête en argument dans le terminal.")
        print(f"   Exemple : python query_search.py \"réseau de neurones\"\n")
        
    run_search(query)
