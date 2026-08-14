# 📊 Mémo : Observabilité LLMOps & Langfuse (Semaine 7 - J1)

Ce mémo résume les concepts clés liés à l'observabilité des LLMs et l'intégration de Langfuse pour monitorer nos agents en production.

## 🎯 Concepts Clés

Qu'est-ce que l'observabilité LLMOps ? #flashcard
L'observabilité LLMOps est la capacité de surveiller, mesurer et comprendre le comportement interne d'un système basé sur des LLMs en production. Elle permet de suivre la latence, les coûts, l'utilisation des tokens, et de déboguer les chaînes d'exécution complexes (comme les agents).

Quelles sont les métriques principales surveillées dans un pipeline LLMOps ? #flashcard
1. **Latence** (Time To First Token - TTFT, temps total)
2. **Coûts** (Calculés selon le nombre de tokens in/out et le modèle)
3. **Volume de tokens** (Prompt tokens, Completion tokens)
4. **Qualité/Feedback** (Scores de satisfaction, taux d'erreur, hallucinations)

Qu'est-ce qu'une "Trace" dans le contexte de l'observabilité ? #flashcard
Une Trace représente l'exécution complète d'une requête utilisateur de bout en bout. Elle est composée de plusieurs "Spans" (étapes) qui détaillent chaque action spécifique (ex: recherche RAG, appel LLM, exécution d'un outil) au sein de la requête globale.

## 🛠️ Langfuse & Implémentation

Qu'est-ce que Langfuse ? #flashcard
Langfuse est une plateforme d'observabilité open-source dédiée aux applications LLMs. Elle permet de collecter des traces d'exécution, d'analyser les coûts, de gérer les prompts et de collecter des retours utilisateurs, intégrable facilement via SDK.

Comment instrumenter un agent LangGraph/LangChain avec Langfuse en Python ? #flashcard
Il faut importer le `CallbackHandler` natif de Langfuse et le passer dans la configuration de l'exécution :
```python
from langfuse.langchain import CallbackHandler

langfuse_handler = CallbackHandler()
config = {"callbacks": [langfuse_handler]}

# Exécution avec transmission du callback
graph.stream(initial_state, config=config)
```

Pourquoi est-il crucial d'utiliser l'observabilité pour des agents autonomes (ex: LangGraph / CrewAI) ? #flashcard
Les agents autonomes prennent des décisions en boucle (boucles `while`, auto-critique, appels d'outils successifs). Sans observabilité, il est impossible de savoir s'ils tournent en boucle infinie (over-generation), s'ils hallucinent sur les résultats d'un outil, ou combien d'appels LLM réels ont été facturés pour une seule tâche.
