import os
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

ROADMAP_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DB_PATH = Path(__file__).resolve().parent.parent / "chroma_db"

def get_collection():
    """Initialise et retourne la collection ChromaDB pour le RAG."""
    client = chromadb.PersistentClient(path=str(DB_PATH))
    # Utilisation du modèle multilingual pour gérer le français
    sbert_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="intfloat/multilingual-e5-base")
    
    # get_or_create_collection pour ne pas crasher si elle existe déjà
    collection = client.get_or_create_collection(
        name="roadmap_knowledge",
        embedding_function=sbert_fn
    )
    return collection

def index_roadmap_files():
    """Indexe tous les fichiers markdown de la roadmap dans ChromaDB."""
    collection = get_collection()
    
    # On évite de réindexer si c'est déjà fait
    if collection.count() > 0:
        print(f"[RAG] Base déjà indexée avec {collection.count()} documents.")
        return

    print("[RAG] Début de l'indexation de la roadmap...")
    docs = []
    metadatas = []
    ids = []
    
    doc_id = 0
    # Parcourir les fichiers de la roadmap
    for md_file in ROADMAP_ROOT.glob("*.md"):
        if md_file.name == "PROGRESS_TRACKER.md":
            continue # Optionnel, on peut exclure certains fichiers
            
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Stratégie de chunking basique par paragraphes
            paragraphs = [p for p in content.split("\n\n") if len(p.strip()) > 50]
            
            for p_id, chunk in enumerate(paragraphs):
                docs.append(chunk)
                metadatas.append({"source": md_file.name, "chunk_id": p_id})
                ids.append(f"doc_{doc_id}")
                doc_id += 1
                
        except Exception as e:
            print(f"Erreur de lecture {md_file.name}: {e}")

    # Ajout par lots pour éviter les limites
    batch_size = 100
    for i in range(0, len(docs), batch_size):
        collection.add(
            documents=docs[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size],
            ids=ids[i:i+batch_size]
        )
    print(f"[RAG] Indexation terminée : {doc_id} chunks indexés.")

def search_roadmap(query: str, n_results: int = 3) -> str:
    """Recherche dans la base vectorielle."""
    collection = get_collection()
    
    results = collection.query(
        query_texts=[f"query: {query}"],
        n_results=n_results
    )
    
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    
    if not documents:
        return "Aucune information trouvée dans la roadmap."
        
    formatted_docs = []
    for idx, doc in enumerate(documents):
        source = metadatas[idx].get('source', 'Inconnue') if idx < len(metadatas) else 'Inconnue'
        formatted_docs.append(f"Source: {source}\nContenu:\n{doc}")
        
    return "\n\n---\n\n".join(formatted_docs)

if __name__ == "__main__":
    # Test unitaire rapide
    index_roadmap_files()
    print("Test de recherche :", search_roadmap("Qu'est-ce que LiteLLM ?"))
