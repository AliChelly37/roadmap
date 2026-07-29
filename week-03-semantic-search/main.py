import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import chromadb
from chromadb.utils import embedding_functions

app = FastAPI(
    title="Second Brain Semantic Search API",
    description="API de recherche sémantique sur vos notes Obsidian.",
    version="1.0.0"
)

DB_PATH = "chroma_db"
COLLECTION_ENG = "second_brain_obsidian"
COLLECTION_MULTI = "second_brain_multilingual"

# Initialisation du client Chroma
client = chromadb.PersistentClient(path=DB_PATH)

# Modèles d'embeddings pour les requêtes
sbert_fn_eng = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
sbert_fn_multi = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="intfloat/multilingual-e5-base")

# Récupération des collections
col_eng = client.get_collection(name=COLLECTION_ENG, embedding_function=sbert_fn_eng)
col_multi = client.get_collection(name=COLLECTION_MULTI, embedding_function=sbert_fn_multi)

@app.get("/search")
def search_notes(
    q: str = Query(..., description="La requête de recherche sémantique"),
    model: str = Query("multilingual", description="Le modèle à utiliser: 'english' ou 'multilingual'"),
    limit: int = Query(3, ge=1, le=10, description="Nombre de résultats à retourner"),
    source_filter: str = Query(None, description="Filtre sur le chemin source du document")
):
    """
    Effectue une recherche sémantique sur les notes de votre Second Brain.
    """
    # Sélection de la collection appropriée
    if model == "english":
        collection = col_eng
        formatted_query = q
    else:
        collection = col_multi
        # Le modèle E5 exige le préfixe "query: " pour les requêtes
        formatted_query = f"query: {q}"
        
    # Définition du filtre where si un filtre source est passé
    where_filter = None
    if source_filter and source_filter.strip() != "":
        where_filter = {"source": {"$contains": source_filter.strip()}}
        
    # Requête de la collection
    results = collection.query(
        query_texts=[formatted_query],
        n_results=limit,
        where=where_filter
    )
    
    # Transformation des résultats dans un format propre pour le frontend
    formatted_results = []
    
    ids = results["ids"][0]
    documents = results["documents"][0]
    distances = results["distances"][0]
    metadatas = results["metadatas"][0]
    
    for i in range(len(ids)):
        raw_doc = documents[i]
        
        # Supprimer le préfixe "passage: " si le modèle E5 est utilisé
        if model == "multilingual" and raw_doc.startswith("passage: "):
            raw_doc = raw_doc[len("passage: "):]
            
        # Nettoyage des caractères spéciaux d'affichage
        clean_doc = raw_doc.replace("\r\n", "\n").replace("\r", "\n").replace("\t", "    ")
        
        formatted_results.append({
            "id": ids[i],
            "score": round(distances[i], 4),
            "source": metadatas[i]["source"],
            "file_name": metadatas[i]["file_name"],
            "chunk_idx": metadatas[i]["chunk_idx"],
            "text": clean_doc
        })
        
    return {
        "query": q,
        "model_used": model,
        "results_count": len(formatted_results),
        "results": formatted_results
    }

# Endpoint racine servant l'interface utilisateur (UI)
@app.get("/", response_class=HTMLResponse)
def read_root():
    # Si le fichier index.html existe, on le lit et le renvoie
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Interface index.html manquante.</h1>")
