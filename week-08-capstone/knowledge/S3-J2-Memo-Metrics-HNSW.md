# 📝 Mémo S3-J2 : Métriques de Similarité & Indexation HNSW

*Ce document valide les tâches `S3-J2-T1`, `S3-J2-T2` et `S3-J2-T4`.*

---

## 1. Les Métriques de Similarité Vectorielle
Pour comparer deux vecteurs, il existe différentes formules mathématiques selon que l'on s'intéresse uniquement à leur direction ou également à leur longueur (magnitude).

### A. Similarité Cosinus
*   **Formule** : `cos(θ) = (A · B) / (||A|| ||B||)`
*   **Intuition** : Elle ne mesure que **l'angle** entre les vecteurs et ignore complètement leur longueur. Sa valeur est toujours comprise entre **-1** (opposés) et **1** (identiques).
*   **Cas d'usage** : C'est le standard pour le texte (RAG/Recherche sémantique) car un tweet court et un long article sur le même sujet pointeront dans la même direction sémantique.

### B. Produit Scalaire (Dot Product)
*   **Formule** : `A · B = ||A|| ||B|| cos(θ)`
*   **Intuition** : Il combine la direction **et** la longueur des vecteurs. Si les vecteurs ne sont pas normalisés, sa valeur n'est pas bornée.
*   **Cas d'usage** : Utile lorsque la popularité ou la fréquence d'un élément doit influencer le résultat (ex. système de recommandation favorisant les articles populaires). Si les vecteurs ont une longueur de 1, le produit scalaire est égal au cosinus.

### C. Distance Euclidienne (L2 Distance)
*   **Formule** : `d(A, B) = √[ Σ (Ai - Bi)² ]`
*   **Intuition** : Mesure la distance physique en ligne droite entre deux points. La similarité maximale est à **0** (distance nulle).
*   **Limites** : Très sensible à la longueur des textes. Deux documents identiques mais de longueurs différentes seront éloignés dans l'espace.

### D. Distance de Manhattan (L1 Distance)
*   **Formule** : `d(A, B) = Σ |Ai - Bi|`
*   **Intuition** : Mesure la distance en suivant un quadrillage (comme les rues d'une ville).

### E. Distance de Hamming
*   **Intuition** : Utilisée pour les vecteurs binaires (composés de 0 et de 1). Elle compte le nombre de bits différents. Elle est ultra-rapide à calculer au niveau matériel (instructions processeur directes).

---

## 2. Recherche Approchée (ANN) et Indexation
Faire une recherche exacte consiste à comparer notre requête à *tous* les vecteurs de la base de données un par un. C'est une recherche linéaire bruteforce, notée **O(N)**. À grande échelle (millions de vecteurs), cette méthode est beaucoup trop lente.

La **Recherche Approchée des Plus Proches Voisins (ANN - Approximate Nearest Neighbors)** résout ce problème en acceptant une légère perte de précision en échange d'une accélération massive. Elle utilise des index pour structurer l'espace et trouver les résultats en temps sub-linéaire, noté **O(log N)**.

---

## 3. L'algorithme HNSW (Hierarchical Navigable Small World)
HNSW est l'algorithme d'indexation graphique de référence dans l'industrie pour la recherche vectorielle.

### L'analogie du Skip List (Autoroute vs. Ruelle)
HNSW transpose le concept de **Skip List** (liste à sauts) dans un graphe multi-couches :
*   **Couche supérieure (L'autoroute)** : Contient très peu de nœuds reliés par de longues distances. Permet de traverser rapidement tout le jeu de données pour se rapprocher de la cible.
*   **Couches intermédiaires (Routes nationales)** : Contient plus de nœuds et des connexions plus locales.
*   **Couche inférieure (Les rues locales)** : Contient tous les vecteurs du jeu de données avec des liens très détaillés entre voisins proches.

### Processus de recherche dans HNSW
1.  La requête entre par un nœud de départ aléatoire sur la couche supérieure.
2.  Elle navigue de nœud en nœud jusqu'à trouver le point le plus proche de la requête dans cette couche.
3.  Elle descend à la couche inférieure sur ce même nœud et reprend la recherche locale.
4.  Le processus se répète jusqu'à la couche inférieure pour affiner la recherche et renvoyer le résultat exact.

---

## 4. Benchmark MTEB (Massive Text Embedding Benchmark)
Pour choisir un modèle d'embedding, on utilise le leaderboard **MTEB** hébergé sur Hugging Face.
*   **Le besoin multilingue** : Les modèles entraînés uniquement en anglais performent mal en français. Pour nos projets, il faut choisir des modèles multilingues (ex. `BAAI/bge-m3`, `intfloat/multilingual-e5-base`, ou des modèles LLM plus lourds comme `F2LLM` ou `inf-retriever`).

---

## Flashcards (Anki / Active Recall)

#flashcard
Q: Quelle est la différence majeure entre la similarité cosinus et le produit scalaire (dot product) ?
A: La similarité cosinus ne mesure que l'angle entre deux vecteurs (indépendante de leur longueur), tandis que le produit scalaire mesure à la fois l'angle et la longueur (magnitude) des vecteurs.

#flashcard
Q: Pourquoi l'algorithme HNSW est-il plus rapide qu'une recherche brute (flat search) ?
A: Parce qu'il structure les vecteurs sous forme de graphe multi-couches (Skip List). Au lieu de comparer la requête à tous les vecteurs O(N), il navigue rapidement de couche en couche pour cibler uniquement les voisins proches O(log N).

#flashcard
Q: Qu'est-ce que la recherche ANN par rapport à la recherche KNN classique ?
A: La recherche KNN cherche les voisins exacts en parcourant tout le jeu de données (précis mais lent). L'ANN (Approximate Nearest Neighbors) cherche des voisins approximatifs très rapidement grâce à un index.

#flashcard
Q: Pourquoi le choix d'un modèle d'embedding est-il critique pour le français sur le leaderboard MTEB ?
A: Car de nombreux modèles performants sont purement anglophones. Pour traiter du français, il faut spécifiquement filtrer et sélectionner des modèles entraînés sur des données multilingues (ex: bge-m3, multilingual-e5).
