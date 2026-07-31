import fitz  # PyMuPDF
import os
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Configuration
PDF_FILE = "document_test.pdf"
DB_PATH = "chroma_db"
COLLECTION_NAME = "rag_document_test"
MODEL_NAME = "intfloat/multilingual-e5-base"

# Initialisation du découpeur de texte récursif (RecursiveCharacterTextSplitter)
# S4-J2-T2 : chunk_size=500, chunk_overlap=100
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    length_function=len
)

print(f"Lecture et decoupage du fichier PDF '{PDF_FILE}'...")
doc = fitz.open(PDF_FILE)

all_chunks = []
all_metadatas = []
all_ids = []
chunk_global_idx = 0

# Ingestion page par page pour conserver le numéro de page dans les métadonnées
for page_idx in range(len(doc)):
    page = doc.load_page(page_idx)
    page_text = page.get_text()
    page_num = page_idx + 1  # 1-indexed
    
    # Découpage du texte de cette page spécifique
    chunks = text_splitter.split_text(page_text)
    
    print(f"  Page {page_num} : decoupee en {len(chunks)} morceaux.")
    
    for local_idx, chunk in enumerate(chunks):
        # Nettoyage des tabulations pour le terminal
        clean_chunk = chunk.replace("\t", "    ").strip()
        if len(clean_chunk) < 15:
            continue
            
        # CRITIQUE E5 : Ajouter le préfixe "passage: " sur chaque morceau de texte indexé
        formatted_chunk = f"passage: {clean_chunk}"
        
        all_chunks.append(formatted_chunk)
        
        # S4-J2-T2 : Propagation des métadonnées (chemin source + numéro de page)
        all_metadatas.append({
            "source": PDF_FILE,
            "page": page_num,
            "local_chunk_idx": local_idx
        })
        
        # Génération d'un identifiant unique pour Chroma
        all_ids.append(f"chunk_p{page_num}_{local_idx}")
        chunk_global_idx += 1

# S4-J2-T3 : Visualisation et validation de la cohérence des chunks
print("\n--- S4-J2-T3 : INSPECTION VISUELLE DES CHUNKS ---")
for i in range(len(all_chunks)):
    # Retirer le préfixe pour afficher le texte propre lors de la visualisation
    display_text = all_chunks[i][len("passage: "):]
    print(f"\nChunk #{i+1} [ID: {all_ids[i]}] [Taille: {len(display_text)} chars]")
    print(f"    Metadonnees : {all_metadatas[i]}")
    print(f"    --------------------------------------------------")
    indented_text = "\n".join([f"    {line}" for line in display_text.split("\n")])
    print(indented_text)
    print(f"    --------------------------------------------------")

# S4-J2-T4 : Indexation dans Chroma DB
print(f"\nConnexion a Chroma DB dans '{DB_PATH}'...")
client = chromadb.PersistentClient(path=DB_PATH)

sbert_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)

# Supprimer la collection si elle existe pour réindexer proprement
if COLLECTION_NAME in [c.name for c in client.list_collections()]:
    client.delete_collection(name=COLLECTION_NAME)

collection = client.create_collection(
    name=COLLECTION_NAME,
    embedding_function=sbert_fn
)

print(f"Inscription des {len(all_chunks)} chunks dans la collection '{COLLECTION_NAME}'...")
collection.add(
    ids=all_ids,
    documents=all_chunks,
    metadatas=all_metadatas
)

print(f"Indexation Chroma completee ! La collection '{COLLECTION_NAME}' contient {collection.count()} chunks vectorises.")
