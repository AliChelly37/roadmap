# 🤖 Week 06 - AI Agents & Orchestration

Ce dossier regroupe nos implémentations de la **Semaine 6**, validant le double défi : l'**Option A** (Agent ReAct outillé et modélisé en graphe avec **LangGraph**) et l'**Option B** (Système multi-agents collaboratif avec **CrewAI**), tous deux orchestrés en local via **Ollama** (`llama3.1`).

---

## 🛠️ Architecture & Fichiers

### Option A : Agent ReAct outillé (LangGraph)
*   `simple_agent.py` : Notre premier agent LangGraph minimal. Il implémente un `StateGraph` simple relié à un outil de calcul (`multiply`) et utilise la condition standard `tools_condition` pour boucler.
*   `advanced_agent.py` : Notre agent de rédaction analytique autonome. Il est structuré sous forme de graphe à 4 nœuds (`research`, `draft`, `critique`, `save`) et intègre la mémoire à court terme via un checkpointer (`MemorySaver`).
*   `server.py` : Un serveur **FastAPI** qui expose l'agent LangGraph via un endpoint `POST /agent` et diffuse en direct la trace d'exécution sous forme de Server-Sent Events (SSE).

### Option B : Système Multi-Agents (CrewAI)
*   `crew_agent.py` : Notre équipe de 3 agents qui collaborent séquentiellement pour rédiger le même rapport analytique.
    *   **Researcher** : Chercheur outillé de RAG et recherche web pour consigner les faits.
    *   **Writer** : Synthétise le journal de recherche pour rédiger un premier brouillon structuré.
    *   **Reviewer** : Critique le brouillon, effectue les corrections finales et écrit le fichier final.

### Outils Communs
Les agents partagent un arsenal d'outils puissants :
1.  `web_search` : Recherche web gratuite et en direct via DuckDuckGo.
2.  `scrape_url` : Extraction et nettoyage du texte brut d'un site web via BeautifulSoup (avec troncature de sécurité à 3500 caractères).
3.  `search_my_docs` : Recherche sémantique locale dans notre base de données vectorielle Chroma (RAG Semaine 5) à l'aide des embeddings Multilingual E5.
4.  `save_markdown` : Sauvegarde persistante des rapports rédigés.

---

## 🚀 Comment exécuter les scripts

Assurez-vous que votre serveur local **Ollama** est démarré et que le modèle `llama3.1` est disponible.

### 1. Lancer l'agent simple (Calcul)
```bash
.venv\Scripts\python week-06-agent\simple_agent.py
```

### 2. Exécuter l'agent LangGraph Avancé (Recherche/Rapport)
```bash
.venv\Scripts\python week-06-agent\advanced_agent.py
```
*Le rapport généré sera sauvegardé dans `week-06-agent/rapport_raft_multi_agents.md`.*

### 3. Exécuter le serveur d'API et tester le Streaming (SSE)
Dans un premier terminal, lancez le serveur :
```bash
.venv\Scripts\python week-06-agent\server.py
```

Dans un second terminal, interrogez l'API en streaming :
```bash
.venv\Scripts\python -c "import requests; r = requests.post('http://127.0.0.1:8000/agent', json={'topic': 'Raft consensus in multi-agents', 'filename': 'rapport_test_stream.md'}, stream=True); [print(line.decode('utf-8')) for line in r.iter_lines() if line]"
```
*Vous verrez les événements de transition du graphe s'afficher en temps réel.*

### 4. Lancer le Système Multi-Agents (CrewAI)
```bash
.venv\Scripts\python week-06-agent\crew_agent.py
```
*Le rapport généré sera sauvegardé dans `week-06-agent/rapport_raft_multi_agents_crew.md`.*

---

## 📈 Analyse & Comparaison des Frameworks

1.  **Garde-fous (Loops & Safety)** :
    Dans `advanced_agent.py`, nous avons modélisé une arête conditionnelle vérifiant si le rapport a été validé ou si le compteur d'itérations a atteint la limite de 4 (`iteration >= 4`). Ce garde-fou est indispensable avec les LLMs locaux pour éviter les boucles infinies de "perfectionnisme" (l'auto-critique qui rejette constamment le rapport).
2.  **Robustesse sémantique** :
    LangGraph s'est révélé extrêmement fiable pour contrôler précisément le flux de travail (la recherche s'arrête dès que l'agent renvoie le token attendu, et l'auto-critique suit des nœuds fixes). CrewAI est plus simple à écrire et excellent pour générer du texte créatif, mais demande plus d'efforts de prompt engineering pour éviter que le modèle local ne dérive ou ne s'égare.
3.  **Compatibilité des signatures d'outils** :
    CrewAI valide les arguments des outils à l'aide de Pydantic v2. Les outils LangChain bruts ne s'y injectent pas directement, d'où la nécessité d'utiliser le décorateur `@tool` de `crewai.tools` pour assurer la conversion.
