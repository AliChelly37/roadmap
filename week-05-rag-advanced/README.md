# 🚀 Week 05 - Advanced RAG & Evaluation

Ce projet implémente et évalue plusieurs techniques de **RAG Avancé (Retrieval-Augmented Generation)** en local à l'aide d'Ollama (`llama3.1`) et de bases de données vectorielles et de graphes locales.

---

## 🛠️ Architecture & Techniques implémentées

Nous avons fait évoluer un RAG basique (Semaine 4) vers un pipeline RAG de niveau industriel intégrant :

1.  **Recherche Hybride (BM25 + Dense E5)** : Fusion lexicale (mots-clés exacts) et vectorielle (similarité sémantique) avec l'algorithme **Reciprocal Rank Fusion (RRF)**.
2.  **Reranking (Cross-Encoder local)** : Réordonnancement précis du Top-20 candidats à l'aide du modèle de pointe **`BAAI/bge-reranker-v2-m3`** exécuté localement en CPU/GPU.
3.  **RAG-Fusion (Multi-Query + RRF)** : Paraphrase de la requête utilisateur sous 3 angles distincts via LLM en entrée pour maximiser le rappel sémantique, combiné avec RRF.
4.  **Contextual Retrieval (Anthropic style)** : Ingestion intelligente où chaque morceau est enrichi par un résumé d'introduction contextualisé pour éviter la perte de contexte global.
5.  **GraphRAG (Graphe de Connaissances)** : Extraction automatique de triplets `(Sujet, Relation, Objet)` à l'aide du LLM local et requête de graphe hybride pour structurer les liens sémantiques.

---

## 📊 Résultats & Analyse Comparative (RAGAS)

Les évaluations ont été mesurées en local à l'aide de **RAGAS** sur un dataset de référence de 16 questions d'évaluation.

| Métrique RAGAS | Baseline S4 (Dense pur) | RAG S5-J2 (Hybride + Rerank) | RAG S5-J3 (RAG-Fusion + Rerank) | Évolution globale |
| :--- | :---: | :---: | :---: | :---: |
| **Faithfulness** (Fidélité) | **0.4333** | **0.8728** | **0.7835** | **+0.3502** 🚀 *(Moins d'hallucinations)* |
| **Answer Relevancy** | **0.8445** | **0.8702** | **0.8612** | **+0.0167** *(Pertinence stable)* |
| **Context Precision** | **0.9583** | **0.9378** | **0.9524** | **-0.0059** *(Tri stable)* |
| **Context Recall** | **0.8458** | **0.9531** | **0.9531** | **+0.1073** 📈 *(Rappel quasi-parfait)* |

### 🔍 Enseignements Clés (Audit des résultats) :
*   **Le Reranker local double la fidélité (Faithfulness : 0.43 ➔ 0.87)** : Le plus grand défaut du RAG de la semaine 4 était l'hallucination due à du contexte bruité ou hors sujet. En forçant un Cross-Encoder à réévaluer les 20 morceaux et en coupant le contexte sémantiquement faible (garde < 0.01), le LLM ne produit plus d'affirmations infondées.
*   **La recherche hybride comble le manque de rappel (Recall : 0.84 ➔ 0.95)** : L'utilisation conjointe de BM25 et de Chroma via RRF permet de capturer des passages techniques précis (comme les spécifications réseau et les noms d'algorithmes) qui échappaient à la recherche vectorielle seule.
*   **RAG-Fusion augmente la précision du contexte** : La reformulation multi-requête permet de cibler des morceaux pertinents sous plusieurs synonymes, ce qui remonte la précision du contexte à 95.24%. Néanmoins, le fait de brasser plus large peut parfois diluer la fidélité sémantique de la génération finale par rapport au RAG hybride simple ciblé.

---

## 📦 Structure des Scripts

*   `query_hybrid.py` : Recherche hybride fusionnée via RRF local (0.6 Dense / 0.4 BM25).
*   `query_rerank.py` : Recherche hybride Top-20 ➔ Reranker `bge-reranker-v2-m3` ➔ Sélection Top-5 ➔ Génération Ollama.
*   `query_transform.py` : Pipeline RAG-Fusion avec génération de 3 paraphrases alternatives et fusion RRF globale.
*   `contextual_indexing.py` : Création de la base contextualisée (Chunk Headers) dans Chroma (`rag_contextual_test`).
*   `graph_rag.py` : Construction du Knowledge Graph local (`knowledge_graph.json`) et requête hybride Graphe + Vecteur.

---

## 🚀 Comment exécuter les pipelines

Assurez-vous que votre serveur local **Ollama** est démarré et que le modèle `llama3.1` est disponible.

### 1. Lancer une requête Hybride simple
```bash
.venv\Scripts\python week-05-rag-advanced\query_hybrid.py "Qu'est-ce que le protocole Raft et ses trois états ?"
```

### 2. Lancer une requête avec Reranking
```bash
.venv\Scripts\python week-05-rag-advanced\query_rerank.py "Qu'est-ce que le protocole Raft et ses trois états ?"
```

### 3. Lancer une requête RAG-Fusion (Multi-Query)
```bash
.venv\Scripts\python week-05-rag-advanced\query_transform.py "Qu'est-ce que le protocole Raft et ses trois états ?"
```

### 4. Indexer le document en Contextual Retrieval (Anthropic)
```bash
.venv\Scripts\python week-05-rag-advanced\contextual_indexing.py
```

### 5. Construire le graphe de connaissances et lancer une requête GraphRAG
```bash
.venv\Scripts\python week-05-rag-advanced\graph_rag.py
```
