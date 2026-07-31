# Week 4 — Chat with your Docs (RAG de base)

Ce projet implémente un pipeline **RAG (Retrieval-Augmented Generation)** de base, s'exécutant sur vos propres documents PDF locaux avec un ancrage strict et des citations de sources vérifiables.

---

## Fonctionnalités
1.  **Ingestion & Inscription** : Lecture des PDFs page par page avec **PyMuPDF** (`fitz`).
2.  **Chunking récursif intelligent** : Découpage récursif par caractères (`RecursiveCharacterTextSplitter`) avec conservation de l'en-tête, du nom de fichier (`source`) et du numéro de page précis (`page`) propagés dans les métadonnées de chaque morceau.
3.  **Stockage Vectoriel** : Stockage et calcul des similarités sémantiques dans **Chroma DB** en utilisant le modèle multilingue d'embeddings `intfloat/multilingual-e5-base`.
4.  **Prompt augmenté XML & Grounding** : Le contexte de recherche est structuré entre des balises XML `<context>` dans le prompt du LLM. Le modèle est configuré à une température de `0.0` pour éliminer les hallucinations.
5.  **Citations dynamiques** : Le LLM insère de manière automatique des citations inline du type `[nom_du_fichier.pdf, Page X]` à l'emplacement exact de chaque affirmation.
6.  **Sécurité (Garde de Score & Injection)** :
    *   *Garde de score* : Si le morceau le plus proche a une distance > `0.22`, le script bypasse l'appel au LLM et répond directement *"Je ne sais pas."* (évite les frais API et les hors-sujets).
    *   *Défense anti-injection* : Instruction stricte empêchant le LLM d'exécuter des ordres indirects insérés dans le texte des PDFs.
7.  **Interface Graphique en Streaming** : Un serveur web **FastAPI** servant une interface sombre glassmorphic interactive qui affiche le stream de la réponse et les cartes des documents consultés en direct.

---

## Installation & Démarrage

### 1. Variables d'environnement
Créez ou vérifiez que votre fichier `.env` à la racine de la roadmap contient vos clés API :
```env
GEMINI_API_KEY=votre_cle_gemini
```

### 2. Générer le document d'exemple
Pour tester l'ingestion sur un PDF multi-page, créez le document d'exemple sur les Systèmes Multi-Agents :
```bash
python generate_test_pdf.py
```

### 3. Lancer l'indexation
Découpez et stockez le PDF dans Chroma :
```bash
python chunk_and_index.py
```

---

## Utilisation

### Mode 1 : Ligne de commande (CLI)
Posez vos questions directement depuis le terminal :
```bash
# Question dans le contexte
python query_rag.py "Qu'est-ce que le protocole Raft et quels sont ses états ?"

# Question hors-contexte (déclenche le blocage automatique)
python query_rag.py "Quelle est la capitale de la France ?"
```

### Mode 2 : Test de sécurité (Indirect Injection)
Vérifiez que le système est immunisé contre les prompt injections indirectes cachées dans les PDFs :
```bash
python test_injection.py
```

### Mode 3 : Interface Web FastAPI (Streaming)
Démarrez le serveur FastAPI local :
```bash
python -m uvicorn main:app --reload --port 8000
```
Ouvrez ensuite votre navigateur sur **[http://127.0.0.1:8000](http://127.0.0.1:8000)** pour poser vos questions en direct !
