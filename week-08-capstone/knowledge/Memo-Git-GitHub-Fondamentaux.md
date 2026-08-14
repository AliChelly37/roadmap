# 📝 Mémo : Git & GitHub — Fondamentaux

*Synthèse du tutoriel vidéo sur Git et GitHub (Sumit Saha).*

---

## 1. Git vs GitHub

*   **Git** : outil de contrôle de version qui s'exécute **localement** sur ta machine. Il enregistre en continu qui a changé quoi, quand et où, sur n'importe quel type de fichier (code, image, vidéo…). Créé par **Linus Torvalds** (également créateur de Linux).
*   **GitHub** : plateforme **cloud** qui héberge des dépôts Git et permet la collaboration à distance. Racheté par Microsoft. Concurrents : GitLab, Bitbucket.
*   **Analogie** : Git est le café, GitHub est le café où ce café est servi. Les deux sont liés mais ne sont pas la même chose.

---

## 2. Architecture : Local vs Remote

Le flux de travail Git repose sur 4 zones successives :

1.  **Working Directory** : le dossier de travail où tu écris/modifies tes fichiers.
2.  **Staging Area (index)** : zone intermédiaire où tu prépares les changements avant de les valider (`git add`). Sert de point de contrôle, comme se regarder dans le miroir avant de sortir.
3.  **Local Repository** : historique versionné stocké sur ta machine (`git commit`). Toutes les métadonnées sont stockées dans le dossier caché `.git` (créé par `git init`).
4.  **Remote Repository** : copie cloud du dépôt (ex. GitHub), utilisée pour partager, sauvegarder et collaborer (`git push`).

Un dépôt peut être créé de deux façons : `git init` (localement) ou `git clone <url>` (en copiant un dépôt distant existant).

---

## 3. Installation & Configuration

*   Vérifier l'installation : `git --version`
*   Config obligatoire à la première utilisation :
    ```bash
    git config --global user.email "email@exemple.com"
    git config --global user.name "Nom Prénom"
    ```
*   `--global` : s'applique à toute la machine. `--local` : s'applique uniquement au dépôt courant.

---

## 4. Cycle de base : add → commit

*   `git status` : affiche l'état des fichiers (modifiés, non suivis, en attente).
*   Variantes de `git add` :
    | Commande | Portée |
    |---|---|
    | `git add -A` / `git add --all` | Tout le projet, y compris suppressions |
    | `git add .` | Dossier courant + sous-dossiers (sans les suppressions) |
    | `git add *` | Fichiers visibles du dossier courant, **sans** les suppressions ni sous-dossiers |
    | `git add fichier.txt` | Un fichier précis |
*   `git commit -m "message"` : sauvegarde définitivement les fichiers stagés dans le dépôt local.
*   `git reset` : dé-stage les changements et les remet dans le working directory (ne restaure pas les fichiers supprimés).
*   `git reset --hard` : annule tout, y compris les fichiers supprimés manuellement.
*   `git reset HEAD~` : annule le dernier commit et remet son contenu dans le working directory.

---

## 5. Suppression de fichiers

*   `git rm fichier.txt` : supprime le fichier **et** stage la suppression en une seule commande (refuse si le fichier a des modifications non commitées).
*   `git rm -f fichier.txt` : force la suppression malgré des modifications locales.
*   `git rm --cached fichier.txt` : retire le fichier du staging mais le garde physiquement dans le working directory (passe en "untracked").
*   `git rm -r dossier/` : suppression récursive (dossier + contenu).

---

## 6. Historique des commits

*   `git log` : historique complet avec ID de commit, auteur, message.
*   `git log --oneline` : version compacte, un commit par ligne (ID raccourci).
*   `git checkout <commit_id>` : revient à l'état exact d'un commit passé → mode **"HEAD detached"**. Nécessite que tous les changements courants soient commités.
*   `git checkout main` : retour à la version la plus récente de la branche.
*   `git diff <commit_récent> <commit_ancien>` : montre les différences (ajouts en vert, suppressions en rouge). L'ordre des IDs détermine la perspective de comparaison.

---

## 7. Branching (branches)

*   **Concept** : une branche est une ligne de développement indépendante, créée à partir de l'état courant de la branche active.
*   **Analogie** : la branche `main` est la cuisine principale d'un restaurant ; une nouvelle branche est une "cuisine de test" pour expérimenter sans risquer de perturber le service principal.
*   Commandes :
    ```bash
    git branch                # liste les branches
    git branch <nom>          # crée une branche
    git checkout <nom>        # bascule sur une branche
    git merge <nom>           # fusionne <nom> dans la branche courante
    ```
*   **Merge conflict** : survient quand la même portion d'un fichier a été modifiée différemment dans deux branches. Git insère des marqueurs de conflit dans le fichier ; il faut choisir/fusionner manuellement les versions, puis `git add` + `git commit` pour valider la résolution.

---

## 8. Rebase

