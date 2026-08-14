# 📝 Mémo S5-J1 : Recherche Hybride & Évaluation RAGAS

*Ce document valide les tâches `S5-J1-T1` à `S5-J1-T4`.*

---

## 1. Diagnostic de la Baseline (RAG Semaine 4)
Nous avons mesuré les performances du RAG de la semaine 4 (ChromaDB + Gemini 3.5 Flash) sur notre jeu de test de 16 questions en utilisant **RAGAS** (sur base Ollama `llama3.1` local).

### Les scores obtenus :
| Métrique RAGAS | Score Baseline S4 | Signification & Diagnostic |
| :--- | :---: | :--- |
| **Faithfulness** (Fidélité) | **0.4333** ⚠️ | **Très bas.** Le modèle hallucine ou génère des faits non présents dans les morceaux récupérés. Cela s'explique par un contexte incomplet ou bruité. |
| **Answer Relevancy** | **0.8445** | **Bon.** Les réponses sont sémantiquement bien ciblées par rapport à la question posée. |
| **Context Precision** | **0.9583** | **Excellent.** L'algorithme dense ordonne très bien les morceaux pertinents en tête de liste. |
| **Context Recall** | **0.8458** | **Moyen.** Environ 15% des informations clés nécessaires pour formuler la réponse idéale n'ont pas été capturées par le retriever vectoriel standard. |

---

## 2. La Recherche Lexicale : BM25 (Best Matching 25)
Pour combler le manque de rappel (recall) et de précision sémantique sur certains termes techniques, nous avons introduit **BM25**, l'algorithme de recherche lexicale standard.

### Les 3 Piliers de la Formule BM25 :
1.  **Fréquence des termes (TF)** : Plus le mot cherché apparaît dans le document, plus le score monte. BM25 apporte une **saturation** (paramètre $k_1$ entre $1.2$ et $2.0$) : après quelques apparitions, le score stagne pour éviter le spam de mots-clés.
2.  **Fréquence Inverse de Document (IDF)** : Les mots rares (ex: `Raft`, `Paxos`) pèsent la majorité du score sémantique, tandis que les mots fréquents (ex: `le`, `et`) ont un poids presque nul.
3.  **Normalisation de la longueur** : Pénalise les documents trop longs (paramètre $b = 0.75$). Un mot-clé trouvé dans un court paragraphe a plus de valeur que le même mot-clé trouvé perdu au milieu d'un livre complet.

---

## 3. RRF (Reciprocal Rank Fusion) : Fusionner Dense & Sparse
Plutôt que d'essayer de normaliser et d'additionner les scores de Chroma (distances cosinus) et de BM25 (scores arbitraires), nous utilisons **RRF**. Cet algorithme combine uniquement les **rangs (classements)** des documents.

### Formule RRF :
$$RRF\_Score(d) = \sum_{m \in M} \frac{W_m}{k + Rank_m(d)}$$
*   $M$ : Ensemble des retrievers (Dense et Sparse).
*   $Rank_m(d)$ : Position du document $d$ dans les résultats du retriever $m$ (1-indexed).
*   $k$ : Constante de lissage (généralement $60$) pour éviter que les rangs très bas n'écrasent le score.
*   $W_m$ : Poids attribué au retriever (ex: $0.6$ pour le vectoriel et $0.4$ pour le BM25).

---

## 4. Architecture de notre Implémentation Hybride
Nous avons écrit [query_hybrid.py](../../week-05-rag-advanced/query_hybrid.py) :
1.  **Chroma DB Ingestion** : Récupération de tous les documents textuels existants dans la collection Chroma de la Semaine 4.
2.  **BM25 Ingestion** : Création du `BM25Retriever` LangChain à partir de ces morceaux textuels (nettoyés de leur préfixe E5 `"passage: "`).
3.  **Dense Custom Wrapper** : Implémentation d'un `E5ChromaRetriever` qui ajoute automatiquement le préfixe requis `"query: "` sur la requête utilisateur pour Chroma.
4.  **RRF Fusion** : Fusion manuelle robuste de type $0.6 \text{ Dense} + 0.4 \text{ BM25}$ pour s'affranchir des contraintes d'import réseau de LangChain.
5.  **Local Generation** : Routage de la génération finale sur votre modèle local Ollama `llama3.1`.

---

## Flashcards (Anki / Active Recall)

#flashcard
Q: Quelles sont les 4 métriques clés évaluées par RAGAS ?
A: Faithfulness (Fidélité), Answer Relevancy (Pertinence), Context Precision (Précision du contexte), et Context Recall (Rappel du contexte).

#flashcard
Q: Qu'est-ce que la métrique de Faithfulness dans RAGAS et que signifie un score faible ?
A: Elle mesure si la réponse générée est factuellement soutenue par le contexte récupéré. Un score faible signifie que le modèle hallucine ou extrapole des faits absents de sa source.

#flashcard
Q: Quels sont les 3 principes mathématiques qui régissent l'algorithme lexicale BM25 ?
A: 1) Le Term Frequency (TF) avec saturation (l'impact de la répétition d'un mot sature). 2) L'Inverse Document Frequency (IDF) (les mots rares pèsent plus lourd). 3) La normalisation par la longueur (pénalise les longs documents).

#flashcard
Q: Comment fonctionne l'algorithme RRF (Reciprocal Rank Fusion) pour fusionner les retrievers Dense et Sparse ?
A: Il additionne les inverses des rangs de classement de chaque document dans les deux retrievers ($1 / (k + rank)$), propageant en tête de liste les documents qui apparaissent très haut dans l'un des retrievers ou moyennement dans les deux.
