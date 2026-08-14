# 🔎 Semaine 3 — Embeddings & recherche vectorielle

**📍 Partie 3 / 9** · Phase : 🔎 *Données & RAG* · Charge : **~20 h** (5 jours × ~4 h)
**🎯 Livrable de la semaine :** un **moteur de recherche sémantique** sur ton propre corpus — la première brique du RAG (S4–S5).

> 🔄 **Refresh éclair (si un prérequis est fragile) :**
> - **NumPy** (vecteurs, opérations) → cherche « numpy quickstart » ⏱️ ~15 min
> - **Similarité cosinus** (intuition + formule) ⏱️ ~10 min
> - **Docker** (lancer un conteneur) — utile pour Qdrant en J5 → cherche « docker run getting started » ⏱️ ~15 min

---

## 🎯 Objectifs

À la fin de la semaine, tu sais :
- Expliquer **ce qu'est un embedding** et comment il encode le *sens* dans un espace vectoriel.
- **Générer des embeddings** en local et gratuitement (sentence-transformers) + via une API d'embedding.
- **Choisir un modèle** via le leaderboard **MTEB** (et pourquoi prendre un modèle **multilingue** pour du français).
- Comprendre les **métriques de similarité** (cosinus, L2, produit scalaire) et l'**indexation ANN** (HNSW, IVF, flat).
- **Stocker et requêter** des vecteurs dans une base vectorielle (**Chroma**, puis un aperçu de **Qdrant**).
- Assembler un **moteur de recherche sémantique** : requête en langage naturel → top-k passages pertinents.

---

## 🧩 Concepts clés

- **Embedding** : vecteur dense qui capture le sens ; proximité = similarité sémantique
- **Dimensionnalité** (384, 768, 1024, 1536…) et **normalisation** des vecteurs
- **Métriques** : **cosinus** (la plus courante), **distance euclidienne (L2)**, **produit scalaire (dot)**
- **Recherche exacte (flat/brute force)** vs **ANN** (approchée, rapide)
- **Index** : **HNSW** (graphe « petit monde » hiérarchique) · **IVF** (clusters) · compromis **recall / vitesse / mémoire**
- **Modèles** : *encoder* (BERT-like) vs *LLM-backbone* ; **multilingue** ; benchmark **MTEB**
- **Base vectorielle** : collection, `upsert`, `query`, **filtrage par metadata**, **persistance**
- **Chunking** (découpe des documents) — survol ici, détaillé en **S4**

---

## 📚 Ressources gratuites

> 📄 cours · 📖 doc · 🎥 vidéo · 📝 article · 💻 repo · 🛠️ playground · 🎓 API gratuite | 🟢 fonda. · 🟡 inter. · 🔴 avancé · ⭐ incontournable

### Théorie & intuition (J1–J2)
- 📝 ⭐ **Vicki Boykis — « What are embeddings »** (mini-livre gratuit, PDF) 🟡 ⏱️ ~2 h — `vickiboykis.com/what_are_embeddings`
- 📄 ⭐ **Pinecone — Learn** : *vector embeddings*, *semantic search*, *HNSW*, *ANN* 🟡 — `pinecone.io/learn`
- 📄 **Cohere — LLM University** : modules *Embeddings* & *Semantic Search* 🟢 — `cohere.com/llmu`
- 🎥 *(optionnel)* **3Blue1Brown** — segment sur les *word embeddings* (dans la série Transformers) 🟢

### Modèles d'embeddings (J1, J4)
- 📖 ⭐ **Sentence-Transformers (SBERT)** — la lib de référence (gratuite, locale) 🟡 — `sbert.net`
- 🛠️ ⭐ **MTEB Leaderboard** — pour choisir/compare un modèle 🟡 — `huggingface.co/spaces/mteb/leaderboard`
- 📖 **Modèles gratuits recommandés** :
  - *Starter (rapide, 384-dim)* : `all-MiniLM-L6-v2` · `all-mpnet-base-v2`
  - *Multilingue (idéal pour le FR)* : `BAAI/bge-m3` · `Alibaba-NLP/gte-multilingual-base` · `intfloat/multilingual-e5-large` · `nomic-ai/nomic-embed-text-v2`
  - ⚠️ Les classements bougent vite — vérifie **MTEB** avant de figer ton choix.
