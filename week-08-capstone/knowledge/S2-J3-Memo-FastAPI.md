# Mémo S2-J3 : FastAPI — Guide pour débutant

> **FastAPI** est un framework web Python **moderne et ultra-rapide** pour construire des APIs. C'est l'outil qu'on utilise pour transformer un script Python en un vrai serveur web que d'autres applications (une app mobile, un front-end React, ou un autre script Python) peuvent interroger via HTTP.

---

## Pourquoi FastAPI plutôt qu'un autre ?

| Avantage | Ce que ça veut dire concrètement |
|---|---|
| **Rapide** | Aussi rapide que NodeJS en termes de performances réseau |
| **Documentation automatique** | Génère un site Swagger UI sans écrire une seule ligne de doc |
| **Validation automatique** | Si quelqu'un envoie un mauvais JSON à ton API, FastAPI le rejette automatiquement |
| **Async natif** | Conçu pour gérer des milliers de requêtes simultanées sans bloquer |
| **Minimal** | Pas de code inutile, on va droit au but |

---

## 1. Minimal Boilerplate (Peu de code pour démarrer)

**"Boilerplate"** = le code obligatoire qu'on doit écrire avant de commencer à faire des choses utiles.

Dans d'autres frameworks Python comme Django, il faut créer des dizaines de fichiers de configuration avant d'afficher "Hello World". FastAPI, lui, est opérationnel en **4 lignes**.

```python
from fastapi import FastAPI   # 1. On importe la librairie

app = FastAPI()               # 2. On crée notre "application"

@app.get("/")                 # 3. On définit une URL
def hello():
    return {"message": "Hello World"}  # 4. On répond en JSON
```

C'est la totalité du code pour un serveur web fonctionnel. C'est ça, "minimal boilerplate".

---

## 2. Décorateur Python (`@app.get("/")`)

Un **décorateur** est une fonction Python qui "enveloppe" une autre fonction pour lui ajouter des pouvoirs, sans modifier son code intérieur.

**Analogie :** Imagine une vignette autocollante sur une boîte. La boîte (ta fonction) reste la même, mais la vignette donne des informations supplémentaires sur ce qu'elle contient et comment la manipuler.

```python
@app.get("/utilisateurs")  # <- LE DÉCORATEUR : dit à FastAPI "cette fonction répond aux requêtes GET sur /utilisateurs"
def get_utilisateurs():    # <- LA FONCTION NORMALE : elle fait juste son travail
    return [{"nom": "Alice"}, {"nom": "Bob"}]
```

Ici, `@app.get("/utilisateurs")` est un décorateur. Il dit à FastAPI : *"Quand quelqu'un fait une requête GET sur l'URL `/utilisateurs`, appelle cette fonction et renvoie le résultat."*

---

## 3. Les Méthodes HTTP de FastAPI (`GET`, `POST`, `PUT`, `DELETE`)

