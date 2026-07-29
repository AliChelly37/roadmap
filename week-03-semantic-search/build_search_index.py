import os
import glob
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path

# Configuration des chemins
WIKI_DIR = Path("c:/Users/LENOVO/3allela/claude-obsidian/wiki")
DB_PATH = "chroma_db"
COLLECTION_NAME = "second_brain_obsidian"

print(f"📂 Indexation du Second Brain depuis '{WIKI_DIR}'...")
print(f"⏳ Initialisation de la base vectorielle Chroma DB...")

# Initialisation du client persistant
client = chromadb.PersistentClient(path=DB_PATH)

# Utilisation explicite du modèle local all-MiniLM-L6-v2 pour l'encodage
sbert_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Création (ou écrasement) de la collection
# Si elle existe déjà, on la supprime pour repartir sur une base propre
if COLLECTION_NAME in [c.name for c in client.list_collections()]:
    client.delete_collection(name=COLLECTION_NAME)

collection = client.create_collection(
    name=COLLECTION_NAME,
    embedding_function=sbert_fn
)

# Fonction de découpage en morceaux (chunking simple avec overlap)
def chunk_text(text, chunk_size=800, overlap=120):
    """
    Découpe le texte en morceaux d'environ `chunk_size` caractères,
    avec un recouvrement `overlap` pour conserver le contexte.
    Tente de couper aux limites de mots pour éviter de hacher le texte.
    """
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
            
        # Chercher un espace près de la fin théorique pour ne pas couper un mot en deux
        cut_index = text.rfind(" ", start, end)
        if cut_index != -1 and cut_index > start + (chunk_size // 2):
            end = cut_index
            
        chunks.append(text[start:end].strip())
        start = end - overlap
        
    return chunks

# Recherche récursive de tous les fichiers Markdown (.md)
md_files = glob.glob(str(WIKI_DIR / "**" / "*.md"), recursive=True)

print(f"📝 Trouvé {len(md_files)} fichiers Markdown à traiter.")

all_documents = []
all_metadatas = []
all_ids = []
chunk_count = 0

for file_path in md_files:
    file_path = Path(file_path)
    
    # Ignorer les fichiers vides ou trop petits
    if file_path.stat().st_size < 10:
        continue
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Chemin relatif pour faciliter l'affichage
        rel_path = file_path.relative_to(WIKI_DIR)
        
        # Découpe en chunks
        chunks = chunk_text(content)
        
        for idx, chunk in enumerate(chunks):
            if len(chunk.strip()) < 30:  # Ignorer les tout petits morceaux
                continue
                
            all_documents.append(chunk)
            all_metadatas.append({
                "source": str(rel_path),
                "file_name": file_path.name,
                "chunk_idx": idx
            })
            # Génère un identifiant unique en remplaçant les séparateurs de chemin
            safe_id = str(rel_path.with_suffix('')).replace(os.sep, "__").replace("/", "__")
            all_ids.append(f"{safe_id}_chunk_{idx}")
            chunk_count += 1
            
    except Exception as e:
        print(f"⚠️ Erreur lors de la lecture de {file_path.name} : {e}")

print(f"\n🚀 Indexation en cours de {chunk_count} morceaux de texte...")

# Ajouter les documents par paquets (batchs) de 100 pour éviter de surcharger Chroma
batch_size = 100
for i in range(0, len(all_documents), batch_size):
    batch_docs = all_documents[i:i+batch_size]
    batch_metas = all_metadatas[i:i+batch_size]
    batch_ids = all_ids[i:i+batch_size]
    
    collection.add(
        ids=batch_ids,
        documents=batch_docs,
        metadatas=batch_metas
    )

print(f"\n✨ Indexation terminée avec succès ! La collection '{COLLECTION_NAME}' contient désormais {collection.count()} vecteurs.")
