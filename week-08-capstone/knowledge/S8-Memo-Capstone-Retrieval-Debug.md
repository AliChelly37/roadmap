# 📝 Mémo S8 : Déboguer un RAG qui « marche » — capstone & déploiement

*Ce document couvre les tâches `S8-J3-T2`, `S8-J4-T2`, `S8-J4-T3` et alimente `S8-J5-T2`.*

> ⚠️ **Explain-back non fait.** Conformément à `learning-system.md` (étape 4), ce mémo
> ne compte comme « appris » qu'après une reformulation orale/écrite sans notes.
> À faire à la prochaine session — voir les flashcards en fin de document.

---

## 1. Le piège central : un pipeline qui répond n'est pas un pipeline qui marche

Le capstone démarrait, l'agent appelait bien son outil, l'UI streamait des réponses
plausibles en français. **Et l'index était vide dans le conteneur.**

La cause : dans [core/rag.py](../../week-08-capstone/core/rag.py),
le corpus était résolu par remontée de chemin relatif :

```python
ROADMAP_ROOT = Path(__file__).resolve().parent.parent.parent.parent
```

Quatre `.parent` depuis `week-08-capstone/core/` mènent à `.raw/ai-engineering/` —
c'est-à-dire **le vault Obsidian, hors du dépôt git**. En local : 15 fichiers trouvés,
tout fonctionne. Dans Docker, le contexte de build s'arrête à `week-08-capstone/` :
0 fichier, 0 chunk, un assistant qui invente.

**Leçon** : un chemin qui sort du dépôt est un bug de déploiement en attente. Le
corpus doit vivre dans le contexte de build (`knowledge/`).

---

## 2. Les trois autres défauts, trouvés en mesurant

| Défaut | Pourquoi c'est faux | Correctif |
|---|---|---|
| `all-MiniLM-L6-v2` sur corpus **français** | Modèle anglophone, choisi pour tenir dans les 512 Mo de Render | `paraphrase-multilingual-MiniLM-L12-v2` (HF Spaces = 16 Go) |
| `split("\n\n")` pour détecter les titres | Un titre et sa liste ne sont séparés que d'un `\n` → les deux dans le même bloc → **contenu jeté avec le titre** | Détection ligne à ligne |
| Poids RRF 0.6 dense / 0.4 sparse | Réglés en S5 sur un corpus **PDF**. Ici le dense ramène la table des matières pour toute question | 0.5 / 0.5 |

Le deuxième est le plus vicieux : `05-semaine-5.md` faisait 9 769 caractères mais ne
produisait que ~5 900 caractères de chunks. **40 % du corpus disparaissait
silencieusement.** Aucune erreur, aucun log — juste des réponses moins bonnes.

---

## 3. L'éval optimiste cache les bugs de production

Premier jeu d'éval : 8 questions bien écrites (« Comment fonctionne le reranking ? »)
→ **100 % de recall@3**. Pipeline déclaré bon.

Sauf que l'agent ne pose pas ces questions-là. Il reformule :

```
[OUTIL] Recherche RAG pour : 'reranking semaine 5 AI Engineering Roadmap'
```

Les méta-mots (« semaine », « roadmap », « formation ») matchent surtout `roadmap_0.md`,
la table des matières. En ajoutant 4 requêtes de ce type au jeu d'éval : **83 %**,
sous le seuil, CI rouge. C'est ce test honnête qui a révélé le défaut de pondération RRF.

**Leçon** : le jeu d'éval doit contenir les requêtes que le *système* génère, pas
seulement celles que l'humain écrit.

### Diagnostic : regarder les deux classements séparément

| Rang | Dense | BM25 |
|---|---|---|
| 1 | `roadmap_0.md` (TdM) | **`05-semaine-5 > Reranking (J2)`** (7.90) |
| 2 | `roadmap_0.md` | `02-semaine-2 > Prompt engineering` |
| 3 | `roadmap_0.md` | `05-semaine-5 > Projet` |

BM25 avait raison depuis le début. Avec un poids dense de 0.6, `0.6/(60+1)` >
`0.4/(60+1)` : **tous** les résultats dense empoisonnés passaient devant le bon
résultat BM25. Le balayage des poids montre un pic net et unimodal :

| dense / sparse | recall@3 |
|---|---|
| 0.6 / 0.4 | 83 % |
| **0.5 / 0.5** | **100 %** |
| 0.4 / 0.6 | 92 % |
| 0.3 / 0.7 | 92 % |