- 🎓 **API d'embeddings gratuites** : **Google Gemini embeddings** (free tier) · **Nomic** (API gratuite) · **Cohere** (essai gratuit)

### Bases vectorielles (J3, J5)
- 📖 ⭐ **Chroma — Getting Started** (le plus simple pour démarrer) 🟢 — `docs.trychroma.com` (et `github.com/chroma-core/chroma`)
- 📖 ⭐ **Qdrant — Quickstart** + *« What is a vector database »* 🟡 — `qdrant.tech/documentation` (et `github.com/qdrant/qdrant`)
- 📖 **pgvector — README** (extension PostgreSQL, HNSW + IVFFlat) 🟡 — `github.com/pgvector/pgvector`
- 💻 *(optionnel 🔴)* **FAISS** — comprendre l'ANN au niveau « librairie » 🔴 — `github.com/facebookresearch/faiss`

### Indexation / ANN (J2)
- 📝 ⭐ **Pinecone — HNSW & ANN explained** 🟡 — section *Learn* de `pinecone.io/learn`
- 📝 **Qdrant — articles** : HNSW, quantization 🟡 — `qdrant.tech/articles`

---

## 💻 Repos GitHub (à lire / forker)

- 💻 ⭐ **`UKPLab/sentence-transformers`** — génération d'embeddings (exemples)
- 💻 ⭐ **`chroma-core/chroma`** — base vectorielle pour prototyper
- 💻 **`qdrant/qdrant`** — base vectorielle de production (Docker)
- 💻 **`pgvector/pgvector`** — vecteurs dans PostgreSQL
- 💻 **`embeddings-benchmark/mteb`** — le benchmark MTEB (code + tâches)
- 💻 *(optionnel)* **`facebookresearch/faiss`** — ANN bas niveau

---

## 🛠️ Projet / Livrable : « Moteur de recherche sémantique »

🎯 Construis un moteur qui répond à une requête en langage naturel par les **passages les plus proches sémantiquement** dans ton corpus.

**Cahier des charges (Definition of Done) :**
1. **Corpus** — rassemble **100–500 passages** (tes notes, des articles, la doc d'une lib, un export Wikipédia…). Découpe-les en passages courts (chunking simple pour l'instant).
2. **Embeddings (local, gratuit)** — encode tout le corpus avec **sentence-transformers** (commence par `all-MiniLM-L6-v2`).
3. **Stockage** — indexe dans **Chroma** (`PersistentClient`) avec des **metadata** (source, titre, date…). Les données **survivent au redémarrage**.
4. **Recherche** — `search(query, k=5)` renvoie le **top-k** avec **scores de similarité**, exposé en **CLI** *ou* via un endpoint **FastAPI** `GET /search?q=...` (réutilise la S2).
5. **Comparaison de modèles** — refais l'index avec **≥1 modèle multilingue** (ex. `bge-m3`) et compare la pertinence sur 3-4 requêtes (surtout en français).
6. **Repo** — `ai-engineer-roadmap/week-03-semantic-search/`, `.env` non commité, **README** (corpus, modèle, lancement, exemples de requêtes).

**🌟 Bonus :**
- Indexe les **mêmes données dans Qdrant** (Docker) et compare vitesse/résultats.
- Ajoute du **filtrage par metadata** (ex. limiter à une source ou une période).
- Mesure le **temps de requête** flat vs HNSW sur ton corpus.

---

## 🗓️ Plan jour par jour

> IDs : `S3-J{jour}-T{tâche}`. Durées indicatives. 🧪 = code · 🎯 = contribue au livrable.

### J1 — Embeddings : intuition & génération *(~4 h)*
- [x] **S3-J1-T1** — Lire **« What are embeddings »** (Vicki Boykis), parties 1–3 ⏱️ ~1 h 15
- [x] **S3-J1-T2** — Parcourir **Pinecone Learn** : *vector embeddings* + *semantic search* ⏱️ ~45 min
- [x] **S3-J1-T3** — 🧪 Installer **sentence-transformers**, encoder 5-10 phrases, **afficher les vecteurs** ⏱️ ~1 h
- [x] **S3-J1-T4** — 🧪 Calculer la **similarité cosinus** entre paires de phrases et vérifier que « proche = même sens » ⏱️ ~1 h

