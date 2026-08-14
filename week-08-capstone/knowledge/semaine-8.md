# Mémos - Semaine 8 (Capstone & Déploiement)

Qu'est-ce qu'une architecture "End-to-End" pour une application LLM ? #flashcard
C'est un flux complet qui part de l'interface utilisateur (UI), passe par une API backend (ex: FastAPI), orchestre la logique via un Agent (avec des outils comme le RAG ou la recherche web), route la requête vers le LLM (ex: LiteLLM), tout en incluant l'observabilité (tracing) et les garde-fous (sécurité) en production.

Pourquoi est-il important de séparer l'agent des outils (comme le RAG) dans l'architecture ? #flashcard
Cela permet de garder un couplage faible. L'agent (ex: LangGraph) se concentre sur le raisonnement (ReAct) et décide quand appeler l'outil. Le RAG est simplement une fonction (outil) que l'agent peut invoquer avec des paramètres. Cela facilite les tests isolés (on peut tester le RAG sans l'agent et inversement).

À quoi sert un fichier `.dockerignore` lors de la construction d'une image Docker ? #flashcard
Il sert à indiquer à Docker quels fichiers ou dossiers locaux (ex: `.venv`, `__pycache__`, `.env`, bases de données locales) NE DOIVENT PAS être copiés dans l'image. Cela réduit la taille de l'image, accélère le build, et empêche surtout de faire fuiter des secrets (comme un fichier `.env`) en production.

Pourquoi utilise-t-on la commande `astream` ou `astream_events` dans un graphe LangGraph pour une UI comme Chainlit ? #flashcard
L'utilisation de méthodes asynchrones de streaming permet de renvoyer la réponse du LLM "token par token" à l'utilisateur (effet machine à écrire), réduisant ainsi la latence perçue (Time To First Token). De plus, ça permet d'intercepter les étapes intermédiaires (quand l'agent utilise un outil) et de les afficher en temps réel dans l'interface sans bloquer l'application.
