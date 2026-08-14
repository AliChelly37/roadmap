# 📚 Semaine 4 — RAG (systèmes de base)

**📍 Partie 4 / 9** · Phase : 🔎 *Données & RAG* · Charge : **~20 h** (5 jours × ~4 h)
**🎯 Livrable de la semaine :** un **« Chat with your docs »** — un RAG qui répond à des questions sur **tes propres PDFs**, avec **citations** des sources.

> 🔄 **Refresh éclair (si un prérequis est fragile) :**
> - Tu **réutilises ton moteur de recherche S3** (Chroma + embeddings) : garde-le ouvert, on le complète.
> - Tu **réutilises le streaming FastAPI S2** pour l'UI de réponse.
> - **PDF = format pénible** : prévois que le parsing « rate » parfois (tableaux, colonnes) — c'est normal, on gère.

---

## 🎯 Objectifs

À la fin de la semaine, tu sais :
- Décrire l'**architecture RAG complète** : ingestion → indexation → retrieval → augmentation → génération.
- **Parser des documents réels** (PDF, DOCX) en texte propre et exploitable.
- Choisir et appliquer une **stratégie de chunking** adaptée au contenu.
- Construire un **pipeline RAG de base** qui produit des réponses **ancrées** (grounded) avec **citations**.
- Reconnaître et limiter les **pièges** : hallucination sans grounding, **injection indirecte** via les documents récupérés.

---

## 🧩 Concepts clés

- **Les 2 phases du RAG** : *indexation* (hors-ligne : charger → découper → embarquer → stocker) et *requête* (en ligne : retrouver → augmenter → générer)
- **Parsing de documents** : PDF (PyMuPDF, Docling), DOCX, HTML ; texte natif vs **OCR** (scans)
- **Chunking** : *fixed-size*, **recursive** (le cheval de bataille), *token-based*, *semantic*, *document-aware*, *parent/child* (sentence-window) ; rôle du **`chunk_size`** et du **`chunk_overlap`**
- **Retrieval** : top-k, seuils de score, garde « je ne sais pas »
- **Augmentation** : injecter le contexte dans le prompt avec des **délimiteurs** (balises XML), instruire le modèle
- **Génération ancrée + citations** : renvoyer fichier/page de chaque source
- **Sécurité** : ⚠️ **injection indirecte** — un document récupéré peut contenir des « instructions » ; traiter le contexte **comme des données**, jamais comme des ordres
- **Frameworks** : **LangChain** vs **LlamaIndex** (ou *from scratch* pour comprendre)

---

## 📚 Ressources gratuites

> 📄 cours · 📖 doc · 🎥 vidéo · 📝 article · 💻 repo | 🟢 fonda. · 🟡 inter. · 🔴 avancé · ⭐ incontournable

