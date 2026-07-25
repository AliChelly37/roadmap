import numpy as np
from sentence_transformers import SentenceTransformer, util

# 1. Chargement du modèle d'embedding léger
# 'all-MiniLM-L6-v2' est ultra-rapide, léger et génère des vecteurs de 384 dimensions.
print("⏳ Chargement du modèle all-MiniLM-L6-v2...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Liste de phrases à encoder
# Nous avons préparé des phrases ayant des sens proches et d'autres complètement différentes.
phrases = [
    "Le chat dort paisiblement sur le canapé.",             # A
    "Un félin fait sa sieste sur le sofa.",                  # B (Proche de A)
    "La voiture roule à vive allure sur l'autoroute.",       # C (Différente)
    "Python est un langage de programmation très populaire.", # D (Différente)
    "J'adore coder des scripts avec le langage Python.",     # E (Proche de D)
]

print(f"\n🚀 Encodage de {len(phrases)} phrases...")
# model.encode génère la liste d'embeddings (tableaux NumPy)
embeddings = model.encode(phrases, convert_to_numpy=True)

# 3. Affichage des informations sur les vecteurs générés (S3-J1-T3)
print("\n--- 📊 Analyse des Vecteurs (Embeddings) ---")
for i, phrase in enumerate(phrases):
    vector = embeddings[i]
    print(f"\nPhrase {i+1} : '{phrase}'")
    print(f"  -> Type : {type(vector)}")
    print(f"  -> Dimension du vecteur : {vector.shape}")
    print(f"  -> Aperçu des 5 premières valeurs : {vector[:5]}")

# 4. Calcul manuel de la similarité cosinus avec NumPy (S3-J1-T4)
def manual_cosine_similarity(v1, v2):
    """Calcule le cosinus de l'angle entre deux vecteurs."""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2)

# 5. Comparaison des paires et affichage des scores de similarité
print("\n--- ⚖️ Comparaison des similarités cosinus ---")

# Comparaison entre phrase 1 (chat sur le canapé) et phrase 2 (félin sur le sofa)
sim_AB_manual = manual_cosine_similarity(embeddings[0], embeddings[1])
# Comparaison avec la fonction intégrée de sentence-transformers pour valider
sim_AB_util = util.cos_sim(embeddings[0], embeddings[1]).item()

print(f"\nComparaison Chat/Félin (proches sémantiquement) :")
print(f"  - Phrase 1 : '{phrases[0]}'")
print(f"  - Phrase 2 : '{phrases[1]}'")
print(f"  -> Similarité cosinus (NumPy) : {sim_AB_manual:.4f}")
print(f"  -> Similarité cosinus (SBERT util) : {sim_AB_util:.4f}")

# Comparaison entre phrase 1 (chat) et phrase 3 (voiture)
sim_AC = manual_cosine_similarity(embeddings[0], embeddings[2])
print(f"\nComparaison Chat/Voiture (non reliées) :")
print(f"  - Phrase 1 : '{phrases[0]}'")
print(f"  - Phrase 3 : '{phrases[2]}'")
print(f"  -> Similarité cosinus : {sim_AC:.4f}")

# Comparaison entre phrase 4 (langage Python) et phrase 5 (coder en Python)
sim_DE = manual_cosine_similarity(embeddings[3], embeddings[4])
print(f"\nComparaison Programmation Python (proches sémantiquement) :")
print(f"  - Phrase 4 : '{phrases[3]}'")
print(f"  - Phrase 5 : '{phrases[4]}'")
print(f"  -> Similarité cosinus : {sim_DE:.4f}")
