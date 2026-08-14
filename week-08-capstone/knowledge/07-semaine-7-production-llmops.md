# 🚀 Semaine 7 — Mise en production & LLMOps

**📍 Partie 7 / 9** · Phase : 🚀 *Production* · Charge : **~20 h** (5 jours × ~4 h)
**🎯 Livrable de la semaine :** ton app (RAG S5 **ou** agent S6) rendue **fiable** : **tracing + gateway + cache + garde-fous + éval continue**.

> 🔄 **Refresh éclair (si un prérequis est fragile) :**
> - Tu **instrumentes une app existante** (ton RAG S5 ou ton agent S6) — choisis-en une.
> - **async / streaming** (S2) : utiles pour le serving et les garde-fous en streaming.
> - **Tout reste gratuit** : Langfuse (free tier + self-host), LiteLLM, LLM Guard… tout est open-source.

---

## 🎯 Objectifs

À la fin de la semaine, tu sais :
- **Instrumenter** ton app avec du **tracing/observabilité** (voir latence, tokens, coûts, étapes).
- Router via un **gateway** (LiteLLM) : interface unifiée, **fallbacks**, **suivi des coûts**, **rate limiting**.
- Ajouter un **cache sémantique** pour réduire coûts et latence.
- Poser des **garde-fous** entrée/sortie : **injection**, **PII**, **modération**, validation de schéma.
- Mettre en place une **évaluation continue** (CI) qui **détecte les régressions**.
- Connaître les **menaces** (OWASP LLM Top 10) et auditer ton app.

---

## 🧩 Concepts clés

- **Serving** : `async`, **batching**, **streaming** (S2), concurrence (les appels LLM sont *I/O-bound*)
- **Observabilité** : *traces*, *spans*, latence, tokens, coûts — ⚠️ **tracing ≠ évaluation** (l'un dit *ce qui s'est passé*, l'autre *si c'était bon*)
- **Gateway / proxy** (LiteLLM) : 1 interface pour 100+ modèles, **fallbacks**, retries, **budgets**, rate limiting, **suivi des coûts**
- **Caching** : *exact* (même requête) et **sémantique** (requête similaire) → moins d'appels, moins cher
- **Garde-fous — 4 couches** : *pré-prompt* (PII, injection) → *pré-inférence* (intégrité du system prompt, budget) → *post-inférence* (modération, schéma, **grounding**) → *post-action* (valider **avant** tout effet de bord/outil)
- **OWASP LLM Top 10** : la grille de menaces de référence (injection, fuite de données, etc.)
- **Coûts** : *token counting*, suivi par modèle/utilisateur, optimisation
- **Fallbacks** : si un fournisseur échoue/atteint son quota → bascule automatique
- **Évaluation continue** : evals en **CI/CD**, *regression detection*, **datasets** issus de la prod

---

## 📚 Ressources gratuites

> 📄 cours · 📖 doc · 📝 article · 💻 repo · 🎓 free tier | 🟢 fonda. · 🟡 inter. · 🔴 avancé · ⭐ incontournable

### Observabilité & tracing (J1)
- 📖 ⭐ **Langfuse** — open-source (MIT), free tier **50k obs/mois**, self-host Docker en 5 min ; décorateur `@observe()` 🟡 — `langfuse.com` (et `github.com/langfuse/langfuse`)
- 📖 **Arize Phoenix** — local-first, notebook-friendly, excellent pour le **RAG** 🟡 — `arize.com/phoenix` (et `github.com/Arize-ai/phoenix`)
- 📖 **LangSmith** — si ton app est en **LangChain/LangGraph** (free tier) 🟢 — `smith.langchain.com`

### Gateway, coûts, fallbacks, caching (J2–J3)
- 📖 ⭐ **LiteLLM** — proxy/SDK unifié (100+ modèles, Ollama), **fallbacks**, **budgets**, rate limiting, **caching** 🟡 — `docs.litellm.ai` (et `github.com/BerriAI/litellm`)
- 💻 **GPTCache** — cache sémantique 🟡 — `github.com/zilliztech/GPTCache`
- 📖 **LiteLLM Caching** (Redis / in-memory) 🟡 — section *Caching* de la doc LiteLLM

