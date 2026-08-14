# 📝 Mémo S6-J4 : Systèmes Multi-Agents (CrewAI vs LangGraph)

*Ce document valide les tâches `S6-J4-T1` à `S6-J4-T4`.*

---

## 1. Principes de Conception Multi-Agents

Dans un système multi-agents, une tâche complexe est résolue en faisant collaborer plusieurs agents autonomes spécialisés dotés de rôles précis, au lieu de tout confier à un seul prompt monolithique.

### Les 3 Piliers de l'Agent CrewAI :
1.  **Role (Le Rôle)** : Définit le titre professionnel de l'agent (ex: "Expert Document and Web Researcher").
2.  **Goal (L'Objectif)** : Décrit la mission spécifique que l'agent doit accomplir.
3.  **Backstory (L'Historique)** : Donne de la personnalité et du contexte à l'agent, ce qui oriente sa façon de raisonner et de rédiger.

### Orchestration : Séquentielle vs Superviseur
*   **Sequential (Séquentiel)** : Les tâches sont résolues les unes après les autres. La sortie de la tâche $N$ sert d'entrée à la tâche $N+1$.
*   **Supervisor (Superviseur)** : Un agent central "manager" distribue dynamiquement les sous-tâches à des agents spécialistes et rassemble leurs retours.

---

## 2. Comparaison : LangGraph vs CrewAI

| Dimension | LangGraph | CrewAI |
| :--- | :--- | :--- |
| **Philosophie** | Machine à états déterministe (graphe) | Équipe par rôles autonome (crew) |
| **Contrôle** | **Très élevé** (on programme chaque transition) | **Faible** (les agents s'auto-organisent via prompts) |
| **Simplicité** | Plus complexe (il faut concevoir l'état et les arêtes) | Très simple (on définit les rôles et tâches) |
| **Cas d'usage** | Processus métiers stricts avec garde-fous | Tâches créatives, brainstormings, rapports généraux |

---

## 3. Risques et Garde-fous Observés en Production

La mise en place de systèmes multi-agents comporte des risques spécifiques que nous avons directement identifiés lors des tests :

1.  **Conflits de types (Pydantic / LangChain)** : Les frameworks évoluent à des vitesses différentes. CrewAI valide strictement les signatures d'outils avec Pydantic v2. Les objets d'outils bruts de LangChain provoquent des erreurs de validation s'ils ne sont pas enveloppés par le décorateur natif de CrewAI (`from crewai.tools import tool`).
2.  **Boucles infinies et Latence** : Si deux agents se renvoient constamment une tâche (ex. rédacteur ➔ critique ➔ rédacteur), le système peut tourner à l'infini. Il est impératif d'intégrer une limite stricte d'itérations (max 4 ou 5) ou un budget de tokens maximum.
3.  **Bruit et dérive sémantique** : Au fur et à mesure que les messages s'accumulent, les agents peuvent perdre le fil de l'instruction utilisateur initiale (drift). Il faut purger la mémoire ou recentrer systématiquement les tâches sur le sujet (`topic`).

---

## Flashcards (Anki / Active Recall)

#flashcard
Q: Quelles sont les trois caractéristiques obligatoires pour définir un agent dans CrewAI ?
A: Le Rôle (Role), l'Objectif (Goal) et l'Historique (Backstory).

#flashcard
Q: Quand faut-il privilégier LangGraph par rapport à CrewAI ?
A: Quand le processus exige un contrôle strict et déterministe sur les transitions de tâches et les actions de l'agent. CrewAI est préférable pour des tâches exploratoires ou rédactionnelles plus libres.

#flashcard
Q: Quel risque technique majeur pose la boucle d'auto-critique entre agents et comment le résoudre ?
A: Le risque de boucle infinie (ou de dérive de contexte). On le résout en fixant un compteur maximum strict d'itérations (max 4-5) ou en implémentant un garde-fou budgétaire dans le graphe/la crew.
