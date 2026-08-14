# 📝 Mémo S5-J2 : Architecture Cross-Encoder & Reranking

*Ce document valide les tâches `S5-J2-T1` à `S5-J2-T4`.*

---

## 1. Bi-Encoders vs Cross-Encoders (Sentence-Transformers)

Pour la recherche de documents, deux architectures de réseaux de neurones s'affrontent :

### Bi-Encoders (ex: `multilingual-e5-base`)
*   **Mécanisme** : La question et les documents sont encodés **séparément** dans un espace vectoriel. La similarité est calculée via une simple mesure géométrique (ex: distance cosinus).
*   **Cas d'usage** : Idéal pour l'indexation de masse et le filtrage initial (Retrieval). On peut précalculer les embeddings des documents et les stocker dans ChromaDB.
*   **Limitation** : Il n'y a aucune interaction mot-à-mot directe entre la question et le document pendant l'encodage, ce qui peut laisser passer des faux positifs sémantiques ou ignorer de petits détails critiques (comme une négation).

### Cross-Encoders (ex: `bge-reranker-v2-m3`)
*   **Mécanisme** : La question et le document sont entrés **conjointement** dans le Transformer : `[CLS] Question [SEP] Document [SEP]`. Les couches d'attention analysent l'interaction complète entre chaque mot de la requête et chaque mot du texte.
*   **Cas d'usage** : Idéal pour réordonner un sous-ensemble restreint de documents candidats (Reranking).
*   **Limitation** : Extrêmement lourd et lent. Impossible de précalculer les scores. C'est pourquoi on ne l'utilise jamais en direct sur l'ensemble d'une base de données, mais uniquement sur le **top-20** ou **top-50** extrait par un Bi-Encoder.

---

## 2. Le Reranker Local : BAAI/bge-reranker-v2-m3
Nous avons intégré le modèle local de reranking de BAAI en utilisant la bibliothèque `sentence-transformers` dans le script [query_rerank.py](../../week-05-rag-advanced/query_rerank.py).

*   **Poids du modèle** : ~1.1 Go (téléchargé et mis en cache automatiquement).
*   **Intégration RAG** : 
    1. Récupération de **20 documents** via notre recherche hybride (RRF).
    2. Calcul du score de répertinence pour chaque couple `[Question, Document]` avec le reranker.
    3. Tri par score décroissant et conservation du **top-5** pour le prompt final.
    4. **Garde de Rerank** : Si le score du meilleur document est inférieur à `0.01`, le RAG refuse de répondre ("Je ne sais pas.") pour éviter les réponses basées sur des documents hors sujet.

---

## 3. Analyse Comparative des Performances (RAGAS)

Nous avons fait tourner [run_evaluation_rerank.py](../../week-05-rag-advanced/run_evaluation_rerank.py) sur nos 16 questions d'évaluation. Voici le comparatif :

| Métrique RAGAS | Baseline S4 (Dense standard) | RAG S5-J2 (Hybride RRF + Reranked) | Évolution |
| :--- | :---: | :---: | :---: |
| **Faithfulness** (Fidélité) | **0.4333** | **0.8728** | **+0.4395** 🚀 |
| **Answer Relevancy** | **0.8445** | **0.8702** | **+0.0257** |
| **Context Precision** | **0.9583** | **0.9378** | **-0.0205** |
| **Context Recall** | **0.8458** | **0.9531** | **+0.1073** 📈 |

### Reranker : Quand aide-t-il vs quand n'apporte-t-il rien ?
*   **Il aide énormément** : 
    *   **Fidélité (Faithfulness)** : En éliminant le "bruit" (les documents non pertinents mais proches vectoriellement) du contexte envoyé au LLM, on divise par deux le taux d'hallucinations.
    *   **Rappel (Context Recall)** : Grâce au retrieval hybride, on capture des documents que la recherche dense pure ratait. Le Reranker se charge ensuite de faire remonter ces pépites oubliées en tête du classement.
*   **Il n'apporte rien (ou ralentit)** : 
    *   **Temps de réponse (Latence)** : L'inférence locale d'un Cross-Encoder sur 20 candidats ajoute une surcharge de calcul (environ 1.5s à 3s sur CPU). Pour des cas d'usage simples de recherche par mot-clé où le premier résultat vectoriel est déjà excellent, le reranker n'améliore pas la réponse mais dégrade la latence.

---

## Flashcards (Anki / Active Recall)

#flashcard
Q: Pourquoi un Cross-Encoder est sémantiquement plus précis qu'un Bi-Encoder ?
A: Parce qu'il analyse simultanément la question et le document dans le Transformer, permettant aux mots de la question d'interagir directement avec les mots du document via le mécanisme d'attention croisée.

#flashcard
Q: Pourquoi n'utilise-t-on pas le Cross-Encoder directement pour chercher dans toute notre base de données ?
A: Car sa complexité de calcul est trop élevée ($O(N)$ passages dans le Transformer à chaque requête pour $N$ documents). Le Bi-Encoder est utilisé en premier car sa similarité vectorielle s'exécute en $O(1)$ à l'aide d'index précalculés.

#flashcard
Q: Quel est l'impact principal du Reranking sur le score de Faithfulness (Fidélité) ?
A: Il l'augmente drastiquement (de 43% à 87% dans nos tests) en filtrant les documents non pertinents (bruit) du contexte du prompt, évitant ainsi que le LLM n'extrapole des faits.

#flashcard
Q: Qu'est-ce que la "garde de rerank" sémantique et pourquoi l'utiliser ?
A: C'est un seuil de score minimal (ex: < 0.01) sous lequel les documents réordonnés sont considérés comme hors sujet. On l'utilise pour forcer le RAG à répondre "Je ne sais pas" quand aucun document n'est pertinent.