### Garde-fous (J4)
- 📖 ⭐ **LLM Guard** (Protect AI) — scanners **injection / PII / toxicité / secrets** (entrée + sortie), self-host 🟡 — `llm-guard.com` (et `github.com/protectai/llm-guard`)
- 📖 **NeMo Guardrails** (NVIDIA) — *dialog rails* (Colang), jailbreak, sécurité agentique 🔴 — `github.com/NVIDIA-NeMo/Guardrails`
- 📖 **Guardrails AI** — **validation de sortie** (RAIL/Pydantic) + reprompt correctif 🟡 — `guardrailsai.com` (et `github.com/guardrails-ai/guardrails`)
- 📖 **Microsoft Presidio** — détection/anonymisation **PII** 🟡 — `github.com/microsoft/presidio`
- 📖 **Meta — Llama Guard / Prompt Guard** — classifiers de sécurité 🟡 — sur Hugging Face
- 🎓 **OpenAI Moderation API** (gratuite) 🟢
- 📝 ⭐ **OWASP — LLM Top 10** (menaces) 🟡 — `genai.owasp.org`

### Évaluation continue (J5)
- 💻 ⭐ *(réf. S2)* **promptfoo** — evals en **CI/CD** (GitHub Actions) 🟡 — `promptfoo.dev`
- 📖 *(réf. S5)* **RAGAS** + **Langfuse datasets** (LLM-as-judge sur données de prod) 🟡
- 📝 *(survol 🔴)* **Garak / PyRIT** — red-teaming automatisé

---

## 💻 Repos GitHub (à lire / forker)

- 💻 ⭐ **`langfuse/langfuse`** — observabilité/tracing
- 💻 ⭐ **`BerriAI/litellm`** — gateway (fallbacks, coûts, caching)
- 💻 ⭐ **`protectai/llm-guard`** — garde-fous entrée/sortie
- 💻 **`Arize-ai/phoenix`** — tracing/éval orienté RAG
- 💻 **`NVIDIA-NeMo/Guardrails`** + **`guardrails-ai/guardrails`** — rails programmables
- 💻 **`microsoft/presidio`** — PII

---

## 🛠️ Projet / Livrable : « App instrumentée »

🎯 Prends **ton RAG S5 ou ton agent S6** et rends-le **production-grade**.

