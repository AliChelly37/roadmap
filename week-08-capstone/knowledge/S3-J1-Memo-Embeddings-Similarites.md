# 📝 Mémo S3-J1 : Embeddings & Similarités

*Ce document valide les tâches `S3-J1-T1` à `S3-J1-T4`.*

---

## 1. Qu'est-ce qu'un Embedding ?
Un **embedding** (ou plongement lexical) est le processus de traduction d'un token, d'un mot ou d'une phrase complète en un **vecteur dense** de nombres réels dans un espace à haute dimension (ex. 384 dimensions pour le modèle léger `all-MiniLM-L6-v2`).

*   **Le concept clé** : Au lieu d'une représentation littérale ou séquentielle (comme le One-Hot Encoding), les nombres d'un vecteur d'embedding capturent des concepts sémantiques.
*   **La géométrie du sens** : Les mots ou les phrases qui partagent un sens ou un contexte similaire se retrouvent géométriquement proches dans cet espace vectoriel.

---

## 2. Comment le modèle apprend-il le sens ?
Le modèle d'embedding est un réseau de neurones entraîné sur d'immenses volumes de données textuelles.
1.  **L'apprentissage par le contexte** : Le modèle ajuste ses poids (ses paramètres) en essayant de prédire un mot en fonction de son contexte (mots environnants).
2.  **Ajustement des poids** : Si deux mots ("roi" et "reine") apparaissent régulièrement dans des phrases similaires (autour de termes comme "trône", "couronne", "gouverner"), le réseau décale leurs coordonnées vectorielles pour les regrouper.
3.  **Axes de sens** : Différentes dimensions du vecteur représentent différents aspects du sens (le genre, le caractère vivant ou inanimé, la royauté, etc.), même si ces axes ne sont pas nommés explicitement par l'ordinateur.

---

## 3. Similarité Cosinus : L'outil de comparaison sémantique
Pour comparer la ressemblance sémantique de deux phrases, on calcule le **cosinus de l'angle ($\theta$)** formé par leurs deux vecteurs.

$$\text{similarité\_cosinus}(\mathbf{A}, \mathbf{B}) = \cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$$

*   **Pourquoi le Cosinus ?** Contrairement à la distance euclidienne ($L_2$) qui mesure la distance en ligne droite entre deux points, la similarité cosinus ne s'intéresse qu'à la **direction** des vecteurs.
*   **Indépendance de la taille** : Ainsi, un texte court (vecteur court) et un texte long (vecteur long) traitant du même sujet pointeront dans la même direction et auront une similarité cosinus élevée, évitant les biais de longueur.

---

## 4. Pourquoi des bases de données vectorielles ?
Les bases de données relationnelles traditionnelles (SQL) ou documentaires (MongoDB) utilisent des index de type **B-Tree**, optimisés pour trier et chercher sur une seule dimension (ex. ID, date, texte exact).
*   **Limites de l'indexation 1D** : Chercher le voisin le plus proche dans un espace à 384 ou 1536 dimensions avec un B-Tree est impossible.
*   **Besoins des bases vectorielles** : Les bases spécialisées (Chroma, Qdrant) stockent des coordonnées multi-dimensionnelles et construisent des **index vectoriels** (comme HNSW) pour accélérer la recherche de voisins proches sans faire de recherche séquentielle brute (brute-force).

---

## 5. La similarité de fond (L'anisotropie)
Lors des tests pratiques, des phrases sans rapport sémantique direct (ex. un chat qui dort vs. une voiture sur l'autoroute) peuvent afficher un score de similarité cosinus de **~0.45** au lieu de **0.0** (orthogonal). Ce phénomène s'explique par :
1.  **Le partage de la syntaxe** : Les deux phrases partagent la même langue (le français), la même grammaire (Sujet + Verbe + Complément) et des mots outils identiques ("le", "la", "sur", "l'").
2.  **L'anisotropie des espaces vectoriels** : Les vecteurs générés par les Transformers ont tendance à occuper un cône étroit dans l'espace multidimensionnel plutôt que d'être répartis uniformément dans toutes les directions.

---

## 🧪 Travaux Pratiques Réalisés
Nous avons implémenté le script [test_embeddings.py](../../week-03-semantic-search/test_embeddings.py) en utilisant `sentence-transformers` et `numpy` :

*   **Calcul manuel** via NumPy :
    ```python
    def manual_cosine_similarity(v1, v2):
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        return dot_product / (norm_v1 * norm_v2)
    ```
*   **Résultats de similarité obtenus** :
    *   **Proches** (*Chat* dort / *Félin* fait sa sieste) : **0.5444**
    *   **Unrelated** (*Chat* dort / *Voiture* roule) : **0.4532** (baseline)
    *   **Proches** (*Programmation* Python / *Coder* en Python) : **0.7236**

---

## Flashcards (Anki / Active Recall)

#flashcard
Q: Qu'est-ce qu'un embedding en IA ?
A: C'est la conversion d'un token ou d'un texte en un vecteur dense (liste de nombres réels) à haute dimension qui capture le sens sémantique de l'information.

#flashcard
Q: Pourquoi utilise-t-on la similarité cosinus plutôt que la distance Euclidienne pour comparer des textes ?
A: Car la similarité cosinus mesure l'angle (la direction) entre deux vecteurs plutôt que leur longueur. Cela permet de comparer des textes de longueurs différentes sans biais.

#flashcard
Q: Pourquoi les bases de données SQL traditionnelles (B-Trees) sont-elles inadaptées pour la recherche vectorielle ?
A: Les index traditionnels (B-Trees) sont conçus pour trier et chercher des données sur une seule dimension (ex. nombres, chaînes exactes) et ne peuvent pas gérer des recherches de proximité dans des espaces à plusieurs centaines de dimensions.

#flashcard
Q: Qu'est-ce que l'anisotropie dans le contexte des embeddings de phrases ?
A: C'est le fait que les vecteurs d'embeddings générés ont tendance à se regrouper dans un cône étroit de l'espace vectoriel au lieu de se répartir partout, ce qui explique pourquoi des phrases différentes partagent une similarité de base positive (ex: ~0.45).
