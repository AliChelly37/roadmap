---
title: AI Roadmap Assistant
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# AI Roadmap Assistant — Capstone (Semaine 8)

Projet de fin de la formation AI Engineering. Un agent conversationnel qui répond
aux questions sur le programme des 8 semaines, en s'appuyant sur le corpus réel de
la roadmap plutôt que sur ses connaissances propres.

## Architecture

| Couche | Choix |
|---|---|
| UI | Gradio (`gr.ChatInterface`, streaming) |
| Orchestration | LangGraph (agent ReAct avec outil) |
| Recherche | ChromaDB (dense) + BM25 (lexical), fusion RRF |
| Embeddings | `paraphrase-multilingual-MiniLM-L12-v2` |
| Gateway LLM | LiteLLM |
| Observabilité | Langfuse |
| Déploiement | Docker → Hugging Face Spaces |

Le corpus (`knowledge/`, 11 fichiers de la roadmap) est **indexé au build**, pas au
démarrage : le conteneur démarre à froid sans réencoder quoi que ce soit.

## Recherche hybride

Le dense seul ratait les termes techniques rares — « LangGraph », « reranking » —
parce qu'un modèle de paraphrase encode mal les noms propres. BM25 les retrouve
par correspondance lexicale exacte. Les deux classements sont fusionnés par
Reciprocal Rank Fusion (`k=60`), la formule reprise du `query_hybrid.py` de la
Semaine 5 — mais **rééquilibrée à 0.5 / 0.5**. Les poids d'origine (0.6 dense) avaient
été réglés sur un corpus PDF ; ici le dense ramène la table des matières pour toute
question contenant « semaine » ou « roadmap ». Un balayage montre un pic net à parts
égales (0.6/0.4 → 83 %, **0.5/0.5 → 100 %**, 0.4/0.6 → 92 %).

Mesure sur le jeu d'éval (`test_retrieval.py`, 8 questions couvrant les 8 semaines) :

| Pipeline | Recall@3 |
|---|---|
| Chunking naïf + modèle anglophone | 12 % |
| Modèle multilingue + chunk headers contextuels | 75 % |
| + hybride BM25/RRF + découpage ligne à ligne | **100 %** |

## Lancer en local

```bash
pip install -r requirements.txt
python app.py                 # http://localhost:7860
```

Renseigner les clés API dans un `.env` à la racine du dépôt (jamais commité).

## Lancer via Docker

```bash
docker build -t roadmap-assistant .
docker run -p 7860:7860 --env-file ../.env roadmap-assistant
```

Le build échoue volontairement si l'indexation produit 0 chunk ou si le recall
passe sous 85 % — on préfère casser le build que déployer un assistant muet.
Sortie de build attendue :

```
[7/9] RUN python -c "...index_roadmap_files()"   → 256 chunks indexés
[8/9] RUN python test_retrieval.py               → Recall@5 (production) : 100% (12/12)
```

**Image : 4,05 Go.** Elle faisait 10,6 Go avant qu'on installe torch depuis l'index
CPU : `sentence-transformers` tire `torch`, et la roue PyPI par défaut embarque toute
la pile CUDA (`nvidia-cudnn`, `cublas`, `triton`…) — ~6 Go de bibliothèques GPU
inutiles ici.

Le conteneur démarre sans réindexer (`Base déjà indexée avec 256 documents`) : l'index
est cuit dans l'image.

## Tests

```bash
python test_retrieval.py      # éval de retrieval, exit 1 si régression
```

Le jeu d'éval contient volontairement les requêtes **reformulées par l'agent**
(« reranking semaine 5 roadmap »), pas seulement des questions bien écrites : c'est
cette version honnête qui a révélé le défaut de pondération RRF.

## Statut du déploiement

**Pas de lien public — décision assumée.** Depuis 2026, créer un Space Gradio ou Docker
demande un plan payant (PRO pour un compte personnel) ; les comptes gratuits sont
limités à 2 Gradio Spaces sur ZeroGPU. Le livrable est donc une **application
conteneurisée vérifiée en local**, pas une démo hébergée.

Le dépôt reste néanmoins prêt à déployer : le frontmatter cible un **Docker Space**
(`sdk: docker`, `app_port: 7860`) et le `Dockerfile` respecte déjà les contraintes de
la plateforme. Il ne manque que le compte.

Points de conformité déjà en place dans le `Dockerfile` :

- conteneur lancé en **UID 1000** (`useradd -m -u 1000 user`, `USER user` avant les `COPY`)
- tous les `COPY` en `--chown=user`
- écoute sur le port `7860`, déclaré via `app_port`
- **aucune écriture disque nécessaire au runtime** : l'index vit dans l'image. Le disque
  d'un Space est effacé à chaque redémarrage, un index construit au démarrage serait
  reconstruit à chaque cold start.

Secrets à déclarer dans *Settings → Secrets* (injectés comme variables d'environnement
au runtime) : `OPENROUTER_API_KEY`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`,
`LANGFUSE_HOST`.

Pour repasser sur un Space Gradio natif (sans Docker), remplacer le frontmatter par
`sdk: gradio` / `app_file: app.py` et retirer `app_port` — HF installe alors
`requirements.txt` et lance `app.py`. L'index est reconstruit au premier démarrage
(~1–2 min), le `Dockerfile` restant utilisable en local.
