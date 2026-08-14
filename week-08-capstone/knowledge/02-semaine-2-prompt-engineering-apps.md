# 🗣️ Semaine 2 — Prompt engineering & premières apps LLM

**📍 Partie 2 / 9** · Phase : 🧱 *Fondations* · Charge : **~20 h** (5 jours × ~4 h)
**🎯 Livrable de la semaine :** une **API FastAPI** qui **streame** la réponse du LLM token par token, expose une **extraction structurée** (Pydantic) et possède une **mini-suite d'évaluation**.

> 🔄 **Refresh éclair (si un prérequis est fragile) :**
> - **async / await** en Python (indispensable pour le streaming) → cherche « real python async io » ⏱️ ~20 min
> - **HTTP & verbes REST** (GET/POST, codes 2xx/4xx) ⏱️ ~10 min
> - Tu réutilises ton **« LLM Playground »** de la S1 (multi-provider + structured output) : garde-le ouvert.

---

## 🎯 Objectifs

À la fin de la semaine, tu sais :
- Concevoir des **prompts robustes** avec les techniques clés (rôle, instructions claires, séparation données/instructions, **few-shot**, **chain-of-thought**, **ReAct**, **self-consistency**).
- **Templatiser** tes prompts (variables, exemples) pour les réutiliser proprement.
- Construire une **API LLM avec FastAPI** : endpoints, validation Pydantic, gestion async.
- **Streamer** la sortie du modèle (SSE / `StreamingResponse`) pour une UX « machine à écrire ».
- Mettre en place une **évaluation de base** (cas de test + assertions) pour ne plus juger « à l'œil ».

---

## 🧩 Concepts clés

- **Anatomie d'un bon prompt** : rôle, contexte, instructions, format de sortie, exemples
- **Few-shot** vs **zero-shot** ; pourquoi les exemples cadrent le comportement
- **Chain-of-Thought (CoT)** : laisser le modèle « réfléchir » avant de répondre
- **Self-Consistency** : échantillonner plusieurs raisonnements et voter
- **ReAct** (Reason + Act) : alterner raisonnement et actions/outils (préfigure les agents en S6)
- **Templating de prompts** (variables, Jinja2 ou f-strings structurées)
- **FastAPI** : routes, modèles Pydantic en entrée/sortie, `async def`, Uvicorn
- **Streaming** : `StreamingResponse`, **Server-Sent Events (SSE)**, `text/event-stream`
- **Évaluation** : jeu de cas, **assertions** déterministes (regex, JSON-schema) vs **LLM-as-a-judge**, détection de régressions

---

## 📚 Ressources gratuites

> 📄 cours · 📖 doc · 🎥 vidéo · 📝 article · 💻 repo · 🛠️ playground | 🟢 fonda. · 🟡 inter. · 🔴 avancé · ⭐ incontournable

### Prompt engineering (J1–J2)
- 📄 ⭐ **Anthropic — Prompt Engineering Interactive Tutorial** (9 chapitres + exercices, notebooks) 🟡 — `github.com/anthropics/courses` → `prompt_engineering_interactive_tutorial`
- 📄 **Anthropic — Real World Prompting** (techniques en conditions réelles) 🟡 — même repo `anthropics/courses`
- 📖 ⭐ **Anthropic — Prompt engineering overview** 🟡 — `platform.claude.com/docs` (→ *Build with Claude* → *Prompt engineering*)
- 📄 ⭐ **Prompt Engineering Guide (DAIR.AI)** — CoT, few-shot, ReAct, self-consistency, etc. 🟡 — `promptingguide.ai`
- 📄 **Learn Prompting** (parcours progressif, gratuit) 🟢 — `learnprompting.org`
- 📄 **DeepLearning.AI — Short Courses** (ex. *ChatGPT Prompt Engineering for Developers*, ~1–2 h, gratuit) 🟢 — `deeplearning.ai/short-courses`
- 📖 **OpenAI — Prompt engineering guide** 🟡 — `developers.openai.com/api/docs` (→ *Guides*)
- 📝 *(optionnel 🔴, les papiers fondateurs — cherche le titre sur arXiv)* : **Chain-of-Thought** (Wei et al., 2022) · **Self-Consistency** (Wang et al., 2022) · **ReAct** (Yao et al., 2022)

