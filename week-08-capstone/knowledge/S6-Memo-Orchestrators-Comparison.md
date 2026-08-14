# 📝 Mémo S6 : Comparatif des Frameworks (LangChain, LangGraph, CrewAI)

Ce mémo synthétise les différences fondamentales de philosophie, de contrôle et d'architecture entre les principaux orchestrateurs du marché.

---

## 1. LangChain vs CrewAI : Niveau d'Abstraction

La distinction majeure réside dans le but et le niveau d'abstraction de chaque outil :

*   **LangChain (Boîte à outils de bas niveau)** :
    *   **Philosophie** : Fournit des blocs de construction élémentaires (wrappers de LLM, chargeurs de documents, templates de prompts, vector stores). C'est le "jeu de Lego" de l'ingénieur IA.
    *   **Développement** : Demande beaucoup de code pour connecter les éléments, parser les sorties et gérer l'historique de conversation.
*   **CrewAI (Framework d'orchestration par rôles de haut niveau)** :
    *   **Philosophie** : Construit sur le paradigme du jeu de rôle. On ne gère pas les prompts de bas niveau ; on définit des **Agents** (avec Rôle, Objectif et Backstory) et des **Tâches** (avec description et sortie attendue).
    *   **Développement** : CrewAI orchestre automatiquement les interactions et les appels d'outils en arrière-plan.

*Note : Sous le capot, CrewAI utilise les structures et wrappers de LangChain pour gérer les modèles et les outils.*

---

## 2. LangGraph vs CrewAI : État de la Machine vs Autonomie de l'Équipe

Lorsqu'on compare spécifiquement l'outil d'agents de LangChain (**LangGraph**) à **CrewAI**, on oppose deux visions de l'orchestration :

### LangGraph (Machine à États Déterministe)
*   **Contrôle** : **Très élevé (Code-First)**. On définit explicitement un graphe orienté composé de Nœuds (fonctions Python) et d'Arêtes (edges). Les transitions et boucles de décision sont codées de manière stricte en Python.
*   **Mémoire** : L'état (State) est partagé et mis à jour de manière explicite. Les checkpointers sauvegardent l'état après chaque nœud, permettant de mettre facilement en place des validations humaines (*Human-in-the-loop*).
*   **Modèles locaux** : Idéal pour les petits LLMs locaux (Ollama) car le code Python force le cadre et évite les égarements.

### CrewAI (Équipe Séquentielle/Hiérarchique)
*   **Contrôle** : **Faible à Moyen (Prompt-First)**. On décrit la mission et les agents s'auto-organisent. Si on utilise un processus hiérarchique, un LLM "Manager" décide lui-même à qui attribuer les tâches.
*   **Mémoire** : L'état et l'historique sont gérés de manière implicite. La sortie d'une tâche est directement injectée dans le contexte de la tâche suivante.
*   **Modèles locaux** : Plus difficile à stabiliser sur de petits modèles car la collaboration dépend de la capacité du LLM à suivre de longues instructions de jeu de rôle.

---

## Flashcards (Anki / Active Recall)

#flashcard
Q: En quoi l'approche de LangChain se distingue-t-elle de celle de CrewAI ?
A: LangChain fournit des blocs de construction de bas niveau (Legos) pour tout type d'application LLM. CrewAI est un framework de haut niveau spécialisé dans le jeu de rôle et la collaboration multi-agents.

#flashcard
Q: Quelle est la différence de contrôle du flux entre LangGraph et CrewAI ?
A: LangGraph utilise un graphe déterministe codé en Python (contrôle total sur les transitions). CrewAI laisse les agents s'organiser et collaborer de manière autonome guidés par les descriptions de tâches et rôles.

#flashcard
Q: Pourquoi LangGraph est-il plus adapté pour les LLM locaux que CrewAI ?
A: Parce que LangGraph contraint l'agent dans un graphe d'exécution strict en Python, évitant que le petit modèle local ne s'égare dans des dialogues ou boucles de rôles infinies.
