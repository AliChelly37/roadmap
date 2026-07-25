# Semaine 2 : Prompt Engineering & FastAPI

Ce projet implémente les objectifs de la **Semaine 2** de la roadmap d'ingénierie IA, combinant la conception de prompts (Prompt Engineering), la validation de données avec **Pydantic**, la programmation asynchrone avec **FastAPI**, et l'évaluation continue des prompts avec **promptfoo**.

## 🚀 Fonctionnalités

1. **Templating de Prompts robuste** : Une classe [PromptTemplate](prompt_template.py) réutilisable gérant les prompts système, l'injection sécurisée de variables (`safe_substitute`) et les exemples few-shot dans le format d'API standard d'OpenAI/Ollama.
2. **Endpoint de Chat en Streaming (SSE)** : Une route `/chat` qui interroge localement un LLM via Ollama et retourne sa réponse token par token en utilisant les Server-Sent Events (SSE).
3. **Extraction de Données Structurées** : Une route `/extract` validée par Pydantic qui analyse du texte libre pour en extraire des informations structurées (nom, âge, profession, ville) sous forme de JSON propre.
4. **Gestionnaire de Tickets (Issues)** : Un mini-CRUD sous `/api/V1/issues` stockant l'état des tickets dans un fichier JSON pour simuler une base de données.
5. **Interface Graphique Premium** : Une page d'accueil interactive et moderne avec un design *glassmorphism* dark mode, permettant de tester le streaming en direct.

---

## 📂 Structure du Projet

```text
week-02-prompt-fastapi/
├── main.py                 # Point d'entrée de l'application FastAPI
├── prompt_template.py      # Module de templating de prompt
├── index.html              # Frontend de l'application (Playground de Chat)
├── promptfooconfig.yaml    # Fichier de configuration des évaluations promptfoo
├── test_template.py        # Script de test unitaire pour PromptTemplate
├── test_extract.py         # Script de test unitaire pour /extract (TestClient)
├── test_chat_stream.py     # Script de test de streaming SSE
└── app/
    ├── __init__.py
    ├── schemas.py          # Modèles de données Pydantic (validation automatique)
    ├── storage.py          # Logique d'écriture/lecture du fichier JSON de données
    └── routes/
        ├── __init__.py
        ├── chat.py         # Route de chat streaming (SSE)
        ├── extract.py      # Route d'extraction d'informations
        └── issues.py       # Route CRUD du gestionnaire de tickets
```

---

## 🛠️ Installation & Démarrage

### 1. Prérequis
Assurez-vous que Node.js (v18+) et Python (3.11+) sont installés.
Démarrez également Ollama en local avec le modèle `llama3.2` ou `llama3.1` :
```bash
ollama run llama3.2
```

### 2. Démarrage de l'API
Activez votre environnement virtuel et lancez le serveur FastAPI :
```bash
uvicorn main:app --reload
```
Le serveur tourne maintenant sur [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
* La documentation Swagger interactive est accessible sur [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
* L'interface de chat interactive est accessible directement sur [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## 🧪 Évaluations avec promptfoo

Pour s'assurer que le prompt d'extraction de données reste performant au fil des modifications, nous utilisons **promptfoo** pour exécuter des tests d'assertions automatisés sur notre API.

### Lancer la suite d'évaluation
```bash
npx promptfoo eval --no-cache
```

### Résultat obtenu
```text
✓ Eval complete (ID: eval-znR-2026-07-25T00:30:39)

Results:
  ✓ 3 passed (100%)
  0 failed (0%)
  0 errors (0%)
```

Les assertions vérifient :
- Que la réponse est un **JSON valide**.
- Que les entités présentes (ex: `Sarah Dupont`, `Paris`, `ingénieure en IA`) sont correctement extraites dans les champs correspondants.
- Que les données manquantes sont correctement assignées à la valeur `null`.
