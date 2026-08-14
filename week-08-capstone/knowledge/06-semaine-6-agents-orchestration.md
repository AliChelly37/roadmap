# 🤖 Semaine 6 — Agents IA & orchestration

**📍 Partie 6 / 9** · Phase : 🤖 *Agents* · Charge : **~20 h** (5 jours × ~4 h)
**🎯 Livrable de la semaine :** un **agent outillé** (recherche web + exécution de code + **ton RAG**) construit avec **LangGraph** — *ou* un **système multi-agents** (CrewAI).

> 🔄 **Refresh éclair (si un prérequis est fragile) :**
> - Tu **réutilises le function calling de la S1** : c'est la base des outils d'un agent.
> - Tu **transformes ton RAG (S4–S5) en outil** que l'agent appelle (`search_my_docs`).
> - ⚠️ **Exécution de code = risque** : on n'exécute jamais du code arbitraire sans **sandbox** (on en reparle en J3).

---

## 🎯 Objectifs

À la fin de la semaine, tu sais :
- Distinguer un **agent** (boucle **ReAct** : raisonner → agir → observer) d'un **workflow** orchestré.
- Construire un **agent outillé** avec **LangGraph** (machine à états : nœuds, arêtes, cycles).
- Donner des **outils réels** à l'agent : **recherche web**, **exécution de code (sandbox)**, **ton RAG**.
- Gérer la **mémoire** d'agent (court terme / long terme, *checkpointers*).
- Construire un **système multi-agents** avec rôles (**CrewAI**) et connaître les patterns (*supervisor*, *handoffs*).
- Situer **MCP** (Model Context Protocol), le standard de connexion outils ↔ agents.

---

## 🧩 Concepts clés

- **Agent = LLM + boucle + outils + mémoire** ; **ReAct** : *Thought → Action → Observation → …*
- **Workflow vs agent** (Anthropic) : *prompt chaining*, *routing*, *parallelization*, *orchestrator-workers*, *evaluator-optimizer* — **commence simple**, n'ajoute de l'autonomie que si nécessaire
- **LangGraph** : `StateGraph`, **nœuds**, **arêtes conditionnelles**, **cycles**, **checkpointers** (mémoire), **human-in-the-loop**
- **Mémoire** : *court terme* (état/historique de conversation) vs *long terme* (vector store / `mem0`)
- **Multi-agents** : **rôles** (CrewAI : researcher/writer/reviewer), **supervisor** (routage explicite), **handoffs** (passage de contrôle avec données **typées**)
- ⚠️ **Risques multi-agents** : boucles infinies, **amplification d'erreurs** → garde-fous (limite d'itérations, budgets, validation)
- **MCP** : protocole ouvert (Linux Foundation) pour brancher des outils/données à un agent
- **Outils gratuits** : recherche web (**Tavily** free tier, **DuckDuckGo**), exécution de code **en sandbox**

---

## 📚 Ressources gratuites

> 📄 cours · 📖 doc · 🎥 vidéo · 📝 article · 💻 repo · 🎓 free tier | 🟢 fonda. · 🟡 inter. · 🔴 avancé · ⭐ incontournable

### Fondamentaux des agents (J1)
- 📝 ⭐ **Anthropic — « Building Effective Agents »** (la référence : workflows vs agents) 🟡 — `anthropic.com` (cherche « Building Effective Agents »)
- 📄 ⭐ **Hugging Face — AI Agents Course**, Unit 1 (concepts) 🟢 — `huggingface.co/learn/agents-course`
- 📝 *(rappel S2)* **ReAct** — raisonner + agir en boucle 🟢

### LangGraph (J2–J3)
- 📄 ⭐ **LangChain Academy — Introduction to LangGraph** (cours gratuit) 🟡 — `academy.langchain.com`
- 📖 ⭐ **LangGraph — Docs & Tutorials** (`StateGraph`, tool-calling, mémoire) 🟡 — `docs.langchain.com/langgraph`
- 📄 **HF Agents Course — Unit 2 : LangGraph** 🟡 — `huggingface.co/learn/agents-course` (→ Unit 2)

