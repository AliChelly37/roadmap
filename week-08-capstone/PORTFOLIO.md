# AI Roadmap Assistant — writeup portfolio

> Capstone de la formation AI Engineering (8 semaines). Assistant conversationnel
> RAG interrogeant mes 30 mémos personnels de la formation.

## Le problème

Pendant 8 semaines de formation, j'ai écrit 30 mémos — un par notion travaillée.
C'est la trace de ce que j'ai réellement compris, mais retrouver « ce que j'avais
noté sur le reranking » demande de fouiller à la main. L'objectif : un assistant qui
interroge mes propres notes, répond en français uniquement à partir d'elles, et
indique de quelle semaine vient chaque réponse.

## L'architecture

```
Gradio ChatInterface  (UI, streaming)
        │
        ▼
LangGraph  StateGraph ─── agent ReAct, checkpointer par session
        │                 boucle : agent → outil → agent
        ▼
search_local_docs  (outil)
        │
        ├── dense  : ChromaDB + paraphrase-multilingual-MiniLM-L12-v2
        └── sparse : BM25Okapi
                 └── fusion RRF (k=60, 0.5 / 0.5) + plafond 2 chunks/fichier
        │
        ▼
LiteLLM / OpenRouter (llama-3.1-8b)  ── traces ──> Langfuse
```

Chaque brique vient d'une semaine : RAG (S4), hybride + RRF (S5), agent LangGraph
(S6), gateway et observabilité (S7).

## Ce que la mesure a révélé

Le pipeline « fonctionnait » — l'app démarrait, l'agent répondait — mais un jeu
d'éval de 12 questions couvrant les 8 semaines a montré qu'il ne récupérait
presque rien de pertinent. Quatre défauts distincts, trouvés en mesurant :

| Défaut | Symptôme | Correctif |
|---|---|---|
| Corpus hors du contexte Docker | `ROADMAP_ROOT` remontait 4 niveaux, vers le vault Obsidian. Des fichiers en local, **0 dans le conteneur** | Corpus vendu dans `knowledge/` |
| Modèle anglophone sur corpus français | `all-MiniLM-L6-v2`, choisi pour tenir dans les 512 Mo de Render | Modèle multilingue (16 Go dispo sur HF Spaces) |
| Contenu jeté au découpage | Titre et liste séparés d'un seul `\n` : `split("\n\n")` mettait les deux dans le même bloc, jeté avec le titre | Détection de titre ligne à ligne |
| Poids RRF inadaptés | 0.6 dense / 0.4 sparse (réglés en S5 sur un corpus PDF) : sur des notes courtes le dense dérive vers les mémos voisins | 0.5 / 0.5 après balayage |

**Recall@3 mesuré à chaque étape :**

| Pipeline | Recall@3 |
|---|---|
| Départ (dans un conteneur) | 0 % — index vide |
| Chunking naïf + modèle anglophone | 12 % |
| + modèle multilingue & chunk headers contextuels | 75 % |
| + hybride BM25/RRF | 75 % |
| + découpage ligne à ligne (contenu récupéré) | 100 % * |
| + requêtes bruitées de l'agent dans l'éval | 83 % |
| + rééquilibrage RRF 0.5/0.5 | **100 %** |

\* sur les questions « propres » uniquement. L'agent reformule en ajoutant des
méta-mots (« reranking cross-encoder **semaine 5 formation** ») qui matchent large :
ajouter ces requêtes réalistes à l'éval a fait retomber le score à 83 % et révélé
le défaut de pondération. **L'éval optimiste cachait un bug de production.**

## Ce que j'en retiens

- **Un pipeline qui répond n'est pas un pipeline qui marche.** L'app produisait des
  réponses plausibles avec un index vide en conteneur. Sans jeu d'éval, le bug
  partait en production.
- **Évaluer sur les requêtes réelles, pas sur les siennes.** Le gain le plus utile
  est venu de tester les reformulations de l'agent, pas mes questions bien écrites.
- **Les hyperparamètres ne se transposent pas.** Les poids RRF réglés en S5 sur des
  PDF étaient contre-productifs sur un corpus de notes personnelles.
- **Un garde-fou trop large est un bug.** Le filtre bloquait « system prompt » —
  soit le sujet même de la Semaine 2. Il faut cibler les tournures d'injection.

## Ce que le conteneur a attrapé et pas les tests locaux

Deux bugs n'existaient **que** dans l'image :

| Bug | Cause |
|---|---|
| `chromadb: Permission denied (os error 13)` | `WORKDIR $HOME/app` exécuté encore en root → dossier `root:root`, illisible en écriture après `USER user` |
| `ChatInterface.__init__() got an unexpected keyword argument 'type'` | `type="messages"` supprimé en Gradio 6. Les tests couvraient l'agent et le retrieval, jamais la construction de l'UI |

Le second est le plus instructif : une suite de tests qui n'importe jamais le point
d'entrée ne teste pas le point d'entrée.

**Taille d'image : 10,6 Go → 4,05 Go.** `sentence-transformers` tire `torch`, dont la
roue PyPI par défaut embarque toute la pile CUDA — ~6 Go de bibliothèques GPU sur un
déploiement CPU. Installer d'abord la roue CPU (191 Mo) les élimine entièrement.

**Vérification finale, contre le conteneur** (pas le code local) : question réelle →
réponse ancrée citant les bons outils ; tentative d'injection → bloquée par le garde-fou.

## Garde-fous en place

- Détection d'injection à l'entrée (OWASP LLM01), par motifs FR/EN, 6/6 sur le jeu de test
- Build qui échoue si l'indexation produit 0 chunk ou si le recall passe sous 85 %
- Thread LangGraph par session — un Space public ne doit pas partager la mémoire
  de conversation entre visiteurs
- Traces Langfuse via callback handler, branchées sur le chemin réellement exécuté

## Limites connues

- Pas de reranker cross-encoder dans le capstone (présent en S5) : coût mémoire
  sur le free tier CPU
- Corpus figé à l'image : ajouter un mémo demande un rebuild
- Les mémos vivent aussi dans le vault Obsidian — les deux copies peuvent diverger
- Modèle 8B — suffisant pour de la synthèse ancrée, limité en raisonnement multi-étapes