**Cahier des charges (Definition of Done) :**
1. **Tracing** — instrumente avec **Langfuse** : chaque appel LLM, retrieval, tool call, **latence**, **tokens**, **coût** est visible dans le dashboard.
2. **Gateway** — fais passer les appels par **LiteLLM** : interface unifiée, **fallback** vers un 2ᵉ fournisseur en cas d'échec, **suivi des coûts** par requête, **rate limiting**.
3. **Cache** — ajoute un **cache** (exact + sémantique) pour éviter de rappeler le LLM sur des requêtes similaires.
4. **Garde-fous** — **entrée** (redaction PII via Presidio/LLM Guard + détection d'injection) **et sortie** (modération + validation de schéma). Au minimum 1 garde-fou entrée **et** 1 sortie.
5. **Éval continue** — une **suite d'éval en CI** (promptfoo ou dataset Langfuse) qui tourne à chaque changement et **signale les régressions**.
6. **Repo** — `ai-engineer-roadmap/week-07-llmops/`, **README** décrivant le setup (tracing, fallbacks, garde-fous, éval) + une **capture d'une trace**.

**🌟 Bonus :**
- **Audit OWASP LLM Top 10** de ton app (checklist remplie).
- **Rapport de coûts** (par modèle / par requête) depuis Langfuse ou LiteLLM.
- **Garde-fous en streaming** (stratégie de buffering).
- Déployer le **proxy LiteLLM** (Docker).

---

## 🗓️ Plan jour par jour

> IDs : `S7-J{jour}-T{tâche}`. Durées indicatives. 🧪 = code · 🎯 = contribue au livrable.

### J1 — Observabilité & tracing *(~4 h)*
- [x] **S7-J1-T1** — Lire le **quickstart Langfuse** (traces, observations, coûts) ⏱️ ~45 min
- [x] **S7-J1-T2** — 🧪 🎯 Créer un compte (free tier) **ou** self-host Docker ⏱️ ~30 min
- [x] **S7-J1-T3** — 🧪 🎯 **Instrumenter** ton app (décorateur/callbacks) : tracer chaque appel + retrieval/outil ⏱️ ~2 h
- [x] **S7-J1-T4** — 🧪 Inspecter une trace : latence, tokens, coût, étapes ⏱️ ~45 min

### J2 — Gateway : routing, fallbacks, coûts *(~4 h)*
- [x] **S7-J2-T1** — Lire l'intro **LiteLLM** (SDK vs proxy, providers) ⏱️ ~45 min
- [x] **S7-J2-T2** — 🧪 🎯 Router tes appels via **LiteLLM** (interface unifiée) ⏱️ ~1 h 15
- [x] **S7-J2-T3** — 🧪 🎯 Configurer un **fallback** (provider B si A échoue) + **retries** ⏱️ ~1 h
- [x] **S7-J2-T4** — 🧪 🎯 Activer le **suivi des coûts** + un **rate limit** simple ⏱️ ~1 h

### J3 — Caching & optimisation des coûts *(~4 h)*
- [x] **S7-J3-T1** — Lire **caching** (LiteLLM / GPTCache) : exact vs sémantique ⏱️ ~45 min
- [x] **S7-J3-T2** — 🧪 🎯 Ajouter un **cache** et vérifier la **baisse d'appels/latence** sur requêtes répétées ⏱️ ~1 h 30
- [x] **S7-J3-T3** — 🧪 Mesurer le **coût avant/après** cache sur un lot de requêtes ⏱️ ~1 h
- [x] **S7-J3-T4** — Identifier 2-3 **leviers d'optimisation** (modèle moins cher pour tâches simples, prompts plus courts) ⏱️ ~45 min

### J4 — Garde-fous (sécurité) *(~4 h)*
- [x] **S7-J4-T1** — Survol **OWASP LLM Top 10** (les menaces principales) ⏱️ ~45 min
- [x] **S7-J4-T2** — 🧪 🎯 Garde-fou **entrée** : **redaction PII** (Presidio) + **détection d'injection** (LLM Guard) ⏱️ ~1 h 30
- [x] **S7-J4-T3** — 🧪 🎯 Garde-fou **sortie** : **modération** (LLM Guard / OpenAI Moderation) + **validation de schéma** ⏱️ ~1 h 15
- [x] **S7-J4-T4** — 🧪 Tracer les **déclenchements** de garde-fous dans Langfuse ⏱️ ~30 min

### J5 — Éval continue & finalisation *(~4 h)*
- [x] **S7-J5-T1** — 🧪 🎯 Mettre la **suite d'éval en CI** (promptfoo + GitHub Actions ou dataset Langfuse) ⏱️ ~1 h 30
- [x] **S7-J5-T2** — 🧪 Simuler une **régression** (prompt cassé) et vérifier que la CI l'attrape ⏱️ ~45 min
- [ ] **S7-J5-T3** — *(bonus)* **Red-teaming** avec promptfoo (tester des dizaines d'injections auto) ⏱️ ~1 h
- [x] **S7-J5-T4** — 📝 Check final de la PR (app stable, sécurisée, observée) ⏱️ ~45 min

---

## ✅ Critères de réussite (validation de la semaine)

- [ ] Mon app est **tracée** (Langfuse) : je vois **latence, tokens, coûts** et les **étapes**.
- [ ] Je passe par un **gateway** (LiteLLM) avec **fallback** et **suivi des coûts**.
- [ ] J'ai un **cache** (sémantique ou exact) qui **réduit** appels et latence.
- [ ] J'ai des **garde-fous entrée ET sortie** (PII / injection / modération).
- [ ] J'ai une **éval en CI** qui **détecte les régressions**.
- [ ] Je connais l'**OWASP LLM Top 10** et j'ai (au moins) survolé l'audit de mon app.
- [ ] Le code est **sur GitHub** avec un README clair.
- [ ] Je peux **expliquer** la différence *tracing vs évaluation*, et les **4 couches** de garde-fous.

> 🧭 **Auto-éval rapide :** un point bloque ? Note-le — le second brain en fera une tâche de rattrapage week-end.

---

## 🔜 Suite

➡️ **Partie 8 — Semaine 8 : Capstone, déploiement & portfolio** — projet **end-to-end** combinant RAG + agents + production, **containerisation (Docker)**, **déploiement** (HF Spaces / cloud free-tier), touche **multimodale** optionnelle (vision/Whisper), **doc + README + writeup portfolio**, et la **suite après 8 semaines**. La dernière ligne droite : rendre tout ça **montrable**.

---

*Partie 7 d'un guide en 9 parties. Liens vérifiés en juin 2026 — l'outillage LLMOps évolue vite (Langfuse, LiteLLM, garde-fous), revérifie le moment venu.*