### FastAPI & streaming (J3–J4)
- 📖 ⭐ **FastAPI — Tutorial / User Guide** 🟢 — `fastapi.tiangolo.com` (→ *Tutorial - User Guide*)
- 📖 ⭐ **FastAPI — Stream Data** (cas d'usage explicite : sortie d'un LLM) 🟡 — `fastapi.tiangolo.com/advanced/stream-data/`
- 📖 **Anthropic — Streaming Messages** / **OpenAI — Streaming** 🟡 — docs respectives (`platform.claude.com/docs`, `developers.openai.com/api/docs`)
- 💻 **`sse-starlette`** — `EventSourceResponse` pour des SSE propres 🟡 — `github.com/sysid/sse-starlette`

### Évaluation (J5)
- 📄 ⭐ **Anthropic — Prompt Evaluations** (écrire des évals de prod) 🟡 — repo `anthropics/courses` → `prompt_evaluations`
- 💻 ⭐ **promptfoo** — évals LLM en YAML, comparaison de modèles, CI 🟡 — `promptfoo.dev` (et `github.com/promptfoo/promptfoo`)
- 📝 **Hamel Husain — écrits sur les évals** (« Your AI product needs evals ») 🟡 — `hamel.dev/blog`
- 💻 **`Vvkmnn/awesome-ai-eval`** — annuaire d'outils & méthodes d'éval 🟢

---

## 💻 Repos GitHub (à lire / forker)

- 💻 ⭐ **`anthropics/courses`** — prompting, *prompt evaluations*, tool use (notebooks exécutables)
- 💻 ⭐ **`promptfoo/promptfoo`** — framework d'évaluation (exemples `promptfoo init`)
- 💻 **`openai/openai-cookbook`** — recettes de prompting & structured outputs
- 💻 **`encode/starlette`** / **`sysid/sse-starlette`** — base technique du streaming SSE
- 💻 *(réf. S1)* **`instructor-ai/instructor`** — sorties structurées réutilisées ici

---

## 🛠️ Projet / Livrable : « LLM API » (FastAPI + streaming + structured + éval)

🎯 Transforme ton script S1 en **service web**. Une seule app FastAPI avec ces endpoints :

**Cahier des charges (Definition of Done) :**
1. **`POST /chat` (streaming)** — reçoit un message, **streame la réponse token par token** via `StreamingResponse` (ou SSE `text/event-stream`). Une page HTML minimale (ou un script `curl`/`requests`) montre l'effet « machine à écrire ».
2. **Prompts templatisés** — un **system prompt** réutilisable + **≥1 technique avancée** (few-shot **ou** CoT). Les variables du prompt sont injectées proprement (Jinja2 ou helper dédié).
3. **`POST /extract` (structuré)** — renvoie un **JSON validé Pydantic** (réutilise `JobPosting` de la S1 ou un nouveau schéma).
4. **Mini-suite d'éval** — **≥3 cas de test** avec assertions (ex. *contains*, JSON valide, ou une `llm-rubric`) via **promptfoo** *ou* un petit script Python. La suite **passe** au vert.
5. **Repo** — code dans `ai-engineer-roadmap/week-02-llm-api/`, `.env` non commité, **README** (lancement Uvicorn, exemples de requêtes, comment lancer les évals).

