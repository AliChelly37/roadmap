# 📝 Mémo S6-J1 : Fondations des Agents IA & Conception

*Ce document valide les tâches `S6-J1-T1` à `S6-J1-T4`.*

---

## 1. Workflows vs Agents (Anthropic)

Dans la conception d'applications basées sur les LLMs, on distingue deux grandes architectures d'orchestration :

### Workflows (Orchestration Statique)
Les étapes de traitement et les transitions sont figées dans le code (DAG statique). Le LLM résout des tâches isolées mais n'a pas la liberté de décider du chemin à suivre.
*   **Prompt Chaining** : Suite séquentielle de prompts où la sortie de l'un nourrit le suivant.
*   **Routing** : Le LLM classifie l'entrée utilisateur pour la diriger vers la branche spécialisée appropriée.
*   **Parallelization** : Exécution de multiples LLMs en parallèle pour synthétiser ensuite les résultats.
*   **Orchestrator-Workers** : Un LLM central décompose une tâche, la distribue à plusieurs "travailleurs" puis rassemble les résultats.
*   **Evaluator-Optimizer** : Un LLM produit un essai, un autre le critique et fournit des retours pour guider le premier dans une boucle d'amélioration.

### Agents (Autonomie Dynamique)
Le LLM est placé dans une boucle active où il contrôle lui-même le flux de contrôle sémantique en fonction des circonstances.
*   **Boucle ReAct (Reasoning + Acting)** : L'agent alterne entre réflexion (`Thought`), action (`Action` - ex: appel d'outils) et observation (`Observation` - traitement du retour de l'outil).
*   **Cas d'usage** : Idéal pour les tâches exploratoires, ouvertes et multivariées (ex: recherche documentaire complexe, débogage interactif).

---

## 2. Anatomie d'un Agent (Hugging Face)

Un agent complet se compose de quatre piliers fondamentaux :
1.  **LLM (Le Cerveau)** : Reçoit les requêtes et pilote la logique de prise de décision.
2.  **System Prompt (Les Consignes)** : Définit l'identité du robot, les outils mis à sa disposition et les consignes de formatage de la pensée (ex. boucle ReAct).
3.  **Outils (Les Mains)** : Fonctions exécutables par le système informatique dont la signature et la description sont partagées avec le LLM.
4.  **Mémoire (Le Contexte)** : Historique de la session (court terme) et base de connaissances acquise (long terme).

---

## 3. Spécifications de notre Agent Cible

Nous choisissons de relever un double défi : implémenter l'**Option A** (Agent ReAct autonome avec LangGraph) ET l'**Option B** (Système multi-agents avec CrewAI).

### Fiche Technique de l'Agent Cible (Rédacteur de Rapports Analytiques) :
*   **Tâche principale** : Rédiger un rapport analytique approfondi et structuré sur un sujet complexe fourni par l'utilisateur.
*   **Fonctionnement itératif** : L'agent ne génère pas de réponse directe. Il applique le pattern *Recherche ➔ Rédaction ➔ Auto-Critique ➔ Correction/Recherche ciblée ➔ Synthèse finale*.
*   **Arsenal d'outils** :
    1.  `web_search` : Recherche de liens pertinents via Tavily / DuckDuckGo.
    2.  `scrape_url` : Extraction du texte brut d'une page Web spécifique pour analyse profonde.
    3.  `search_my_docs` : Interrogation de notre base vectorielle locale RAG (Semaine 5).
    4.  `save_markdown` : Enregistrement ou mise à jour locale du rapport (`rapport_final.md`).
*   **Critères d'arrêt de la boucle** :
    *   *Succès* : Le module d'auto-critique juge le brouillon actuel complet et validé.
    *   *Sécurité* : Limite stricte de 4 ou 5 cycles. En cas de dépassement, l'agent sauvegarde la meilleure version disponible et ajoute une section *"Pistes non explorées"*.

---

## Flashcards (Anki / Active Recall)

#flashcard
Q: Quelle est la différence majeure entre un "Workflow" et un "Agent" selon Anthropic ?
A: Un workflow suit un chemin statique et déterministe préprogrammé (DAG). Un agent a l'autonomie de décider dynamiquement de ses actions et transitions dans une boucle active en fonction du contexte.

#flashcard
Q: Pourquoi Anthropic recommande-t-il de privilégier les workflows simples aux agents autonomes ?
A: Parce que les workflows sont prévisibles, faciles à tester, moins chers et ont une latence plus faible. L'autonomie agentique ne doit être ajoutée que si la tâche est imprévisible.

#flashcard
Q: Quels sont les 4 composants de base d'un agent autonome ?
A: Le LLM (cerveau), le System Prompt (règles et boucle ReAct), les Outils (fonctions Python descriptives) et la Mémoire (court et long terme).

#flashcard
Q: Quels sont les deux critères d'arrêt de notre agent de rédaction de rapports ?
A: 1) Le critère qualitatif de l'auto-critique qui valide le rapport. 2) La limite de sécurité matérielle (max 4 à 5 itérations) avec génération de "pistes non explorées".
