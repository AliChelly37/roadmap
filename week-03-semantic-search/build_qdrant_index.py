import os
import glob
import uuid
from pathlib import Path
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Configuration
WIKI_DIR = Path("c:/Users/LENOVO/3allela/claude-obsidian/wiki")
MODEL_NAME = "intfloat/multilingual-e5-base"
COLLECTION_NAME = "second_brain_obsidian"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

print(f"📂 Indexation dans Qdrant depuis '{WIKI_DIR}'...")
print(f"⏳ Chargement du modèle sémantique '{MODEL_NAME}' en local...")
encoder = SentenceTransformer(MODEL_NAME)

print(f"🔌 Connexion à Qdrant sur {QDRANT_HOST}:{QDRANT_PORT}...")
q_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Configuration de la dimension du modèle E5 (768)
vector_size = 768

# Réinitialisation de la collection Qdrant
if q_client.collection_exists(collection_name=COLLECTION_NAME):
    print(f"🗑️ La collection '{COLLECTION_NAME}' existe déjà. Suppression...")
    q_client.delete_collection(collection_name=COLLECTION_NAME)

print(f"🧱 Création de la collection '{COLLECTION_NAME}'...")
q_client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=models.VectorParams(
        size=vector_size,
        distance=models.Distance.COSINE  # Cosine similarity
    )
)

# Fonction de chunking
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

# Recherche des fichiers
md_files = glob.glob(str(WIKI_DIR / "**" / "*.md"), recursive=True)
print(f"📝 Trouvé {len(md_files)} fichiers Markdown.")

points = []
point_count = 0

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
            clean_chunk = chunk.replace("\t", "    ")
            if len(clean_chunk.strip()) < 30:
                continue
                
            # Préfixe obligatoire pour E5
            formatted_document = f"passage: {clean_chunk}"
            
            # Encodage du passage
            vector = encoder.encode(formatted_document).tolist()
            
            # Identifiant unique déterministe (UUID v5 basé sur le nom du fichier et l'index du chunk)
            safe_id_str = f"{rel_path}_chunk_{idx}"
            point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, safe_id_str))
            
            # Payload (métadonnées + document d'origine)
            payload = {
                "source": str(rel_path),
                "file_name": file_path.name,
                "chunk_idx": idx,
                "document": clean_chunk
            }
            
            # Ajouter au format Qdrant PointStruct
            points.append(models.PointStruct(
                id=point_id,
                vector=vector,
                payload=payload
            ))
            point_count += 1
            
    except Exception as e:
        print(f"⚠️ Erreur sur {file_path.name} : {e}")

print(f"\n🚀 Téléchargement de {point_count} points vers la base Qdrant...")

# Téléversement en masse (batch upload)
q_client.upload_points(
    collection_name=COLLECTION_NAME,
    points=points
)

print(f"\n✨ Indexation Qdrant terminée ! Nombre de points stockés : {q_client.get_collection(COLLECTION_NAME).points_count}")
