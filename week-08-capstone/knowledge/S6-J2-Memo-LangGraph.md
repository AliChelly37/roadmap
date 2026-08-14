# 📝 Mémo S6-J2 : Architecture de LangGraph & Boucle de Tool-Calling

*Ce document valide les tâches `S6-J2-T1` à `S6-J2-T3`.*

---

## 1. La Philosophie de LangGraph

LangGraph est une extension de LangChain conçue pour modéliser des flux de travail cycliques (State Machines), indispensables pour les agents conversationnels et les boucles **ReAct** (Raisonner + Agir). Contrairement aux chains classiques (DAGs linéaires), LangGraph permet de définir des relations bidirectionnelles et des boucles répétitives entre nœuds.

---

## 2. Les Composants Clés d'un Graphe LangGraph

Un graphe LangGraph s'appuie sur quatre primitives majeures :

### L'État (State)
L'État est la source unique de vérité partagée entre tous les nœuds du graphe.
*   **Implémentation** : Souvent défini sous forme de dictionnaire typé (`TypedDict` en Python) ou d'objet Pydantic.
*   **Reducteurs (Reducers)** : Définissent comment les valeurs renvoyées par un nœud fusionnent avec la valeur existante de l'état. L'annotation `Annotated[list, add_messages]` est le réducteur standard qui concatène automatiquement les nouveaux messages à l'historique sans effacer les précédents.

### Les Nœuds (Nodes)
Ce sont des fonctions Python pures ou des runnables.
*   **Fonctionnement** : Un nœud reçoit l'état courant en paramètre, effectue des calculs (ex. appeler un LLM ou lancer un script), puis retourne les clés de l'état qu'il souhaite modifier ou mettre à jour.

### Les Arêtes (Edges)
Définissent le sens de circulation dans le graphe.
*   **Arêtes simples** : Lien déterministe reliant un nœud à un autre (ex. `builder.add_edge(START, "agent")`).
*   **Arêtes conditionnelles (Conditional Edges)** : Utilisent une fonction de décision (router) pour orienter le flux en fonction de l'état (ex. rediriger vers le nœud d'outils si l'agent a généré un appel d'outil, ou s'arrêter).

### La Compilation (Compilation)
L'étape de compilation valide la structure sémantique du graphe (pas d'arêtes vers des nœuds non enregistrés, présence d'un point d'entrée, etc.) et retourne un objet `CompiledGraph` exécutable via `.invoke()` ou `.stream()`.

---

## 3. Implémentation du pattern ReAct Standard

Dans notre script `simple_agent.py`, nous avons assemblé un agent ReAct standard en utilisant les composants préconstruits de LangGraph :

```python
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition

builder = StateGraph(State)

# 1. Enregistrement des nœuds
builder.add_node("agent", call_model) # Nœud LLM
builder.add_node("tools", tool_node)  # Nœud d'exécution des outils

# 2. Enregistrement des arêtes
builder.add_edge(START, "agent")

# Aiguillage automatique : tools_condition redirige vers "tools" si l'agent veut
# appeler un outil, ou vers END si l'agent a formulé sa réponse finale
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent") # boucle de retour

graph = builder.compile()
```

---

## Flashcards (Anki / Active Recall)

#flashcard
Q: À quoi sert un réducteur (reducer) dans la définition du State de LangGraph ?
A: Il définit les règles de fusion des données quand un nœud retourne une mise à jour (ex. `add_messages` concatène les nouveaux messages à l'historique existant au lieu de l'écraser).

#flashcard
Q: Quelle est la différence entre une arête classique (edge) et une arête conditionnelle (conditional edge) ?
A: Une arête classique relie deux nœuds de manière fixe et déterministe. Une arête conditionnelle utilise une fonction de routage pour décider dynamiquement du prochain nœud à exécuter en fonction des données actuelles du State.

#flashcard
Q: À quoi sert l'utilitaire `tools_condition` pré-compilé de LangGraph ?
A: Il sert d'arête conditionnelle standard : il inspecte le dernier message de l'état. S'il contient des `tool_calls`, il redirige vers le nœud d'outils, sinon il termine le graphe en allant vers `__end__`.
