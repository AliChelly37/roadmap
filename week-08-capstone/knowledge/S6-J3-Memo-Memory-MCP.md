# 📝 Mémo S6-J3 : Mémoire des Agents, Outils & MCP

*Ce document valide les tâches `S6-J3-T1` à `S6-J3-T4`.*

---

## 1. La Mémoire des Agents

Pour mener des tâches à bien sur la durée, un agent a besoin de se souvenir de ses actions passées et du contexte utilisateur. On distingue deux types de mémoire :

### Mémoire à court terme (Short-Term Memory / Conversational State)
*   **Concept** : Permet à l'agent de conserver le contexte au cours d'une même session utilisateur (historique de chat, variables d'état du graphe).
*   **En LangGraph** : Gérée via les **Checkpointers** (ex: `MemorySaver` en mémoire ou `SqliteSaver` persistant sur disque). Le graphe sauvegarde automatiquement son état courant après le passage de chaque nœud à l'aide d'un `thread_id` unique.

### Mémoire à long terme (Long-Term Memory)
*   **Concept** : Permet à l'agent d'apprendre d'une session à l'autre (se rappeler des préférences utilisateur, des erreurs passées).
*   **Techniques** : Stockage de profils utilisateur dans des bases vectorielles ou utilisation de frameworks spécialisés comme `mem0`.

---

## 2. Model Context Protocol (MCP)

Le **Model Context Protocol (MCP)** est un protocole open-source conçu par Anthropic pour standardiser la manière dont les LLMs accèdent à des outils et des sources de données.

### Architecture Client-Serveur
*   **MCP Client** : L'application IA (Cursor, Claude Desktop, ou un agent autonome).
*   **MCP Server** : Des services indépendants ultra-légers qui exposent des données ou des actions via trois primitives :
    1.  **Resources** : Données en lecture seule (fichiers locaux, tables de base de données).
    2.  **Prompts** : Modèles de prompts réutilisables.
    3.  **Tools** : Fonctions exécutables par le client avec validation stricte (ex. exécuter du code, faire une recherche).
*   **Intérêt** : Évite d'écrire du code d'intégration sur mesure pour chaque outil. Un serveur MCP développé une fois peut être immédiatement branché sur n'importe quel client compatible.

---

## 3. Détails de notre Implémentation Pratique

Nous avons développé un agent itératif (`ReportAgent`) combinant recherche sémantique locale et recherche web :
*   **Recherche Web** : Implémentée avec DuckDuckGo (`DuckDuckGoSearchRun`). Elle est 100% gratuite et ne nécessite pas de clé d'API.
*   **Lecture Profonde (Scraping)** : Développée via une fonction personnalisée avec `BeautifulSoup` et `requests`, configurée pour nettoyer le HTML (retrait des scripts/styles) et tronquer le texte à 3500 caractères pour respecter la fenêtre de contexte.
*   **Interconnexion RAG (Semaine 5)** : Le script charge directement notre base Chroma locale (`rag_document_test`) et utilise le modèle d'embeddings `intfloat/multilingual-e5-base` pour effectuer une recherche documentaire sémantique.
*   **Contrôle de Boucle** : Le compteur d'itérations (`state["iteration"]`) agit comme garde-fou strict. Si la limite de 4 est atteinte, le nœud de sauvegarde finale est forcé et le rapport est clôturé avec la mention des pistes non explorées.

---

## Flashcards (Anki / Active Recall)

#flashcard
Q: Qu'est-ce qu'un "Checkpointer" dans LangGraph et quel type de mémoire gère-t-il ?
A: C'est un mécanisme qui sauvegarde l'état du graphe après l'exécution de chaque nœud. Il gère la mémoire à court terme (conversational state) pour permettre des interactions multi-tours cohérentes.

#flashcard
Q: Quelles sont les trois primitives de base exposées par un serveur MCP (Model Context Protocol) ?
A: Les Resources (données en lecture seule), les Prompts (modèles de prompts préconfigurés) et les Tools (fonctions exécutables avec validation).

#flashcard
Q: Pourquoi est-il important de tronquer la sortie d'un outil de scraping comme `scrape_url` ?
A: Pour éviter de saturer la fenêtre de contexte du LLM (context window) avec des milliers de lignes de texte HTML ou de publicités inutiles, ce qui augmenterait la latence et les coûts.
