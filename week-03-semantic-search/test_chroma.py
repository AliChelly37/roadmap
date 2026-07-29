import chromadb
import os

# Dossier local où Chroma va écrire les données sur le disque dur
DB_PATH = "chroma_db"

print(f"⏳ Initialisation du client persistant Chroma DB dans le dossier '{DB_PATH}'...")
# S3-J3-T2 : Utilisation de PersistentClient pour assurer la persistance sur disque
client = chromadb.PersistentClient(path=DB_PATH)

# Nom de notre collection de test
COLLECTION_NAME = "mon_debarras_semantique"

# Vérifier si la base de données contient déjà notre collection (pour tester la persistance)
collection_existante = COLLECTION_NAME in [c.name for c in client.list_collections()]

# S3-J3-T2 : Création ou récupération de la collection
collection = client.get_or_create_collection(name=COLLECTION_NAME)

if not collection_existante:
    print(f"\n📂 Collection '{COLLECTION_NAME}' vide. Ajout de nouveaux documents de test...")
    
    # 5 Documents de test avec des sources et des catégories variées
    documents = [
        "Les chiens sont des animaux domestiques très fidèles et protecteurs.",
        "Le chat noir adore dormir paisiblement sur le canapé au soleil.",
        "La programmation en Python utilise des concepts d'objets et de fonctions.",
        "Docker permet de packager des applications avec toutes leurs dépendances.",
        "Les félins sauvages aiment chasser de petites proies pendant la nuit."
    ]
    
    # Métadonnées associées à chaque document (pour tester le filtrage)
    metadatas = [
        {"source": "articles", "category": "animaux", "date": "2026-07-21"},
        {"source": "memos", "category": "animaux", "date": "2026-07-22"},
        {"source": "cours", "category": "informatique", "date": "2026-07-23"},
        {"source": "cours", "category": "informatique", "date": "2026-07-24"},
        {"source": "articles", "category": "animaux", "date": "2026-07-25"}
    ]
    
    # Identifiants uniques pour chaque document
    ids = ["doc_chien", "doc_chat", "doc_python", "doc_docker", "doc_felin"]
    
    # S3-J3-T2 : Ajout des documents dans la collection. 
    # Note : Puisque nous ne passons pas le paramètre 'embeddings', Chroma va automatiquement
    # utiliser son modèle par défaut (all-MiniLM-L6-v2) pour générer les vecteurs.
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    print("✅ Documents ajoutés avec succès !")
else:
    # S3-J3-T4 : Si la collection existe déjà, cela prouve que les données ont survécu au redémarrage
    print(f"\n💾 Données chargées depuis le disque dur (Persistance OK). Nombre de documents : {collection.count()}")

# --- S3-J3-T3 : Requêtes de recherche sémantique ---

# Requête 1 : Recherche sémantique simple
query_1 = "animaux de compagnie"
print(f"\n🔍 1. Recherche sémantique simple pour : '{query_1}' (top 2)")
results_1 = collection.query(
    query_texts=[query_1],
    n_results=2
)

# Affichage des résultats
for i in range(len(results_1["ids"][0])):
    print(f"  [{i+1}] ID : {results_1['ids'][0][i]}")
    print(f"      Document : {results_1['documents'][0][i]}")
    print(f"      Distance (L2) : {results_1['distances'][0][i]:.4f}")
    print(f"      Métadonnées : {results_1['metadatas'][0][i]}")

# Requête 2 : Recherche sémantique avec filtrage par métadonnées (where)
query_2 = "développement logiciel et conteneurs"
print(f"\n🔍 2. Recherche avec filtre (source = 'cours') pour : '{query_2}' (top 2)")
results_2 = collection.query(
    query_texts=[query_2],
    n_results=2,
    where={"source": "cours"} # Filtre de métadonnées
)

# Affichage des résultats filtrés
for i in range(len(results_2["ids"][0])):
    print(f"  [{i+1}] ID : {results_2['ids'][0][i]}")
    print(f"      Document : {results_2['documents'][0][i]}")
    print(f"      Distance (L2) : {results_2['distances'][0][i]:.4f}")
    print(f"      Métadonnées : {results_2['metadatas'][0][i]}")
