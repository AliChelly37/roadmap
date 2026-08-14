# 🧪 Semaine 5 — RAG avancé & évaluation

**📍 Partie 5 / 9** · Phase : 🔎 *Données & RAG* · Charge : **~20 h** (5 jours × ~4 h)
**🎯 Livrable de la semaine :** une **version « musclée » de ton RAG S4** + une **mesure chiffrée** des gains (avant/après) avec **RAGAS**.

> 🔄 **Refresh éclair (si un prérequis est fragile) :**
> - Tu **pars du RAG S4** (« chat with your docs ») : c'est ta **baseline** à améliorer.
> - **bi-encoder vs cross-encoder** : embeddings rapides (retrieval) vs reranker précis (réordonnancement) — concept clé de la semaine.
> - **BM25** (recherche lexicale par mots-clés) — intuition suffit.

---

## 🎯 Objectifs

À la fin de la semaine, tu sais :
- Améliorer le **retrieval** avec une **recherche hybride** (BM25 + vecteurs, fusion **RRF**).
- Ajouter un **reranker** (cross-encoder) pour booster la **précision** du top-k.
- Appliquer des **transformations de requête** (**HyDE**, **RAG-Fusion**, décomposition, routing).
- **Compresser le contexte** pour réduire le bruit envoyé au LLM.
- Situer **GraphRAG**, **self-RAG** et **corrective-RAG** (vue d'ensemble).
- **Évaluer rigoureusement** avec **RAGAS** et **détecter les régressions** (avant/après).

---

## 🧩 Concepts clés

- **Bi-encoder** (embeddings, rapide, tout le corpus) vs **cross-encoder** (reranker, précis, top-N seulement)
- **Recherche hybride** : **BM25** (lexical, bon pour codes/noms propres/termes exacts) + **dense** (sémantique) → **Reciprocal Rank Fusion (RRF)**
- **Pattern de prod** : *retrieve top-50 hybride → rerank → top-5 → LLM* (+15-30 % sur les métriques RAGAS)
- **Transformations de requête** : **HyDE** (doc hypothétique), **RAG-Fusion** (multi-query + RRF), **décomposition** en sous-questions, **step-back**, **query rewriting**, **routing**
- **Compression de contexte** / *contextual chunk headers* / **Contextual Retrieval** (Anthropic)
- **GraphRAG** (graphe de connaissances, multi-hop) · **self-RAG** / **corrective-RAG (CRAG)** (auto-vérification)
- **Évaluation RAG** : *faithfulness*, *answer relevancy*, *context precision*, *context recall* (RAGAS) ; et **recall@k / MRR / NDCG**
- ⚠️ **Le reranking aide quand le recall est haut mais la précision basse** — il ne « rattrape » jamais un bon chunk absent du candidate set

---

## 📚 Ressources gratuites

> 📄 cours · 📖 doc · 🎥 vidéo · 📝 article · 💻 repo · 🎓 API gratuite | 🟢 fonda. · 🟡 inter. · 🔴 avancé · ⭐ incontournable

### Techniques avancées (transverse)
- 💻 ⭐ **`NirDiamant/RAG_Techniques`** — **un notebook par technique** (HyDE, fusion BM25+vecteurs, décomposition, GraphRAG, reliable RAG…) 🟡 — `github.com/NirDiamant/RAG_Techniques`
- 🎥 ⭐ **LangChain — « RAG from scratch »** (query translation, routing, fusion) 🟡 — repo `langchain-ai/rag-from-scratch`
- 📝 **Advanced RAG** (guides) 🟡 — Weaviate (`weaviate.io/blog`) & Pinecone Learn
- 📝 **Anthropic — Contextual Retrieval** 🔴 — `anthropic.com/news/contextual-retrieval`

### Recherche hybride (J1)
- 💻 ⭐ **`rank_bm25`** — BM25 en Python 🟢 — `github.com/dorianbrown/rank_bm25`
- 📖 **LangChain — `EnsembleRetriever`** (hybride BM25 + vecteurs) 🟡 — `docs.langchain.com`
- 💻 Notebook **`fusion_retrieval`** de `NirDiamant/RAG_Techniques` (RRF clé en main) 🟡

### Reranking (J2)
- 📖 ⭐ **Sentence-Transformers — Cross-Encoders / Rerankers** 🟡 — `sbert.net`
- 📖 ⭐ **`BAAI/bge-reranker-v2-m3`** — reranker **multilingue, gratuit, local** (idéal FR) 🟡 — `huggingface.co/BAAI/bge-reranker-v2-m3`
- 📖 **`cross-encoder/ms-marco-MiniLM-L-6-v2`** — rapide, CPU, anglais 🟢
- 🎓 **Cohere Rerank** (API, essai gratuit) 🟡 — `cohere.com`
- 📖 **LangChain — `ContextualCompressionRetriever`** (reranking + compression) 🟡

### Transformations de requête (J3)
- 💻 ⭐ Notebooks `NirDiamant/RAG_Techniques` : *HyDE*, *query rewriting*, *step-back*, *sub-query decomposition* 🟡
- 🎥 **LangChain rag-from-scratch** : *multi-query*, *RAG-Fusion*, *routing* 🟡

### GraphRAG & RAG « auto-correctif » (J4, survol)
- 💻 ⭐ **Microsoft GraphRAG** 🔴 — `github.com/microsoft/graphrag`
- 📝 *(optionnel 🔴)* **self-RAG** & **corrective-RAG (CRAG)** (arXiv — cherche le titre)

### Évaluation (J5)
- 📖 ⭐ **RAGAS** — métriques & quickstart 🟡 — `docs.ragas.io` (et `github.com/explodinggradients/ragas`) ⚠️ l'API a changé en **v0.2+**, suis la doc à jour
- 💻 **TruLens** — alternative d'éval 🟡 — `github.com/truera/trulens`
- 📝 *(réf. S2)* **promptfoo** a aussi un guide *Evaluating RAG Pipelines* 🟡 — `promptfoo.dev/docs/guides`

---

## 💻 Repos GitHub (à lire / forker)

- 💻 ⭐ **`NirDiamant/RAG_Techniques`** — la référence de la semaine
- 💻 ⭐ **`langchain-ai/rag-from-scratch`** — transformations de requête & routing
- 💻 **`explodinggradients/ragas`** — évaluation RAG
- 💻 **`microsoft/graphrag`** — GraphRAG
- 💻 **`dorianbrown/rank_bm25`** — BM25
- 💻 **`FlagOpen/FlagEmbedding`** — modèles BGE (embeddings + rerankers)

---

## 🛠️ Projet / Livrable : « RAG S4, version pro » + mesure

🎯 Reprends ton **« chat with your docs » (S4)** et améliore-le **méthodiquement**, en **mesurant** chaque gain.

**Cahier des charges (Definition of Done) :**
1. **Baseline + jeu d'éval** — crée un **jeu de 10–20 questions** sur tes PDFs avec **réponses de référence** (ground truth). Mesure la **baseline S4** avec **RAGAS** (*faithfulness*, *answer relevancy*, *context precision/recall*).
2. **Recherche hybride** — remplace le retrieval pur-vecteur par **BM25 + dense** fusionnés en **RRF**.
3. **Reranking** — ajoute un **cross-encoder** (`bge-reranker-v2-m3` en local, *ou* Cohere) : *retrieve top-20/50 → rerank → top-5*.
4. **Transformation de requête** — applique **≥1 technique** (**HyDE** *ou* **RAG-Fusion/multi-query**).
5. **Mesure finale** — relance **RAGAS** et **compare avant/après** dans un **tableau de résultats** (README).
6. **Repo** — `ai-engineer-roadmap/week-05-rag-advanced/`, README avec le **tableau des métriques** et tes conclusions.

> 💡 **Rester gratuit :** RAGAS et HyDE utilisent un LLM « juge/générateur ». Branche **Gemini (AI Studio)** ou **Groq** comme modèle pour ne rien payer.

**🌟 Bonus :**
- **Compression de contexte** (`ContextualCompressionRetriever`) ou *contextual chunk headers*.
- Mini-démo **GraphRAG** (notebook NirDiamant) sur un petit corpus.
- Lecture **self-RAG / CRAG** + idée d'auto-vérification de la réponse.

---

## 🗓️ Plan jour par jour

> IDs : `S5-J{jour}-T{tâche}`. Durées indicatives. 🧪 = code · 🎯 = contribue au livrable.

### J1 — Recherche hybride & baseline *(~4 h)*
- [ ] **S5-J1-T1** — 🧪 🎯 Créer le **jeu d'éval** (10–20 Q + réponses de référence) ⏱️ ~1 h 15
- [ ] **S5-J1-T2** — 🧪 🎯 Mesurer la **baseline S4** avec RAGAS (4 métriques) ⏱️ ~1 h
- [ ] **S5-J1-T3** — Lire le notebook **fusion_retrieval** (RRF) + `EnsembleRetriever` ⏱️ ~45 min
- [ ] **S5-J1-T4** — 🧪 🎯 Implémenter la **recherche hybride** (BM25 + dense, RRF) ⏱️ ~1 h

### J2 — Reranking *(~4 h)*
- [ ] **S5-J2-T1** — Lire **Cross-Encoders** (SBERT) : pourquoi plus précis ⏱️ ~45 min
- [ ] **S5-J2-T2** — 🧪 🎯 Brancher **`bge-reranker-v2-m3`** : *retrieve top-20 → rerank → top-5* ⏱️ ~1 h 45
- [ ] **S5-J2-T3** — 🧪 Comparer top-k **avec / sans** reranker sur 4-5 questions ⏱️ ~1 h
- [ ] **S5-J2-T4** — Noter quand le reranker **aide vs n'apporte rien** (recall haut/précision basse) ⏱️ ~30 min

### J3 — Transformations de requête *(~4 h)*
- [ ] **S5-J3-T1** — Lire/exécuter le notebook **HyDE** (NirDiamant) ⏱️ ~1 h
- [ ] **S5-J3-T2** — Survol **RAG-Fusion / multi-query / décomposition** (rag-from-scratch) ⏱️ ~1 h
- [ ] **S5-J3-T3** — 🧪 🎯 Implémenter **≥1 transformation** (HyDE **ou** RAG-Fusion) dans ton pipeline ⏱️ ~1 h 30
- [ ] **S5-J3-T4** — 🧪 Tester sur des questions « vagues » ou multi-parties ⏱️ ~30 min

### J4 — Compression & RAG avancé (survol) *(~4 h)*
- [ ] **S5-J4-T1** — 🧪 *(bonus)* Ajouter la **compression de contexte** ou des *chunk headers* ⏱️ ~1 h 15
- [ ] **S5-J4-T2** — Lire **Anthropic Contextual Retrieval** ⏱️ ~45 min
- [ ] **S5-J4-T3** — 🧪 🎯 Construire un Knowledge Graph basique et l'intégrer au RAG (GraphRAG) ⏱️ ~1 h 30
- [ ] **S5-J4-T4** — Survol **self-RAG / CRAG** (idée d'auto-correction) ⏱️ ~45 min

### J5 — Évaluation finale & finalisation *(~4 h)*
- [ ] **S5-J5-T1** — 🧪 🎯 Relancer **RAGAS** sur le pipeline amélioré ⏱️ ~1 h
- [ ] **S5-J5-T2** — 🧪 🎯 Construire le **tableau avant/après** (baseline → hybride → +rerank → +transfo) ⏱️ ~1 h
- [ ] **S5-J5-T3** — 🧪 Analyser : quelle amélioration a le plus payé ? ⏱️ ~45 min
- [ ] **S5-J5-T4** — 🧪 🎯 **README** (avec résultats) + **push GitHub** ⏱️ ~1 h 15

---

## ✅ Critères de réussite (validation de la semaine)

- [ ] Mon retrieval est **hybride** (BM25 + vecteurs, fusion RRF).
- [ ] J'ai ajouté un **reranker** (cross-encoder) et je vois son effet sur la précision.
- [ ] J'applique **≥1 transformation de requête** (HyDE ou RAG-Fusion).
- [ ] J'ai un **jeu d'éval RAGAS** et je mesure *faithfulness / context precision / recall* **avant/après**.
- [ ] Je peux **quantifier le gain** de chaque amélioration (tableau de résultats).
- [ ] Le code est **sur GitHub** avec un README incluant les **métriques**.
- [ ] Je peux **expliquer** : bi-encoder vs cross-encoder, pourquoi l'hybride, et quand le reranking aide (recall haut / précision basse).

> 🧭 **Auto-éval rapide :** un point bloque ? Note-le — le second brain en fera une tâche de rattrapage week-end.

---

## 🔜 Suite

➡️ **Partie 6 — Semaine 6 : Agents IA & orchestration** — fondamentaux des agents (**ReAct**, planning, tool use), **LangGraph**, **LlamaIndex**, multi-agents (**CrewAI / AutoGen**), mémoire d'agent. On passe du « récupérer/répondre » au « **raisonner et agir** » — ton RAG deviendra un **outil** appelé par un agent.

---

*Partie 5 d'un guide en 9 parties. Liens vérifiés en juin 2026 — RAGAS et les rerankers évoluent (API v0.2+, nouveaux modèles), revérifie le moment venu.*