*   `git rebase main` (depuis une branche `feature`) : rejoue les commits de `feature` par-dessus les derniers commits de `main`, au lieu de créer un commit de fusion.
*   **Différence avec merge** : le rebase produit un historique **linéaire** et plus propre ; le merge crée un commit de fusion supplémentaire.
*   ⚠️ **Danger** : le rebase **réécrit l'historique** (les IDs de commit changent). À éviter sur des branches partagées/publiques sans prévenir l'équipe — sinon les collaborateurs ne pourront plus synchroniser normalement.

---

## 9. Restore & Stash

*   `git restore fichier.txt` : annule les changements non commités d'un fichier, retour au dernier commit.
*   `git restore .` : restaure tout le dépôt à l'état du dernier commit.
*   `git restore --staged fichier.txt` : retire un fichier du staging sans toucher au working directory.
*   `git stash` : met de côté temporairement les changements non commités (utile pour changer de branche sans perdre son travail en cours).
*   `git stash pop` : réapplique le stash le plus récent **et le supprime** de la liste.
*   `git stash apply` : réapplique le stash **sans le supprimer** de la liste (réutilisable).
*   `git stash list` / `git stash drop` : lister / supprimer manuellement un stash.

---

## 10. Revert vs Reset

*   `git revert <commit_id>` : crée un **nouveau commit** qui annule les effets d'un commit passé, sans supprimer l'historique. Idéal en équipe/remote car tout reste traçable.
*   `git reset` : ramène le dépôt à un commit antérieur en **supprimant** les commits suivants de l'historique (aucune trace après un `git log`).
*   **Analogie revert** : comme corriger un plat trop salé en ajustant plutôt qu'en le jetant.

---

## 11. Push, Fetch, Pull

*   `git push origin <branche>` : envoie les commits locaux vers le dépôt distant.
*   `git fetch` : télécharge les changements distants **sans** les fusionner dans le working directory.
*   `git pull` = `git fetch` + `git merge` : télécharge **et** fusionne automatiquement.

---

## 12. Pull Request (PR)

*   Une **pull request** est une demande de fusion d'une branche vers une autre (généralement `main`), avec revue de code avant validation.
*   Workflow GitHub : onglet *Pull Requests* → *New pull request* → choisir la branche **base** (destination) et la branche **compare** (source) → titre + description → *Create pull request* → revue (onglets Conversation / Commits / Files changed) → *Merge pull request*.
*   Permet de garder `main` stable tout en collaborant en sécurité.

---

## Flashcards (Anki / Active Recall)

#flashcard
Q: Quelle est la différence fondamentale entre Git et GitHub ?
A: Git est un outil de contrôle de version qui s'exécute localement ; GitHub est une plateforme cloud qui héberge des dépôts Git et permet la collaboration à distance.

#flashcard
Q: Quelles sont les 4 zones successives du workflow Git ?
A: Working Directory → Staging Area (index) → Local Repository → Remote Repository.

#flashcard
Q: Quelle est la différence entre `git add -A`, `git add .` et `git add *` ?
A: `-A`/`--all` stage tout le projet y compris les suppressions ; `.` stage le dossier courant et ses sous-dossiers sans les suppressions ; `*` stage les fichiers visibles du dossier courant seulement, sans suppressions ni sous-dossiers.

#flashcard
Q: Que fait `git rm --cached fichier.txt` par rapport à `git rm -f fichier.txt` ?
A: `--cached` retire le fichier du staging mais le garde physiquement dans le working directory ; `-f` le supprime réellement malgré des modifications locales non commitées.

#flashcard
Q: Quelle est la différence entre `git stash pop` et `git stash apply` ?
A: `pop` réapplique le stash le plus récent et le supprime de la liste ; `apply` le réapplique mais le conserve dans la liste pour réutilisation future.

#flashcard
Q: Quelle est la différence entre `git revert` et `git reset` ?
A: `git revert` crée un nouveau commit qui annule un commit passé sans supprimer l'historique ; `git reset` ramène le dépôt à un commit antérieur en supprimant les commits suivants de l'historique.

#flashcard
Q: Pourquoi `git rebase` est-il déconseillé sur une branche partagée/publique ?
A: Parce qu'il réécrit l'historique des commits (les IDs changent), ce qui empêche les collaborateurs travaillant sur la même branche de synchroniser normalement leurs copies locales.

#flashcard
Q: Que fait exactement `git pull` par rapport à `git fetch` ?
A: `git fetch` télécharge les changements distants sans les fusionner dans le working directory ; `git pull` fait `fetch` + `merge` en une seule commande.

#flashcard
Q: Qu'est-ce qu'un merge conflict et comment se résout-il ?
A: Il survient quand la même portion d'un fichier a été modifiée différemment dans deux branches ; Git insère des marqueurs de conflit dans le fichier, et il faut choisir/fusionner manuellement les versions puis committer la résolution.

#flashcard
Q: À quoi sert une Pull Request sur GitHub ?
A: À demander la fusion d'une branche (compare) vers une autre (base, souvent main), en permettant une revue de code avant validation, ce qui garde la branche principale stable.
