# 📝 Mémo S5-J3 : Transformations de Requêtes & RAG-Fusion

*Ce document valide les tâches `S5-J3-T1` à `S5-J3-T4`.*

---

## 1. HyDE (Hypothetical Document Embeddings)

HyDE résout le problème de l'asymétrie de style entre les questions courtes des utilisateurs et les longs passages informatifs de notre base de connaissances.

### Mécanisme :
1.  **Génération fictive** : Le LLM reçoit la question originale et génère une réponse fictive (appelée document hypothétique). Même si les faits y sont faux (hallucinations), la structure de phrase et le vocabulaire correspondent au ton de l'encyclopédie ou de la documentation technique cherchée.
2.  **Vectorisation & Recherche** : Ce document hypothétique est converti en embedding puis comparé avec la base vectorielle.
3.  **Résultat** : On trouve de meilleurs candidats qu'en cherchant directement avec la question d'origine, car on compare un document déclaratif avec des documents déclaratifs.

---

## 2. Multi-Query & RAG-Fusion

### Le problème adressé :
Les utilisateurs formulent leurs questions de manière subjective. Un mot-clé manquant ou un synonyme non détecté par la recherche vectorielle peut exclure un document crucial de notre retrieval.

### Notre Pipeline RAG-Fusion ([query_transform.py](../../week-05-rag-advanced/query_transform.py)) :
1.  **Multi-Query** : Nous utilisons Ollama `llama3.1` pour générer **3 variations sémantiques** de la requête de base.
2.  **Recherches Parallèles** : Nous lançons une recherche hybride (BM25 + Chroma Dense) pour chacune des 4 requêtes (l'originale + les 3 variantes).
3.  **RAG-Fusion (RRF Multi-Requête)** : Nous combinons l'ensemble des documents récupérés (qui peuvent se chevaucher). Le score RRF de chaque document est calculé en faisant la somme de son inverse de rang $\frac{1}{60 + \text{Rank}}$ dans chaque liste de recherche.
4.  **Reranking local** : Nous réordonnons le top-20 global issu de RAG-Fusion avec le Cross-Encoder `BAAI/bge-reranker-v2-m3` pour en extraire le top-5 final ultra-ciblé.
5.  **Génération d'Ancrage** : Rédaction de la réponse finale basée sur le top-5 par Ollama.

---

## 3. La Décomposition de Requêtes (Sub-Queries)

Pour les questions complexes ou composites (contenant plusieurs questions en une seule), la recherche globale est inefficace car elle mélange les requêtes.
*   **Solution** : Découper la question composite en sous-questions simples.
*   **Exemple** : *"Compare Raft et Paxos et explique leur latence"* devient :
    1. *"Comment fonctionne le consensus dans Paxos ?"*
    2. *"Comment fonctionne le consensus dans Raft ?"*
    3. *"Quelle est la latence de Paxos et Raft ?"*
*   Chaque sous-requête effectue sa propre recherche et les contextes fusionnés sont fournis au LLM pour la synthèse finale.

---

## Flashcards (Anki / Active Recall)

#flashcard
Q: Quel problème sémantique la méthode HyDE tente-t-elle de résoudre ?
A: L'asymétrie de ton et de style entre les questions courtes/interrogatives des utilisateurs et les longs textes déclaratifs stockés en base, en cherchant à l'aide d'une réponse déclarative fictive générée par le LLM.

#flashcard
Q: Quel est l'inconvénient principal de la méthode HyDE ?
A: La latence (il faut attendre un premier appel LLM pour générer le document fictif avant de lancer la recherche) et le risque de dérive sémantique si le document hypothétique est trop éloigné du sujet réel.

#flashcard
Q: En quoi consiste la technique de Multi-Query dans un système RAG ?
A: Elle consiste à utiliser un LLM pour générer plusieurs formulations alternatives de la question de l'utilisateur afin de chercher la base documentaire sous plusieurs angles et d'éviter les manques de rappel (recall).

#flashcard
Q: Comment RAG-Fusion consolide-t-il les résultats des multiples requêtes générées par le Multi-Query ?
A: Il rassemble les documents de toutes les recherches alternatives et applique l'algorithme RRF (Reciprocal Rank Fusion) pour agréger leurs classements respectifs et former un top-k final dédoublé et ordonné.
