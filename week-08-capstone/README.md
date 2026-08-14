---
title: AI Roadmap Assistant
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 4.41.0
---

# AI Engineering Roadmap - Capstone Project

Ceci est le projet de fin (Capstone) de la formation AI Engineering. Il s'agit d'un agent conversationnel (AI Roadmap Assistant) capable de répondre aux questions sur le programme de la formation.

## Architecture
- **UI** : Chainlit
- **Orchestration** : LangGraph (Agent ReAct)
- **Base de connaissances** : ChromaDB local (RAG)
- **Gateway LLM** : LiteLLM
- **Observabilité** : Langfuse

## Installation Locale
1. Clonez ce dépôt.
2. Installez les dépendances : `pip install -r requirements.txt`.
3. Lancez l'application : `chainlit run app.py`.
