# 🔎 Week 3 — Moteur de Recherche Sémantique local (Second Brain)

Ce projet implémente un moteur de recherche sémantique complet s'exécutant entièrement en local sur vos notes Obsidian (votre "Second Brain"). Il permet de retrouver des passages d'informations par pertinence sémantique (conceptuelle) plutôt que par simple recherche textuelle exacte (lexicale).

---

## 🚀 Fonctionnalités
1.  **Indexation de documents locaux** : Scan récursif et découpage intelligent de vos fichiers Markdown en morceaux (chunks) avec un recouvrement de contexte (overlap) pour éviter les coupures abruptes de phrases.
2.  **Support Multi-Modèles** :
    *   **MiniLM-L6-v2** (384 dimensions) : Modèle ultra-léger optimisé pour l'anglais.
    *   **Multilingual-E5-Base** (768 dimensions) : Modèle haut de gamme optimisé pour la recherche multilingue (notamment en français).
3.  **Bases de Données Vectorielles (Chroma DB & Qdrant)** :
    *   **Chroma DB** : Fonctionne en local *in-process* (sauvegarde persistante sur disque).
    *   **Qdrant** : Fonctionne dans un conteneur **Docker** avec filtrage avancé des métadonnées (payload queries).
4.  **Interface Graphique Premium (FastAPI)** : Un serveur web FastAPI servant une interface utilisateur sombre, interactive et glassmorphic pour effectuer vos requêtes visuellement.

---

## 🛠️ Installation & Démarrage

### 1. Prérequis
Assurez-vous que votre environnement virtuel `.venv` est activé et contient les dépendances requises :
```bash
pip install sentence-transformers chromadb qdrant-client uvicorn fastapi
```

Pour utiliser Qdrant, lancez Docker Desktop et démarrez le conteneur officiel :
```bash
docker run -d --name qdrant_dev -p 6333:6333 -p 6334:6334 -v qdrant_storage:/qdrant/storage qdrant/qdrant
```

---

## 📖 Utilisation

### Mode 1 : Chroma DB (Client local persistant)

*   **Indexation (Modèle Anglais léger)** :
    ```bash
    python build_search_index.py
    ```
*   **Indexation (Modèle Multilingue E5 - Recommandé)** :
    ```bash
    python build_search_index_multilingual.py
    ```
*   **Recherche sémantique en ligne de commande** :
    ```bash
    python query_search_multilingual.py "Pourquoi les bases SQL traditionnelles échouent"
    ```

---

### Mode 2 : Qdrant (Conteneur Docker avec filtres)

*   **Indexation dans Qdrant** :
    ```bash
    python build_qdrant_index.py
    ```
*   **Recherche Qdrant avec filtrage optionnel de métadonnées** :
    ```bash
    # Syntaxe : python query_qdrant.py "votre requête" "filtre de source (chemin du fichier)"
    python query_qdrant.py "System 1 vs System 2" "memos"
    ```

---

### Mode 3 : Interface Web Interactive (FastAPI)

Lancez le serveur d'application local :
```bash
python -m uvicorn main:app --reload --port 8000
```

Ouvrez ensuite votre navigateur sur **[http://127.0.0.1:8000](http://127.0.0.1:8000)** pour accéder à l'interface de recherche sémantique. Elle vous permet de :
*   Saisir vos requêtes en langage naturel.
*   Choisir dynamiquement entre le modèle anglais léger et le modèle multilingue.
*   Ajuster le nombre de résultats (K) renvoyés à l'aide d'un curseur.
*   Lire les passages correspondants indentés, avec leurs fichiers sources et leurs scores de distance sémantique.