### Multi-agents (J4)
- 📖 ⭐ **CrewAI — Docs & Quickstart** (rôles, tâches, crews) 🟡 — `docs.crewai.com`
- 📄 **DeepLearning.AI — *Multi AI Agent Systems with crewAI*** (gratuit) 🟢 — `deeplearning.ai/short-courses`
- 📖 *(alternatives à connaître)* **OpenAI Agents SDK** · **Claude Agent SDK** · **Pydantic AI** (type-safe) — docs respectives 🟡
- ℹ️ **Note 2026** : *AutoGen* a fusionné dans **Microsoft Agent Framework** — apprends plutôt **LangGraph** (contrôle) + **CrewAI** (multi-agent facile)

### Outils & MCP (J3)
- 📖 ⭐ **MCP — Model Context Protocol** (spec + quickstart) 🟡 — `modelcontextprotocol.io`
- 💻 ⭐ **`NirDiamant/GenAI_Agents`** — **50+ tutos** (LangGraph, MCP, multi-agents) 🟡 — `github.com/NirDiamant/GenAI_Agents`
- 🎓 **Tavily** (recherche web, free tier) — `tavily.com` · **DuckDuckGo Search** (gratuit, sans clé)

---

## 💻 Repos GitHub (à lire / forker)

- 💻 ⭐ **`NirDiamant/GenAI_Agents`** — la mine de la semaine (du bot simple au multi-agents)
- 💻 **`NirDiamant/agents-towards-production`** — patterns d'agents en production
- 💻 **`huggingface/agents-course`** — notebooks du cours HF
- 💻 ⭐ **`langchain-ai/langgraph`** — framework + exemples
- 💻 **`crewAIInc/crewAI`** — multi-agents par rôles

---

## 🛠️ Projet / Livrable : agent outillé (Option A) ou multi-agents (Option B)