### Fondamentaux RAG (J1, J3)
- 📄 ⭐ **LangChain — Build a RAG app/agent** (tutoriel officiel pas-à-pas) 🟡 — `docs.langchain.com/oss/python/langchain/rag`
- 📄 ⭐ **LlamaIndex — Starter tutorial / RAG** 🟡 — `docs.llamaindex.ai`
- 🎥 ⭐ **« RAG from scratch »** (série LangChain, notebooks) 🟡 — repo `langchain-ai/rag-from-scratch`
- 📝 **What is RAG** (vue d'ensemble) 🟢 — section *Learn* de `pinecone.io/learn` et `ibm.com/think` (tutoriels RAG)

### Parsing de documents (J1)
- 📖 ⭐ **PyMuPDF / `pymupdf4llm`** — rapide & léger, idéal PDF texte 🟢 — `github.com/pymupdf/PyMuPDF`
- 📖 ⭐ **Docling** (IBM, MIT) — *structure-aware*, excellent sur PDF complexes/scientifiques, `DoclingLoader` pour LangChain 🟡 — `github.com/docling-project/docling`
- 📖 **Unstructured** — 25+ formats, sortie « éléments typés » (Title/Table/…) 🟡 — `github.com/Unstructured-IO/unstructured`
- 📖 *(optionnel, API managée gratuite)* **LlamaParse** — vision, tableaux complexes (free tier) 🟡 — `cloud.llamaindex.ai`

### Chunking (J2)
- 📖 ⭐ **LangChain — Text Splitters** (`RecursiveCharacterTextSplitter`, etc.) 🟡 — `docs.langchain.com` (→ *Text splitters*)
- 📝 ⭐ **Chunking strategies** (guides comparés) 🟡 — Weaviate (`weaviate.io/blog/chunking-strategies-for-rag`) & Pinecone Learn
- 💻 **`chonkie`** — librairie de chunking légère et dédiée 🟢 — `chonkie.ai`
- 🎥 *(optionnel)* **Greg Kamradt — « 5 Levels of Text Splitting »** (notebook — cherche le titre) 🟡

### Citations & sécurité (J4)
- 📖 ⭐ **Anthropic — Citations** (renvoyer des sources vérifiables) 🟡 — `platform.claude.com/docs` (→ *Build with Claude* → *Citations*)
- 📝 **Anthropic — Contextual Retrieval** (technique avancée, *preview* pour la S5) 🔴 — `anthropic.com/news/contextual-retrieval`

---

## 💻 Repos GitHub (à lire / forker)

- 💻 ⭐ **`langchain-ai/langchain`** + **`langchain-ai/rag-from-scratch`** — RAG pas-à-pas
- 💻 ⭐ **`run-llama/llama_index`** — RAG « batteries incluses »
- 💻 ⭐ **`docling-project/docling`** — parsing structure-aware
- 💻 **`pymupdf/PyMuPDF`** — extraction PDF rapide
- 💻 **`Unstructured-IO/unstructured`** — ingestion multi-formats
- 💻 *(réf. S3)* **`chroma-core/chroma`** — stockage des chunks embarqués

---

## 🛠️ Projet / Livrable : « Chat with your docs »

🎯 Transforme ton moteur de recherche S3 en **assistant qui répond sur tes PDFs**, sources à l'appui.

**Cahier des charges (Definition of Done) :**
1. **Ingestion** — charge **3 à 10 PDFs à toi** et parse-les en texte propre (**PyMuPDF** d'abord ; **Docling** si tableaux/colonnes).
2. **Chunking** — découpe avec `RecursiveCharacterTextSplitter` (départ : `chunk_size=1000`, `chunk_overlap=200`) et attache des **metadata** (fichier source + **n° de page**).
3. **Indexation** — embarque (modèle S3) + stocke dans **Chroma** (persistant).
4. **Pipeline de requête** — `ask(question)` : **retrieve top-k** → construit un prompt avec le contexte entre **balises XML** (en instruisant le modèle de **traiter le contexte comme des données**) → le LLM **génère une réponse ancrée**.
5. **Citations** — chaque réponse **cite ses sources** (fichier + page) à partir des metadata des chunks récupérés.
6. **UI** — expose `POST /ask` en **streaming** (réutilise la S2) ou une CLI.
7. **Repo** — `ai-engineer-roadmap/week-04-rag-chat-docs/`, `.env` non commité, **README** (PDFs d'exemple, lancement, exemples de Q/R).

**🌟 Bonus :**
- Garde **« je ne sais pas »** quand aucun chunk pertinent (scores trop bas) — réduit les hallucinations.
- Compare **2 stratégies de chunking** (ou 2 `chunk_size`) sur les mêmes questions.
- Compare **Docling vs PyMuPDF** sur un PDF à tableaux.

---

## 🗓️ Plan jour par jour

> IDs : `S4-J{jour}-T{tâche}`. Durées indicatives. 🧪 = code · 🎯 = contribue au livrable.

### J1 — Architecture RAG & parsing PDF *(~4 h)*
- [x] **S4-J1-T1** — Lire le **tutoriel RAG LangChain** (les 2 phases, schéma mental) ⏱️ ~1 h
- [x] **S4-J1-T2** — Survol **What is RAG** (Pinecone/IBM) pour fixer le vocabulaire ⏱️ ~30 min
- [x] **S4-J1-T3** — 🧪 🎯 Parser **1-2 PDFs** avec PyMuPDF, inspecter le texte extrait ⏱️ ~1 h 30
- [x] **S4-J1-T4** — 🧪 Tester **Docling** sur un PDF « difficile » (tableaux/colonnes) et comparer ⏱️ ~1 h

### J2 — Stratégies de chunking *(~4 h)*
- [x] **S4-J2-T1** — Lire **Text Splitters** (LangChain) + un guide chunking (Weaviate) ⏱️ ~1 h
- [x] **S4-J2-T2** — 🧪 🎯 Découper le corpus avec `RecursiveCharacterTextSplitter` + **metadata (source, page)** ⏱️ ~1 h 30
- [x] **S4-J2-T3** — 🧪 Visualiser quelques chunks : sont-ils cohérents ? ajuster `chunk_size`/`overlap` ⏱️ ~1 h
- [x] **S4-J2-T4** — 🧪 Indexer les chunks dans **Chroma** (réutilise S3) ⏱️ ~30 min

### J3 — Retrieval & génération ancrée *(~4 h)*
- [x] **S4-J3-T1** — 🧪 🎯 `retrieve(question, k)` → récupérer top-k chunks + metadata ⏱️ ~1 h
- [x] **S4-J3-T2** — 🧪 🎯 Construire le **prompt augmenté** (contexte entre balises XML, instruction « contexte = données ») ⏱️ ~1 h 30
- [x] **S4-J3-T3** — 🧪 🎯 Brancher le **LLM** : générer une réponse **uniquement** à partir du contexte ⏱️ ~1 h
- [x] **S4-J3-T4** — 🧪 Tester 4-5 questions, repérer les réponses inventées (manque de grounding) ⏱️ ~30 min

### J4 — Citations, streaming & sécurité *(~4 h)*
- [x] **S4-J4-T1** — Lire **Anthropic Citations** (principe) ⏱️ ~30 min
- [x] **S4-J4-T2** — 🧪 🎯 Ajouter les **citations** (fichier + page) à chaque réponse ⏱️ ~1 h 15
- [x] **S4-J4-T3** — 🧪 🎯 Exposer `POST /ask` en **streaming** (ou CLI) ⏱️ ~1 h 15
- [x] **S4-J4-T4** — 🧪 Tester la **défense contre l'injection indirecte** (un chunk contenant « ignore les instructions ») ⏱️ ~1 h

### J5 — Robustesse & finalisation *(~4 h)*
- [x] **S4-J5-T1** — 🧪 🎯 Ajouter la garde **« je ne sais pas »** (seuil de score) ⏱️ ~1 h
- [ ] **S4-J5-T2** — 🧪 *(bonus)* Comparer **2 chunkings** ou **Docling vs PyMuPDF** sur les mêmes questions ⏱️ ~1 h
- [x] **S4-J5-T3** — 🧪 Nettoyer le pipeline (fonctions claires, gestion d'erreurs) ⏱️ ~1 h
- [x] **S4-J5-T4** — 🧪 🎯 **README** + **push GitHub** ⏱️ ~1 h

---

## ✅ Critères de réussite (validation de la semaine)

- [ ] Je **parse mes propres PDFs** en texte propre (et je sais quand passer de PyMuPDF à Docling).
- [ ] J'applique un **chunking avec metadata** (source + page).
- [ ] Mon RAG répond **en s'appuyant sur le contexte récupéré** (réponses ancrées, pas inventées).
- [ ] Chaque réponse **cite ses sources** (fichier + page).
- [ ] Le modèle **traite le contexte comme des données** (défense de base contre l'injection indirecte).
- [ ] Le code est **sur GitHub** avec un README clair.
- [ ] Je peux **expliquer** : les 2 phases du RAG, et l'effet de `chunk_size` / `chunk_overlap` sur la qualité.

> 🧭 **Auto-éval rapide :** un point bloque ? Note-le — le second brain en fera une tâche de rattrapage week-end.

---

## 🔜 Suite

➡️ **Partie 5 — Semaine 5 : RAG avancé & évaluation** — recherche **hybride** (BM25 + vecteurs), **reranking**, transformations de requête (**HyDE**, **RAG-Fusion**, décomposition, routing), compression de contexte, aperçu **GraphRAG / self-RAG**, et **évaluation** rigoureuse (RAGAS). Tu **muscleras** le RAG de cette semaine et mesureras les gains.

---

*Partie 4 d'un guide en 9 parties. Liens vérifiés en juin 2026 — l'écosystème parsing/chunking évolue vite (Docling, LlamaParse…), revérifie les outils le moment venu.*