### Corollaire : mesurer la configuration qui part en production

Deuxième piège du même genre, trouvé en retirant les 2 fichiers de théorie des jeux
du corpus. Le recall est tombé de 100 % à 92 %… mais uniquement dans l'éval, qui
mesurait à `k=3`. **L'outil de l'agent, lui, appelle `search_roadmap(query, n_results=5)`.**
À k=5 : toujours 100 %.

On notait donc une configuration qui n'existe nulle part. Correctif : une constante
unique `DEFAULT_N_RESULTS` lue **à la fois** par l'outil et par l'éval — impossible
qu'elles divergent. L'éval affiche les deux (k=5 = production, k=3 = signal strict
d'alerte précoce).

À noter aussi : retirer 2 fichiers d'un corpus **change les scores BM25 des autres**
(l'IDF dépend du corpus entier). Un corpus modifié impose de reprendre la mesure.

---

## 4. Garde-fou trop large = bug, pas sécurité

Le filtre d'injection bloquait la sous-chaîne `"system prompt"`. Or le prompt
engineering **est le sujet de la Semaine 2** : « Explique-moi le system prompt de la
semaine 2 » était refusé. Idem pour `"hack"`.

Correctif : cibler les **tournures impératives** d'injection, pas les mots-clés
thématiques — `ignore (all) previous instructions`, `oublie tes instructions`,
`tu es maintenant un…`, `reveal your prompt`. 6/6 sur le jeu de test, faux positifs
éliminés.

---

## 5. Déploiement : ce que disent vraiment les docs HF Spaces

- **Docker Spaces exigent désormais un plan payant** (PRO pour un compte perso).
  Les comptes gratuits sont limités à 2 Gradio Spaces sur ZeroGPU.
- Conteneur lancé en **UID 1000** → `useradd -m -u 1000 user`, puis `USER user`
  **avant** tout `COPY --chown=user`.
- Frontmatter requis : `sdk: docker` + `app_port: 7860`.
- Secrets : injectés comme variables d'environnement **au runtime**. Au *buildtime*
  il faut un montage explicite (`--mount=type=secret`).
- **Le disque est perdu à chaque redémarrage.** D'où le choix d'indexer au *build* :
  l'index vit dans une couche de l'image, pas sur le disque éphémère. Bonus : plus de
  pic mémoire au démarrage — la cause des OOM sur Render.

---

## 6. Concurrence : un `thread_id` constant sur un Space public

```python
config = {"configurable": {"thread_id": "gradio_thread"}}   # ❌
```

Avec un checkpointer `MemorySaver`, ce `thread_id` codé en dur fait **partager la
mémoire de conversation entre tous les visiteurs** du Space. Correctif : dériver le
thread de la session Gradio (`request.session_hash`).

---

---

## 7. Le conteneur attrape ce que les tests locaux ratent

Deux bugs de cette session n'existaient **que** dans le conteneur, et aucun test local
ne les voyait :

1. `chromadb.errors.InternalError: Permission denied` — `WORKDIR $HOME/app` exécuté
   alors qu'on est encore `root` crée le dossier en `root:root`. Après `USER user`,
   chromadb ne peut plus y écrire. Correctif : `mkdir` + `chown` explicites **avant**
   de descendre en privilèges.
2. `ChatInterface.__init__() got an unexpected keyword argument 'type'` — l'argument
   `type="messages"` a disparu en Gradio 6 (le format messages est devenu le défaut).
   Les tests portaient sur l'agent et le retrieval, jamais sur la construction de l'UI :
   personne ne lançait `app.py`.

**Leçon** : « ça tourne en local » ne dit rien sur les permissions, l'utilisateur
d'exécution ni les versions résolues dans l'image. Et un test qui n'importe jamais le
point d'entrée ne teste pas le point d'entrée.

### Corollaire coût : la roue torch par défaut embarque CUDA

`sentence-transformers` tire `torch`, et la roue PyPI standard inclut toute la pile
GPU (`nvidia-cudnn`, `cublas`, `triton`…) : **~6 Go inutiles sur un déploiement CPU**.
Installer d'abord la roue CPU (`--index-url https://download.pytorch.org/whl/cpu`,
191 Mo) élimine la totalité de ces paquets.

---

## Flashcards (Anki / Active Recall)

#flashcard
Q: Pourquoi un chemin de corpus construit avec plusieurs `.parent` est-il un bug de déploiement en attente ?
A: Parce qu'il peut pointer hors du dépôt. En local le dossier existe et tout marche ; dans le conteneur, le contexte de build s'arrête à la racine du projet, le chemin ne résout rien et l'index est vide — sans lever d'erreur.

#flashcard
Q: Pourquoi un `split("\n\n")` peut-il faire disparaître silencieusement 40 % d'un corpus markdown ?
A: Si un titre et sa liste ne sont séparés que d'un seul `\n`, ils forment un même bloc. Un chunker qui teste `block.startswith("#")` prend tout le bloc pour un titre et jette le contenu avec lui. Il faut détecter les titres ligne à ligne.

#flashcard
Q: Un jeu d'éval RAG à 100 % de recall peut-il masquer un bug de production ? Comment ?
A: Oui. Si l'éval ne contient que des questions bien formulées par un humain alors qu'en production c'est l'agent qui reformule (en ajoutant des méta-mots), on mesure un cas qui ne se produit jamais. Il faut inclure les requêtes réellement émises par le système.

#flashcard
Q: Ton éval RAG mesure recall@3, ton agent appelle l'outil avec n_results=5. Où est le problème ?
A: Tu notes une configuration qui ne part jamais en production — trop sévère ici, mais ce serait pire dans l'autre sens (éval à k=5, prod à k=3 = faux vert). Il faut que l'outil et l'éval lisent la même constante, et mesurer d'abord la valeur de production.

#flashcard
Q: Pourquoi retirer des fichiers d'un corpus peut-il dégrader le retrieval sur les fichiers restants ?
A: Parce que BM25 pondère par IDF, qui se calcule sur l'ensemble du corpus. Retirer des documents change la rareté de chaque terme, donc les scores et le classement de tous les autres. Toute modification du corpus impose de relancer l'éval.

#flashcard
Q: Pourquoi des poids RRF réglés sur un corpus ne se transposent-ils pas à un autre ?
A: Les poids encodent la fiabilité relative du dense et du lexical *pour ce corpus*. Sur des PDF de prose, le dense est fiable (0.6). Sur un curriculum plein de noms propres techniques et de méta-documents, le dense ramène la table des matières et BM25 est plus fiable — l'optimum retombe à 0.5/0.5.

#flashcard
Q: Pourquoi un filtre d'injection basé sur des mots-clés est-il un mauvais garde-fou ?
A: Parce qu'il refuse le sujet légitime. Bloquer « system prompt » interdit toute question sur la Semaine 2 (prompt engineering). Il faut détecter des tournures impératives de détournement, pas des mots thématiques.

#flashcard
Q: Pourquoi un `WORKDIR` placé avant `USER user` casse-t-il une app qui écrit sur disque ?
A: Le dossier est créé par l'utilisateur courant du build — root — donc en `root:root`. Une fois passé en `user`, l'app ne peut plus y écrire (Permission denied, os error 13). Il faut `mkdir` + `chown` explicitement avant de descendre en privilèges.

#flashcard
Q: Pourquoi `pip install sentence-transformers` peut-il ajouter ~6 Go à une image CPU ?
A: Il tire `torch`, et la roue PyPI par défaut embarque toute la pile CUDA (nvidia-cudnn, cublas, triton…), inutile sans GPU. Installer d'abord la roue CPU depuis `download.pytorch.org/whl/cpu` (~190 Mo) évite ces paquets.

#flashcard
Q: Pourquoi indexer au build d'une image Docker plutôt qu'au démarrage de l'app ?
A: Le disque d'un Space est perdu à chaque redémarrage, donc un index construit au runtime est refait à chaque cold start : latence + pic mémoire (cause classique d'OOM). Construit au build, il vit dans une couche de l'image, immuable et instantanée.

#flashcard
Q: Quel risque fait courir un `thread_id` codé en dur avec un checkpointer LangGraph sur une app publique ?
A: Tous les utilisateurs partagent le même fil de conversation : chacun voit et pollue la mémoire des autres. Il faut dériver le thread de la session (ex. `request.session_hash`).

## Links
- [[S5-J1-Memo-Hybrid-Ragas]]
- [[S5-J2-Memo-Reranking]]
- [[S7-Memo-Observability-Langfuse]]
- [[S7-Memo-Security-Guardrails]]
- [[LLMOps]]
- [[RAG]]
