# 📝 Mémo S3-J3 : Fondations Chroma DB

*Ce document valide les tâches `S3-J3-T1` à `S3-J3-T4`.*

---

## 1. Qu'est-ce que Chroma DB ?
Chroma DB est une base de données vectorielle open-source, ultra-légère et conçue pour s'exécuter **in-process** (c'est-à-dire directement à l'intérieur de notre application Python, sans avoir besoin de lancer un serveur lourd séparé). 
*   **Analogie** : Chroma DB est pour les vecteurs ce que **SQLite** est pour les données relationnelles.

---

## 2. In-Memory vs. Persistent Client
Chroma propose deux modes de fonctionnement selon les besoins de persistance des données :

| Type de Client | Emplacement de stockage | Comportement à l'arrêt du script | Cas d'usage principal |
|---|---|---|---|
| **Client en mémoire** (`chromadb.Client()`) | Mémoire vive (RAM) | **Perte totale** immédiate de toutes les données | Tests unitaires, prototypages rapides, scripts jetables |
| **Client persistant** (`chromadb.PersistentClient(path)`) | Fichiers sur le disque dur | **Sauvegarde permanente** ; survit aux redémarrages | Applications de production, RAG locaux, moteurs de recherche sémantique |

---

## 3. Le concept de "Collection"
Dans Chroma, les données sont organisées en **Collections**.
*   **Équivalent SQL** : Une collection est l'équivalent d'une **Table** dans une base de données relationnelle.
*   **Contenu d'une collection** : Elle regroupe des documents textuels, leurs identifiants uniques (`ids`), leurs embeddings vectoriels (`embeddings`), et leurs dictionnaires d'informations associées (`metadatas`).

---

## 4. Génération d'embeddings par défaut
Chroma DB est conçu pour simplifier le développement :
*   **Intégration transparente** : Si vous ajoutez des documents texte avec `collection.add(...)` sans fournir de vecteurs numériques, Chroma ne plante pas. Il utilise par défaut son propre modèle embarqué (`all-MiniLM-L6-v2`) pour calculer automatiquement les embeddings en arrière-plan.
*   **Personnalisation** : Pour les projets réels (ex. requêtes en français), on désactive souvent ce comportement pour passer manuellement nos propres vecteurs calculés via un modèle plus performant.

---

## 5. Filtrage par Métadonnées (`where`)
Lors de la recherche sémantique, il est souvent nécessaire de restreindre les résultats à un certain contexte (ex. chercher uniquement dans la documentation technique et pas dans les actualités).
*   **Le paramètre `where`** : Permet de filtrer sur les valeurs du dictionnaire `metadatas` associé aux documents.
*   **Fonctionnement** : La base de données filtre d'abord ou pendant la recherche pour ne retourner que les voisins les plus proches qui valident la condition.

```python
results = collection.query(
    query_texts=["ma requête"],
    n_results=3,
    where={"source": "cours"}  # Filtre uniquement les documents de source "cours"
)
```

---

## Flashcards (Anki / Active Recall)

#flashcard
Q: Quelle est la différence de persistance entre `chromadb.Client()` et `chromadb.PersistentClient()` ?
A: `chromadb.Client()` stocke les données en RAM (les données disparaissent à la fin du script). `chromadb.PersistentClient(path)` écrit les données sur le disque dur (les données survivent aux redémarrages).

#flashcard
Q: Que fait Chroma DB par défaut si l'on ajoute des documents textuels sans fournir d'embeddings ?
A: Il calcule automatiquement les vecteurs en arrière-plan en utilisant son modèle par défaut (all-MiniLM-L6-v2).

#flashcard
Q: À quoi correspond le concept de "Collection" dans Chroma DB ?
A: C'est l'équivalent d'une table SQL. Il s'agit d'un groupe logique stockant des documents, leurs identifiants, leurs métadonnées et leurs embeddings.

#flashcard
Q: Comment réalise-t-on un filtrage par métadonnées lors d'une recherche dans Chroma DB ?
A: En passant un dictionnaire de filtres au paramètre `where` de la méthode `collection.query()`.
