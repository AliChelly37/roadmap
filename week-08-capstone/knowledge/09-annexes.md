# 📎 Annexes — Bibliothèque, repos, cheat sheets & glossaire

**📍 Partie 9 / 9** · Référence transverse à garder ouverte pendant tout le parcours.
**Contenu :** [A. Ressources gratuites](#a--bibliothèque-de-ressources-gratuites) · [B. Repos GitHub](#b--répertoire-des-repos-github) · [C. Cheat sheets](#c--cheat-sheets--outils) · [D. Glossaire](#d--glossaire) · [E. Pour aller plus loin](#e--pour-aller-plus-loin)

> Tous les liens vérifiés en **juin 2026**. L'écosystème IA bouge vite : revérifie quotas, versions et classements le moment venu.

---

## A — Bibliothèque de ressources gratuites

### 📄 Cours & parcours
- **Hugging Face — LLM Course** — `huggingface.co/learn/llm-course`
- **Hugging Face — AI Agents Course** (avec certificat) — `huggingface.co/learn/agents-course`
- **Hugging Face — MCP Course** — `huggingface.co/learn`
- **DeepLearning.AI — Short Courses** (7 cours gratuits couvrant toute la stack GenAI) — `deeplearning.ai/courses`
- **LangChain Academy — Intro to LangGraph** — `academy.langchain.com`
- **Kaggle × Google — 5-Day Gen AI Intensive** (self-paced) — `kaggle.com/learn-guide/5-day-genai`
- **Kaggle × Google — 5-Day AI Agents Intensive** (self-paced) — `kaggle.com/learn-guide/5-day-agents`
- **Maxime Labonne — LLM Course** — `github.com/mlabonne/llm-course`
- **MIT 6.S191 — Intro to Deep Learning** (mis à jour chaque année) — `introtodeeplearning.com`
- **fast.ai — Practical Deep Learning** (+ livre gratuit en notebooks) — `course.fast.ai`

### 🎥 Vidéos & chaînes YouTube
- **Andrej Karpathy** (Intro to LLMs, Deep Dive, Let's build GPT) — `youtube.com/@AndrejKarpathy`
- **3Blue1Brown** (transformers, attention, embeddings, visuels) — `youtube.com/@3blue1brown`
- **Sebastian Raschka**, **Sam Witteveen**, **James Briggs / Aurelio AI**, **Umar Jamil**, **Cameron R. Wolfe**, **AssemblyAI**, **DeepLearning.AI**

### 📖 Docs officielles
- **Anthropic** — `platform.claude.com/docs` · **OpenAI** — `developers.openai.com/api/docs` · **Google Gemini** — `ai.google.dev`
- **LangChain** — `docs.langchain.com` · **LangGraph** — `docs.langchain.com/langgraph` · **LlamaIndex** — `docs.llamaindex.ai`
- **Sentence-Transformers** — `sbert.net` · **Pydantic** — `docs.pydantic.dev` · **FastAPI** — `fastapi.tiangolo.com`
- **Chroma** — `docs.trychroma.com` · **Qdrant** — `qdrant.tech/documentation` · **Ollama** — `ollama.com`
- **MCP** — `modelcontextprotocol.io` · **Docker** — `docs.docker.com` · **HF Spaces** — `huggingface.co/docs/hub/spaces`

### 📚 Livres & code gratuits
- **Sebastian Raschka — « Build a LLM (From Scratch) »** → **code gratuit** + guides : `github.com/rasbt/LLMs-from-scratch` (hub : `sebastianraschka.com/llms-from-scratch`)
- **Vicki Boykis — « What are embeddings »** (PDF gratuit) — `vickiboykis.com/what_are_embeddings`
- **Jay Alammar & M. Grootendorst — « Hands-On LLMs »** → **notebooks gratuits** : `github.com/HandsOnLLM/Hands-On-Large-Language-Models`
- **Jay Alammar — The Illustrated Transformer** (article) — `jalammar.github.io/illustrated-transformer/`
- *(notables, payants)* Chip Huyen — *AI Engineering* (O'Reilly) ; Bouchard & Peters — *Building LLMs for Production*

### 🛠️ Playgrounds & outils interactifs
- **Tiktokenizer** (tokenisation) — `tiktokenizer.vercel.app`
- **Google AI Studio** (tester Gemini) — `aistudio.google.com`
- **Anthropic Console / Workbench** — `console.anthropic.com`
- **MTEB Leaderboard** (choisir un modèle d'embedding) — `huggingface.co/spaces/mteb/leaderboard`
- **LMArena** (comparer des modèles, classement par votes) — `lmarena.ai`
- **Artificial Analysis** (benchmarks vitesse/coût/qualité) — `artificialanalysis.ai`

### 📰 Newsletters
- **TLDR AI** (quotidien, technique, dense) — `tldr.tech/ai`
- **The Batch** (DeepLearning.AI, hebdo, cadrage recherche) — `deeplearning.ai/the-batch`
- **Latent Space** (swyx — *l'ingénierie IA* comme discipline) — `latent.space`
- **Ahead of AI** (Sebastian Raschka — architectures LLM en profondeur) — `magazine.sebastianraschka.com`
- **Import AI** (Jack Clark, co-fondateur Anthropic — recherche + politique) — `importai.net`
- **Interconnects** (Nathan Lambert — post-training, RLHF)

### 🎓 Certifications gratuites
- **Certificats Hugging Face** (LLM Course, Agents Course, MCP)
- **Kaggle × Google** (5-Day Gen AI & 5-Day Agents — badge à la complétion)
- **DeepLearning.AI Short Courses** (attestations)

---

## B — Répertoire des repos GitHub

### Fondamentaux, cours & cookbooks
- `rasbt/LLMs-from-scratch` — construire un LLM de zéro (PyTorch)
- `mlabonne/llm-course` — parcours + notebooks
- `HandsOnLLM/Hands-On-Large-Language-Models` — notebooks du livre
- `anthropics/courses` — prompting, *prompt evaluations*, tool use
- `anthropics/anthropic-cookbook` · `openai/openai-cookbook` — recettes

### LLM, structured outputs & tool use
- `instructor-ai/instructor` — sorties structurées multi-providers
- `ollama/ollama` — modèles en local
- `cheahjs/free-llm-api-resources` — **liste à jour des APIs LLM gratuites**

### Embeddings & bases vectorielles
- `UKPLab/sentence-transformers` · `FlagOpen/FlagEmbedding` (BGE + rerankers)
- `chroma-core/chroma` · `qdrant/qdrant` · `pgvector/pgvector` · `facebookresearch/faiss`
- `embeddings-benchmark/mteb` — benchmark MTEB

### RAG
- `NirDiamant/RAG_Techniques` — **un notebook par technique** (HyDE, fusion, GraphRAG…)
- `langchain-ai/rag-from-scratch` — RAG pas-à-pas
- `docling-project/docling` — parsing structure-aware · `Unstructured-IO/unstructured`
- `explodinggradients/ragas` — évaluation RAG · `microsoft/graphrag`
- `dorianbrown/rank_bm25` — BM25 (recherche hybride)

### Agents & orchestration
- `NirDiamant/GenAI_Agents` — **50+ tutos** (LangGraph, MCP, multi-agents)
- `NirDiamant/agents-towards-production` — patterns de production
- `huggingface/agents-course` · `langchain-ai/langgraph` · `crewAIInc/crewAI`

### LLMOps, production & garde-fous
- `langfuse/langfuse` · `Arize-ai/phoenix` — observabilité/tracing
- `BerriAI/litellm` — gateway (routing, fallbacks, cache, coûts)
- `protectai/llm-guard` · `guardrails-ai/guardrails` · `NVIDIA-NeMo/Guardrails` · `microsoft/presidio` — garde-fous
- `promptfoo/promptfoo` — évals & red-teaming en CI

### Déploiement & UI
- `gradio-app/gradio` — démos ML · `Chainlit/chainlit` — UI de chat pour agents
- `SYSTRAN/faster-whisper` — STT local

---

## C — Cheat sheets & outils

### 🎓 APIs LLM gratuites (pour rester à 0 €)
| Fournisseur | Modèles | Quota gratuit (ordre de grandeur) | Carte requise |
|---|---|---|---|
| **Google AI Studio** | Gemini 2.5 Flash / Pro | ~1 500 req/jour, contexte 1M | ❌ Non |
| **Groq** | Llama, Qwen, **Whisper** | jusqu'à ~14 400 req/jour (petits modèles) | ❌ Non |
| **OpenRouter** | 28+ modèles `:free` | variable selon modèle | ❌ Non |
| **Cerebras** | Llama, Qwen | ~1M tokens/jour | ❌ Non |
| **Ollama** | local (Llama, Qwen, Mistral…) | illimité (ta machine) | ❌ Non |
| OpenAI / Anthropic | GPT / Claude | — (API payante, chat gratuit) | ✅ Oui |

### 🗄️ Bases vectorielles
| Outil | Idéal pour | Déploiement |
|---|---|---|
| **Chroma** | prototypage, démarrage rapide | local / embedded |
| **Qdrant** | production, filtrage avancé | Docker / cloud |
| **pgvector** | déjà sur PostgreSQL | extension PG |
| **FAISS** | comprendre l'ANN bas niveau | librairie |

### 🤖 Frameworks d'agents
| Framework | Force | Quand l'utiliser |
|---|---|---|
| **LangGraph** | contrôle fin (machine à états) | agents complexes, prod |
| **CrewAI** | multi-agents par rôles | prototypes multi-agents |
| **LlamaIndex** | *RAG-first* | agents sur tes données |
| **Pydantic AI** | type-safe | apps robustes |
| **smolagents** (HF) | minimal, *code-driven* | démarrage léger |

### 🔭 Observabilité / LLMOps
| Outil | Force | Gratuit |
|---|---|---|
| **Langfuse** | open-source, self-host, agnostique | MIT + free tier |
| **Phoenix** (Arize) | éval RAG, OpenTelemetry | open-source |
| **LangSmith** | natif LangChain/LangGraph, LangGraph Studio | free dev tier |
| **LiteLLM** | gateway : routing/fallbacks/cache/coûts | open-source |

### 💚 Le « stack 0 € » recommandé (récap du parcours)
| Couche | Choix gratuit |
|---|---|
| **LLM** | Gemini (AI Studio) · Groq · Ollama (local) |
| **Embeddings** | `sentence-transformers` — `bge-m3` (multilingue/FR) |
| **Vector DB** | Chroma (proto) → Qdrant (prod) |
| **Frameworks** | LangChain · LangGraph · LlamaIndex |
| **Parsing** | PyMuPDF → Docling |
| **RAG avancé** | rank_bm25 · `bge-reranker-v2-m3` · RAGAS |
| **Agents** | LangGraph · CrewAI · MCP |
| **Éval** | promptfoo · RAGAS |
| **Observabilité** | Langfuse |
| **Gateway** | LiteLLM |
| **Garde-fous** | LLM Guard · Presidio · OpenAI Moderation |
| **UI** | Chainlit · Gradio |
| **Déploiement** | Docker · Hugging Face Spaces |

---

## D — Glossaire

> Définitions courtes des termes du parcours.

- **Token** — unité de texte traitée par le LLM (≈ ¾ de mot) ; le coût se compte en tokens.
- **Tokenisation** — découpe du texte en tokens (souvent BPE).
- **Fenêtre de contexte** — nb max de tokens (entrée + sortie) qu'un modèle gère d'un coup.
- **Température** — contrôle l'aléa de génération (0 = déterministe, élevé = créatif).
- **Embedding** — vecteur dense capturant le *sens* ; proximité = similarité sémantique.
- **Similarité cosinus** — mesure d'angle entre 2 vecteurs (métrique de proximité la plus courante).
- **ANN** (*Approximate Nearest Neighbor*) — recherche de voisins approchée, rapide (vs exacte).
- **HNSW** — index ANN à base de graphe hiérarchique (rapide, bon recall).
- **Structured output** — sortie LLM contrainte à un schéma (JSON validé, ex. Pydantic).
- **Function calling / Tool use** — le modèle décide d'appeler un outil ; toi tu l'exécutes et renvoies le résultat.
- **RAG** (*Retrieval-Augmented Generation*) — récupérer du contexte pertinent puis générer une réponse ancrée.
- **Chunking** — découpe des documents en passages avant indexation.
- **Base vectorielle** — stockage/recherche de vecteurs (Chroma, Qdrant, pgvector…).
- **BM25** — score de pertinence lexicale (mots-clés).
- **Recherche hybride** — combine BM25 (lexical) + dense (sémantique).
- **RRF** (*Reciprocal Rank Fusion*) — fusionne plusieurs classements en un seul.
- **Reranking** — réordonner le top-k avec un *cross-encoder* (précis mais coûteux).
- **Bi-encoder vs cross-encoder** — embeddings rapides (retrieval) vs scoring précis (reranking).
- **HyDE** — générer un document hypothétique pour améliorer le retrieval.
- **RAGAS** — framework d'éval RAG (faithfulness, answer relevancy, context precision/recall).
- **Agent** — LLM + boucle (raisonner→agir→observer) + outils + mémoire.
- **ReAct** — *Reason + Act* : alterner raisonnement et actions.
- **Workflow vs agent** — chemins orchestrés/figés vs autonomie décisionnelle.
- **Multi-agents** — plusieurs agents à rôles qui collaborent (supervisor, handoffs).
- **MCP** (*Model Context Protocol*) — standard ouvert pour connecter outils/données aux agents.
- **Checkpointer** — mécanisme de mémoire d'état (LangGraph).
- **Observabilité / Tracing** — visualiser chaque appel (LLM, retrieval, outil), latence, coût.
- **Caching sémantique** — réutiliser une réponse en cache pour une requête *similaire*.
- **Gateway** — proxy unifiant plusieurs fournisseurs (routing, fallbacks, coûts) — ex. LiteLLM.
- **Garde-fou (guardrail)** — contrôle entrée/sortie (PII, injection, modération, schéma).
- **Prompt injection** — *directe* (l'utilisateur) ou *indirecte* (instructions cachées dans un doc récupéré).
- **PII** — données personnelles identifiables (à détecter/masquer).
- **OWASP LLM Top 10** — liste de référence des risques de sécurité des apps LLM.
- **Fine-tuning** — ré-entraîner un modèle sur tes données (LoRA/QLoRA = méthodes légères).
- **vLLM** — moteur d'inférence haute performance pour servir des modèles open.

---

## E — Pour aller plus loin

### 💡 Idées de projets portfolio
**Accessibles (consolider S1–S4) :**
- *Doc Q&A* (RAG) sur tes propres PDFs avec citations.
- *Moteur de recherche sémantique* sur un corpus (notes, articles).
- *Extracteur de données structurées* (offres d'emploi, factures, articles → JSON).

**Intermédiaires (S5–S6) :**
- *Agent de recherche* (web + ton RAG) qui rédige une synthèse sourcée.
- *Système multi-agents* (researcher → writer → reviewer) qui produit un mini-rapport.
- *Q&A sur une codebase* (la doc d'une librairie open-source).

**Avancés (S7–S8) :**
- *RAG agentique* déployé, **instrumenté** (tracing + garde-fous + évals en CI).
- *Assistant multimodal* (voix via Whisper, ou vision).
- *Assistant vertical* (santé/juridique/finance) avec garde-fous + tracing, **déployé**.

### 🎯 Te spécialiser
Choisis **une verticale** (santé, finance, juridique, code, support client…) et construis 1-2 projets ciblés : c'est ce qui te démarque sur le marché.

### 🔬 Approfondir techniquement
- **Fine-tuning** : LoRA/QLoRA avec **Unsloth** ou **Axolotl** (gratuit, Colab).
- **Serving** : **vLLM** pour héberger tes propres modèles open.
- **Évaluation avancée** : evals custom, **red-teaming** (Garak, PyRIT).
- **Comprendre le moteur** : `rasbt/LLMs-from-scratch` (construire un LLM de zéro).

### 👥 Communautés
- **r/LocalLLaMA** (Reddit) — modèles open, le plus actif côté pratique.
- **Hugging Face Discord** · **LangChain Discord** · **Latent Space Discord**.
- **r/MachineLearning** · **Kaggle** (compétitions, notebooks).

### 🔄 Rester à jour
- 1 newsletter **quotidienne** (TLDR AI) + 1 **hebdo** de fond (The Batch, Latent Space ou Ahead of AI).
- Suis le **MTEB Leaderboard** et **LMArena** pour les modèles ; **cheahjs/free-llm-api-resources** pour les APIs gratuites.
- Construis **en public** et **contribue** à un repo open-source que tu utilises.

---

## 🎓 Fin du guide

Tu as désormais le parcours **complet** : **Partie 0** (mode d'emploi) + **8 semaines** (S1→S8) + ces **annexes**.

**Rappel du fil rouge :** chaque semaine produit **1 livrable** qui alimente la suivante — APIs → apps → recherche vectorielle → RAG → RAG avancé → agents → production → **capstone déployé**. À la fin : un **portfolio d'ingénieur IA**, pas seulement des notes de cours.

**Pour ton second brain :** toutes les parties partagent le même format (objectifs · concepts · ressources · repos · livrable · plan jour-par-jour avec IDs `Sx-Jy-Tz` · critères de réussite) et le **prompt de génération de tâches** est en Partie 0.

Bonne route, et surtout : **construis**. 🚀

---

*Partie 9 (Annexes) d'un guide en 9 parties. Liens vérifiés en juin 2026 — quotas, versions et classements évoluent vite, revérifie régulièrement (notamment via `cheahjs/free-llm-api-resources` et le MTEB Leaderboard).*
