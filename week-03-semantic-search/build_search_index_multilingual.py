import os
import glob
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path

# Configuration des chemins
WIKI_DIR = Path("c:/Users/LENOVO/3allela/claude-obsidian/wiki")
DB_PATH = "chroma_db"
COLLECTION_NAME = "second_brain_multilingual"
MODEL_NAME = "intfloat/multilingual-e5-base"

print(f"📂 Indexation Multilingue du Second Brain depuis '{WIKI_DIR}'...")
print(f"⏳ Chargement du modèle multilingue '{MODEL_NAME}' (768 dimensions)...")

# Initialisation du client persistant
client = chromadb.PersistentClient(path=DB_PATH)

# Utilisation explicite du modèle multilingue
sbert_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=MODEL_NAME)

# Création ou réinitialisation de la collection
if COLLECTION_NAME in [c.name for c in client.list_collections()]:
    client.delete_collection(name=COLLECTION_NAME)

collection = client.create_collection(
    name=COLLECTION_NAME,
    embedding_function=sbert_fn
)

# Fonction de découpage
def chunk_text(text, chunk_size=800, overlap=120):
    chunks = []
    start = 0
    text_len = len(text)
    
    if text_len <= chunk_size:
        return [text]
        
    while start < text_len:
        end = start + chunk_size
        if end >= text_len:
            chunks.append(text[start:])
            break
            
        cut_index = text.rfind(" ", start, end)
        if cut_index != -1 and cut_index > start + (chunk_size // 2):
            end = cut_index
            
        chunks.append(text[start:end].strip())
        start = end - overlap
        
    return chunks

# Recherche des fichiers Markdown (.md)
md_files = glob.glob(str(WIKI_DIR / "**" / "*.md"), recursive=True)
print(f"📝 Trouvé {len(md_files)} fichiers Markdown.")

all_documents = []
all_metadatas = []
all_ids = []
chunk_count = 0

for file_path in md_files:
    file_path = Path(file_path)
    if file_path.stat().st_size < 10:
        continue
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        rel_path = file_path.relative_to(WIKI_DIR)
        chunks = chunk_text(content)
        
        for idx, chunk in enumerate(chunks):
            # Remplacement des tabulations pour éviter le bug de décalage dans le terminal
            clean_chunk = chunk.replace("\t", "    ")
            if len(clean_chunk.strip()) < 30:
                continue
            
            # CRITIQUE : Le modèle E5 exige que chaque document commence par le préfixe "passage: "
            formatted_document = f"passage: {clean_chunk}"
            
            all_documents.append(formatted_document)
            all_metadatas.append({
                "source": str(rel_path),
                "file_name": file_path.name,
                "chunk_idx": idx
            })
            # ID unique basé sur le chemin relatif
            safe_id = str(rel_path.with_suffix('')).replace(os.sep, "__").replace("/", "__")
            all_ids.append(f"multi__{safe_id}_chunk_{idx}")
            chunk_count += 1
            
    except Exception as e:
        print(f"⚠️ Erreur sur {file_path.name} : {e}")

print(f"\n🚀 Indexation en cours de {chunk_count} morceaux de texte (Modèle Multilingue)...")

# Batch indexation
batch_size = 64
for i in range(0, len(all_documents), batch_size):
    batch_docs = all_documents[i:i+batch_size]
    batch_metas = all_metadatas[i:i+batch_size]
    batch_ids = all_ids[i:i+batch_size]
    
    collection.add(
        ids=batch_ids,
        documents=batch_docs,
        metadatas=batch_metas
    )

print(f"\n✨ Indexation multilingue terminée ! La collection '{COLLECTION_NAME}' contient {collection.count()} vecteurs.")