**🌟 Bonus :**
- Endpoint `/health` + gestion d'erreurs (timeout LLM, 4xx/5xx propres).
- Bascule de provider via paramètre (réutilise l'interface unifiée S1).
- Comparer 2 modèles sur ta suite d'éval et noter les écarts.

---

## 🗓️ Plan jour par jour

> IDs : `S2-J{jour}-T{tâche}`. Durées indicatives. 🧪 = code · 🎯 = contribue au livrable.

### J1 — Fondations du prompting *(~4 h)*
- [ ] **S2-J1-T1** — Lire **Anthropic Prompt engineering overview** ⏱️ ~30 min
- [ ] **S2-J1-T2** — 🧪 Faire les **chapitres 1–5** du *Prompt Engineering Interactive Tutorial* (structure, clarté, rôles, séparation données/instructions, format) ⏱️ ~2 h
- [ ] **S2-J1-T3** — Parcourir **promptingguide.ai** : sections *zero/few-shot* + *CoT* ⏱️ ~1 h
- [ ] **S2-J1-T4** — 🧪 Noter 3 prompts « avant/après » améliorés dans ton journal ⏱️ ~30 min

### J2 — Techniques avancées & templating *(~4 h)*
- [ ] **S2-J2-T1** — 🧪 Chapitres **6–9** du tutoriel (think step-by-step, few-shot, formatage de sortie) ⏱️ ~1 h 30
- [ ] **S2-J2-T2** — Lire **ReAct** & **Self-Consistency** sur promptingguide.ai ⏱️ ~45 min
- [ ] **S2-J2-T3** — 🧪 🎯 Construire un **template de prompt réutilisable** (system + few-shot, variables injectées) ⏱️ ~1 h 15
- [ ] **S2-J2-T4** — 🧪 Tester le template sur 2-3 entrées et comparer les sorties ⏱️ ~30 min

### J3 — FastAPI : première API *(~4 h)*
- [ ] **S2-J3-T1** — Suivre le **Tutorial FastAPI** (routes, paramètres, modèles Pydantic) ⏱️ ~1 h 30
- [ ] **S2-J3-T2** — 🧪 🎯 Créer l'app : `POST /chat` (non-streaming d'abord) qui appelle ton LLM ⏱️ ~1 h 30
- [ ] **S2-J3-T3** — 🧪 🎯 Ajouter `POST /extract` renvoyant un **JSON Pydantic** ⏱️ ~1 h

### J4 — Streaming (SSE / StreamingResponse) *(~4 h)*
- [ ] **S2-J4-T1** — Lire **FastAPI – Stream Data** + doc *streaming* de ton provider ⏱️ ~45 min
- [ ] **S2-J4-T2** — 🧪 🎯 Convertir `/chat` en **streaming** (générateur async qui *yield* les tokens) ⏱️ ~1 h 30
- [ ] **S2-J4-T3** — 🧪 Tester le flux avec `curl`/`requests` (chunks) **et** une petite page HTML `EventSource` ⏱️ ~1 h
- [ ] **S2-J4-T4** — 🧪 Gérer la fin de flux + une erreur mid-stream proprement ⏱️ ~45 min

### J5 — Évaluation & finalisation *(~4 h)*
- [ ] **S2-J5-T1** — Lire l'intro de **promptfoo** + survol du cours **Prompt Evaluations** ⏱️ ~45 min
- [ ] **S2-J5-T2** — 🧪 🎯 Écrire une **suite d'éval** : ≥3 cas, assertions (contains / JSON valide / rubric) ⏱️ ~1 h 30
- [ ] **S2-J5-T3** — 🧪 Lancer la suite, corriger un prompt qui échoue, re-tester ⏱️ ~45 min
- [ ] **S2-J5-T4** — 🧪 🎯 Écrire le **README** et **pousser sur GitHub** ⏱️ ~1 h

---

## ✅ Critères de réussite (validation de la semaine)

- [ ] Mon API FastAPI tourne en local et `POST /chat` **streame** la réponse token par token.
- [ ] J'utilise un **prompt templatisé** avec au moins une technique avancée (few-shot ou CoT).
- [ ] `POST /extract` renvoie un **JSON validé par Pydantic**.
- [ ] Ma **suite d'éval** (≥3 cas) passe au vert et je sais ce qu'elle teste.
- [ ] Le code est **sur GitHub** avec un README clair (lancement + requêtes + évals).
- [ ] Je peux **expliquer** : différence few-shot / CoT / ReAct, et pourquoi le streaming améliore l'UX sans accélérer le calcul.

> 🧭 **Auto-éval rapide :** si un point coince, note-le — le second brain en fera une tâche de rattrapage week-end.

---

## 🔜 Suite

➡️ **Partie 3 — Semaine 3 : Embeddings & recherche vectorielle** — modèles d'embeddings, bases vectorielles (Chroma / Qdrant / pgvector), indexation (HNSW), métriques de similarité. Tu construiras un **moteur de recherche sémantique** : la première brique du RAG (S4–S5).

---

*Partie 2 d'un guide en 9 parties. Liens vérifiés en juin 2026.*