HTTP (le protocole d'Internet) définit différents **types de requêtes** selon ce qu'on veut faire. FastAPI les expose directement comme décorateurs :

| Méthode | Décorateur FastAPI | Usage |
|---|---|---|
| **GET** | `@app.get("/")` | Récupérer des données (lecture) |
| **POST** | `@app.post("/")` | Envoyer des nouvelles données (création) |
| **PUT** | `@app.put("/{id}")` | Modifier des données existantes |
| **DELETE** | `@app.delete("/{id}")` | Supprimer des données |

**Analogie :** C'est comme un formulaire dans une mairie.
- **GET** = Demander un document ("Donnez-moi ma carte d'identité").
- **POST** = Déposer un dossier ("Voici ma demande de passeport").
- **PUT** = Modifier un dossier existant ("Je veux changer mon adresse").
- **DELETE** = Annuler une demande.

---

## 4. Les Routes

Une **route** = une URL de ton API. C'est l'adresse à laquelle on peut "frapper à la porte" de ton serveur pour lui demander quelque chose.

**Analogie :** Ton serveur est un immeuble. Chaque route est un appartement différent avec son propre numéro.
- `/` → Le hall d'entrée (route principale).
- `/chat` → L'appartement "Chat avec le LLM".
- `/extract` → L'appartement "Extraire des données structurées".

```python
@app.get("/")          # Route "/" → Accueil
def accueil():
    return {"status": "ok"}

@app.get("/chat")      # Route "/chat" → Chat
def chat():
    return {"message": "Ici tu parles au LLM"}
```

### Route avec paramètre variable (`{id}`)
On peut mettre une variable dans l'URL avec `{nom_variable}` :
```python
@app.get("/issues/{issue_id}")  # L'ID varie selon la requête
def get_issue(issue_id: str):   # FastAPI injecte automatiquement la valeur ici
    return {"id": issue_id}
# → http://localhost:8000/issues/42 → retourne {"id": "42"}
```

---

## 5. Requêtes POST et corps de la requête

Pour une requête **POST**, l'utilisateur envoie des données à l'API (un "corps" de requête, en JSON). On définit le format de ces données avec **Pydantic** (voir ci-dessous) :

```python
from pydantic import BaseModel

class IssueCreation(BaseModel):  # On définit les champs attendus
    title: str
    priority: str

@app.post("/issues/")
def create_issue(payload: IssueCreation):  # FastAPI valide automatiquement le JSON
    return {"message": f"Issue '{payload.title}' créée !"}
```

Si quelqu'un envoie un JSON sans le champ `title`, FastAPI renvoie automatiquement une erreur 422 (données invalides). Plus besoin de vérification manuelle.

---

## 6. APIRouter — Structurer le code en modules

Quand une application grossit, on ne veut pas tout mettre dans `main.py`. **`APIRouter`** permet de définir des routes dans des fichiers séparés et de les "brancher" ensuite sur l'application principale.

**Analogie :** C'est comme une multiprise électrique. `FastAPI()` est la prise murale principale. Chaque `APIRouter` est une multiprise qu'on branche dessus, avec ses propres prises (routes).

```
week-02-prompt-fastapi/
├── main.py             ← Prise murale principale
└── app/
    ├── __init__.py
    └── routes/
        ├── chat.py     ← Multiprise "chat"
        └── issues.py   ← Multiprise "issues"
```

**Dans `app/routes/issues.py` :**
```python
from fastapi import APIRouter

router = APIRouter()  # ← On crée une multiprise

@router.get("")       # ← On y branche des appareils (routes)
def get_issues():
    return [{"title": "Bug 1"}]
```

**Dans `main.py` :**
```python
from fastapi import FastAPI
from app.routes.issues import router as issues_router

app = FastAPI()

# On branche la multiprise "issues" sur la prise principale, avec un préfixe
app.include_router(issues_router, prefix="/issues")
# → Crée automatiquement la route GET /issues
```

---

## 7. Module de Stockage JSON (`storage.py`)

Pour éviter une vraie base de données complexe (comme PostgreSQL), on peut utiliser un **fichier JSON** comme base de données simplifiée. Un fichier `storage.py` gère tout ça :

```python
import json

DATA_FILE = "data.json"  # Notre "base de données" simplifiée

def load_data():
    """Lit le fichier JSON et renvoie les données sous forme de dictionnaire Python."""
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    """Écrit les nouvelles données dans le fichier JSON."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
```

**Usage dans une route :**
```python
@router.post("/")
def create_issue(payload: IssueCreation):
    data = load_data()             # 1. Lis les données existantes
    data.append(payload.dict())    # 2. Ajoute le nouvel élément
    save_data(data)                # 3. Sauvegarde tout
    return payload
```

---

## 8. `async` / `await` en Python

**`async`** et **`await`** permettent à Python d'exécuter plusieurs tâches "en même temps" (de manière concurrente) sans bloquer.

**Analogie :** Imagine un cuisinier (Python) dans un restaurant.

- **Sans `async` (synchrone) :** Il met de l'eau à bouillir, et il **attend debout devant la casserole** que ça bouille avant de faire quoi que ce soit d'autre. Pendant ce temps, tous les autres clients attendent.
- **Avec `async` (asynchrone) :** Il met de l'eau à bouillir, **va préparer autre chose** pendant que ça chauffe, et revient quand l'eau est prête. Il peut servir plusieurs clients en même temps !

```python
import httpx

@app.get("/weather")
async def get_weather():
    # "await" dit : "Lance cet appel réseau lent, et pendant ce temps,
    # FastAPI peut gérer les requêtes des autres utilisateurs."
    async with httpx.AsyncClient() as client:
        response = await client.get("http://api.meteo.fr")
    return response.json()
```

**Règle pratique :** Dès qu'une fonction fait une opération lente (appel réseau, lecture de fichier, requête base de données), ajoute `async` devant `def` et `await` devant l'opération lente. Pour tout le reste, une fonction `def` normale suffit.

---

## 9. Documentation Automatique (Swagger UI)

C'est l'une des fonctionnalités les plus magiques de FastAPI. Dès que ton serveur tourne, tu peux aller sur **`http://127.0.0.1:8000/docs`** et tu trouveras un site web interactif généré automatiquement qui :
- Liste toutes tes routes (`GET /issues`, `POST /issues`, etc.).
- Te permet de tester chaque route en cliquant sur un bouton, sans avoir besoin de Postman ou d'un autre outil.
- Documente automatiquement le format JSON attendu (grâce aux modèles Pydantic).

---

## 10. Websockets & Streaming

FastAPI ne sert pas qu'à faire du CRUD (Créer, Lire, Modifier, Supprimer).

- **Streaming HTTP :** Envoyer la réponse d'un LLM **mot par mot** (comme ChatGPT qui tape progressivement). On utilise `StreamingResponse` pour ça.
- **WebSockets :** Connexion bi-directionnelle persistante entre le client et le serveur. Utile pour les chats en temps réel ou les applications collaboratives.
- **Background Tasks :** Lancer une tâche longue (ex: envoyer un email, traiter une image) **sans faire attendre** l'utilisateur. La route répond immédiatement "C'est lancé !" et la tâche s'exécute en arrière-plan.

---

## 11. Streaming d'un LLM en Pratique (Server-Sent Events)

Pour streamer une réponse d'un LLM vers le client (effet "machine à écrire"), on utilise la technique des **Server-Sent Events (SSE)** avec FastAPI. Voici les concepts clés mis en pratique lors de l'intégration :

### 1. Le passage à `AsyncOpenAI` (L'asynchrone)
Pour ne pas bloquer le serveur FastAPI pendant que le modèle génère le texte, il est indispensable d'utiliser un client asynchrone :
```python
from openai import AsyncOpenAI
client = AsyncOpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
```
Cela permet d'utiliser le mot-clé `await` lors de la requête. Pendant que l'API attend le prochain token, la boucle d'événements (event loop) de FastAPI est libérée et peut traiter les requêtes d'autres utilisateurs.

### 2. Le générateur asynchrone (`yield`)
Pour renvoyer du texte morceau par morceau, Python utilise un **générateur** (une fonction avec `yield` au lieu de `return`) :

```python
async def stream_generator():
    stream = await client.chat.completions.create(
        model="llama3.2", messages=messages, stream=True # <-- Active le streaming
    )
    
    async for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            # Format SSE obligatoire : "data: [texte]\n\n"
            yield f"data: {content}\n\n"
            
    # Marqueur de fin de flux
    yield "data: [DONE]\n\n"
```
**Pourquoi le format `data: ... \n\n` ?** C'est le standard du protocole SSE. Pour qu'un navigateur web comprenne qu'il s'agit d'un flux de données, chaque message doit obligatoirement commencer par `data: ` et finir par un double saut de ligne.

### 3. Brancher la `StreamingResponse` de FastAPI
À la fin de la route, on donne notre générateur directement à FastAPI avec le bon `media_type` pour que la connexion HTTP reste ouverte :
```python
from fastapi.responses import StreamingResponse
return StreamingResponse(stream_generator(), media_type="text/event-stream")
```

### 4. Le Frontend (Client JS)
Côté navigateur, on ne peut pas simplement faire un `await fetch().json()` car la réponse n'est pas finalisée. On doit lire le flux manuellement au fur et à mesure que les paquets arrivent :
```javascript
const response = await fetch('/chat/', { method: 'POST', ... });
const reader = response.body.getReader();

while (true) {
    const { done, value } = await reader.read(); // On lit les morceaux (octets) un par un
    if (done) break;
    const chunk = new TextDecoder().decode(value); // Conversion des octets en texte
    // Traitement du chunk (découpage sur "data: ") et injection dans le HTML
}
```

---
*FastAPI est l'outil parfait pour construire des applications d'IA : il est rapide, supporte le streaming natif (indispensable pour afficher les réponses des LLMs en temps réel) et la validation automatique des données avec Pydantic.*