🎯 **Choisis une option** (l'A est recommandée pour un généraliste — elle capitalise sur ton RAG).

### Option A — Agent ReAct outillé (LangGraph)
Un agent qui **raisonne, choisit des outils, et résout des questions multi-étapes** :
1. **Outils** — au moins **2-3** parmi : **recherche web** (Tavily/DuckDuckGo), **exécution de code en sandbox** (calculatrice / REPL Python restreint), et **`search_my_docs`** (ton RAG S4–S5).
2. **Boucle ReAct** — l'agent décide quel outil appeler, observe le résultat, et itère jusqu'à la réponse.
3. **Mémoire** — ajoute un **checkpointer** (SQLite/in-memory) pour tenir une conversation multi-tours.
4. **Garde-fous** — **limite d'itérations** + arrêt propre (pas de boucle infinie).
5. **UI** — expose `POST /agent` en **streaming** (réutilise S2), montre les étapes (trace).
6. **Repo** — `ai-engineer-roadmap/week-06-agent/`, **README** (outils, exemples de questions multi-étapes).

### Option B — Système multi-agents (CrewAI)
Une **crew** qui produit un livrable (ex. mini-rapport) :
- **Researcher** (utilise recherche web + ton RAG) → **Writer** → **Reviewer**.
- Rôles + tâches définis, sortie finale assemblée, garde-fous contre les boucles.

**🌟 Bonus (les deux options) :**
- Brancher **un outil via MCP** (tuto NirDiamant).
- Comparer **LangGraph vs CrewAI** sur la même tâche.
- **Mémoire long terme** (vector store / `mem0`).
- Pattern **supervisor** ou **human-in-the-loop** (validation avant action sensible).

> ⚠️ **Sécurité (exécution de code) :** n'exécute jamais de code arbitraire du LLM sur ta machine sans isolation. Utilise un **REPL restreint**, un conteneur, ou un **sandbox** (ex. free tier dédié). Limite aussi les **actions** de l'agent (pas d'accès fichiers/réseau non maîtrisé).

---

## 🗓️ Plan jour par jour

> IDs : `S6-J{jour}-T{tâche}`. Durées indicatives. 🧪 = code · 🎯 = contribue au livrable.

### J1 — Fondamentaux des agents *(~4 h)*
- [x] **S6-J1-T1** — Lire ⭐ **« Building Effective Agents »** (Anthropic) — workflows vs agents ⏱️ ~1 h
- [x] **S6-J1-T2** — HF Agents Course **Unit 1** (boucle, outils, observation) ⏱️ ~1 h 30
- [x] **S6-J1-T3** — 🧪 Décrire dans ton journal **ton agent cible** : tâche, outils, critère d'arrêt ⏱️ ~30 min
- [x] **S6-J1-T4** — Choisir **Option A ou B** et le framework ⏱️ ~30 min

### J2 — LangGraph : premier agent *(~4 h)*
- [x] **S6-J2-T1** — **LangChain Academy — Intro to LangGraph** (modules 1–2) ⏱️ ~1 h 30
- [x] **S6-J2-T2** — 🧪 🎯 Construire un **`StateGraph`** minimal (nœuds, arêtes, état) ⏱️ ~1 h 30
- [x] **S6-J2-T3** — 🧪 🎯 Ajouter un **premier outil** (calculatrice) et la boucle de tool-calling ⏱️ ~1 h

### J3 — Outils, mémoire & MCP *(~4 h)*
- [x] **S6-J3-T1** — 🧪 🎯 Ajouter la **recherche web** (Tavily/DuckDuckGo) ⏱️ ~1 h
- [x] **S6-J3-T2** — 🧪 🎯 Brancher **ton RAG comme outil** `search_my_docs` ⏱️ ~1 h
- [x] **S6-J3-T3** — 🧪 🎯 Ajouter la **mémoire** (checkpointer) + **limite d'itérations** ⏱️ ~1 h
- [x] **S6-J3-T4** — Lire l'intro **MCP** + tuto NirDiamant (concept) ⏱️ ~1 h

### J4 — Multi-agents (ou LangGraph avancé) *(~4 h)*
- [x] **S6-J4-T1** — Lire **CrewAI Quickstart** (rôles, tâches, crew) ⏱️ ~45 min
- [x] **S6-J4-T2** — 🧪 🎯 Construire une **crew à 2-3 rôles** (researcher → writer → reviewer) **ou** un pattern **supervisor** en LangGraph ⏱️ ~2 h
- [x] **S6-J4-T3** — 🧪 Tester sur une tâche réelle, observer la collaboration ⏱️ ~45 min
- [x] **S6-J4-T4** — Noter les **risques** observés (boucles, dérives) et les garde-fous ⏱️ ~30 min

### J5 — Assemblage, garde-fous & finalisation *(~4 h)*
- [x] **S6-J5-T1** — 🧪 🎯 Renforcer les **garde-fous** (budget, validation avant action sensible) ⏱️ ~1 h
- [x] **S6-J5-T2** — 🧪 🎯 Exposer l'agent en **streaming** (trace des étapes) ⏱️ ~1 h 15
- [x] **S6-J5-T3** — 🧪 *(bonus)* Brancher **un outil via MCP** ⏱️ ~1 h
- [x] **S6-J5-T4** — 🧪 🎯 **README** + **push GitHub** ⏱️ ~45 min

---

## ✅ Critères de réussite (validation de la semaine)

- [x] Je sais **distinguer agent vs workflow** et expliquer la **boucle ReAct**.
- [x] Mon agent **appelle ≥2 outils** (dont une recherche web et/ou **mon RAG**) et résout une **tâche multi-étapes**.
- [x] L'agent a une **mémoire** (checkpointer) sur plusieurs tours.
- [x] J'ai des **garde-fous** (limite d'itérations / budget) et l'exécution de code est **isolée**.
- [x] *(Option B)* J'ai **≥2 agents avec rôles** qui collaborent.
- [x] Le code est **sur GitHub** avec un README clair (prêt à être poussé).
- [x] Je peux **expliquer** un pattern multi-agents (*supervisor* ou *handoffs*) et **ce qu'est MCP** ou comment il fonctionne.

> 🧭 **Auto-éval rapide :** un point bloque ? Note-le — le second brain en fera une tâche de rattrapage week-end.

---

## 🔜 Suite

➡️ **Partie 7 — Semaine 7 : Mise en production & LLMOps** — serving (async, batching, streaming), **caching sémantique**, **observabilité/tracing** (LangSmith, Phoenix, Langfuse), évaluation continue, **coûts & rate limiting**, **garde-fous** (prompt injection, PII, modération), fallbacks. Tu **instrumenteras** ton agent/RAG pour le rendre fiable.

---

*Partie 6 d'un guide en 9 parties. Liens vérifiés en juin 2026 — l'écosystème agents bouge très vite (frameworks, versions, MCP), revérifie le moment venu.*