### J2 — Similarité & indexation (ANN) *(~4 h)*
- [x] **S3-J2-T1** — Lire **HNSW / ANN** sur Pinecone Learn (graphe, recall vs vitesse) ⏱️ ~1 h
- [x] **S3-J2-T2** — Comparer **cosinus / L2 / dot** : quand chacun, effet de la normalisation ⏱️ ~45 min
- [ ] **S3-J2-T3** — 🧪 *(optionnel 🔴)* Mini-démo **FAISS** : index flat vs HNSW sur 1000 vecteurs ⏱️ ~1 h 15
- [x] **S3-J2-T4** — Ouvrir le **MTEB Leaderboard**, repérer 2-3 modèles multilingues candidats ⏱️ ~1 h

### J3 — Base vectorielle : Chroma *(~4 h)*
- [x] **S3-J3-T1** — Lire le **Getting Started de Chroma** ⏱️ ~45 min
- [x] **S3-J3-T2** — 🧪 🎯 `PersistentClient`, créer une collection, **`add`** quelques documents + metadata ⏱️ ~1 h 15
- [x] **S3-J3-T3** — 🧪 🎯 **`query`** par texte, lire les distances/scores, tester `where` (metadata) ⏱️ ~1 h
- [x] **S3-J3-T4** — 🧪 Vérifier la **persistance** (relancer le script, données toujours là) ⏱️ ~1 h

### J4 — Construire le moteur sur un vrai corpus *(~4 h)*
- [x] **S3-J4-T1** — 🧪 🎯 Charger ton **corpus** (100–500 passages), chunking simple ⏱️ ~1 h
- [x] **S3-J4-T2** — 🧪 🎯 Encoder tout le corpus + **indexer** dans Chroma ⏱️ ~1 h
- [x] **S3-J4-T3** — 🧪 🎯 Écrire `search(query, k)` (top-k + scores), tester 4-5 requêtes ⏱️ ~1 h
- [x] **S3-J4-T4** — 🧪 🎯 Réindexer avec un **modèle multilingue** et **comparer** la pertinence (FR) ⏱️ ~1 h

### J5 — Qdrant (aperçu) & finalisation *(~4 h)*
- [x] **S3-J5-T1** — 🧪 Lancer **Qdrant via Docker** (ports 6333/6334), lire le Quickstart ⏱️ ~1 h
- [x] **S3-J5-T2** — 🧪 *(bonus)* Réindexer le corpus dans Qdrant + **filtrage par metadata** ⏱️ ~1 h
- [x] **S3-J5-T3** — 🧪 🎯 Exposer la recherche en **CLI ou FastAPI** `GET /search` ⏱️ ~1 h
- [x] **S3-J5-T4** — 🧪 🎯 **README** + **push GitHub** ⏱️ ~1 h

---

## ✅ Critères de réussite (validation de la semaine)

- [ ] Je **génère des embeddings en local** (sentence-transformers) sans aucun coût.
- [ ] Je sais **choisir un modèle via MTEB** et pourquoi un modèle multilingue convient mieux au français.
- [ ] Mon moteur renvoie un **top-k pertinent** avec **scores de similarité**.
- [ ] Les données sont **persistées** et je sais **filtrer par metadata**.
- [ ] J'ai **comparé ≥2 modèles** d'embeddings sur des requêtes réelles.
- [ ] Le code est **sur GitHub** avec un README clair.
- [ ] Je peux **expliquer** : cosinus vs L2, HNSW vs flat, et le compromis recall / vitesse / mémoire.

> 🧭 **Auto-éval rapide :** un point bloque ? Note-le — le second brain en fera une tâche de rattrapage week-end.

---

## 🔜 Suite

➡️ **Partie 4 — Semaine 4 : RAG (systèmes de base)** — architecture RAG, parsing de documents, **stratégies de chunking**, pipeline de retrieval, augmentation du prompt + **citations**. Tu transformeras ce moteur de recherche en un vrai **« chat with your docs »**.

---

*Partie 3 d'un guide en 9 parties. Liens vérifiés en juin 2026 — le classement des modèles d'embeddings évolue vite, reverifie MTEB le moment venu.*
