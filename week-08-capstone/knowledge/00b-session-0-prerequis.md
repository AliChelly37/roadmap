# 🔬 Session 0 — Validation des prérequis

**📍 Fichier système** · À faire **une seule fois**, avant la Semaine 1 · Durée : **~2 h**
**🎯 Objectif :** confirmer que chaque prérequis est **vraiment opérationnel** — pas juste « je pense maîtriser », mais « ça tourne sur ma machine ».

> **Pour l'agent IA :** ce fichier contient des tâches préfixées `S0-T{n}`. Elles apparaissent dans `PROGRESS_TRACKER.md` avant la Semaine 1. Toutes les tâches `S0` doivent être `✅` ou `⏭️` avant de générer le plan de `S1-J1`.

---

## Comment utiliser ce fichier

Chaque section = **1 prérequis** à valider avec un **mini-exercice concret** (~10–20 min).

- Si l'exercice **passe** → coche `✅`, tu es bon.
- Si tu **bloques** → suis le lien de rattrapage avant S1 (durée indiquée).
- Les prérequis marqués `⭐ Critique` bloquent la S1 si non validés. Les autres sont rattrapables en cours de route.

---

## S0-T1 — Python intermédiaire ⭐ Critique ⏱️ ~20 min

### Mini-exercice
Écris ce script **de mémoire** (sans copier) et fais-le tourner :

```python
# prerequisite_check.py
import json
from dataclasses import dataclass
from typing import Optional

@dataclass
class ModelResponse:
    content: str
    tokens_used: int
    model: str
    cached: Optional[bool] = False

def parse_response(raw: dict) -> ModelResponse:
    """Parse une réponse brute d'API en objet typé."""
    return ModelResponse(
        content=raw["choices"][0]["message"]["content"],
        tokens_used=raw["usage"]["total_tokens"],
        model=raw["model"],
        cached=raw.get("cached", False)
    )

# Données de test
fake_response = {
    "choices": [{"message": {"content": "Bonjour !"}}],
    "usage": {"total_tokens": 42},
    "model": "gemini-2.5-flash",
    "cached": True
}

result = parse_response(fake_response)
print(json.dumps(result.__dict__, indent=2))
assert result.tokens_used == 42, "Erreur de parsing"
assert result.cached is True
print("✅ Prérequis Python OK")
```

**Résultat attendu :**
```json
{
  "content": "Bonjour !",
  "tokens_used": 42,
  "model": "gemini-2.5-flash",
  "cached": true
}
✅ Prérequis Python OK
```

**Ce que ça teste :** dataclasses, typing, dict access, `.get()`, `json`, assertions, f-strings.

**Si tu bloques :**
- Revoir `dataclass` → `realpython.com/python-data-classes` ⏱️ ~30 min
- Revoir `typing` (Optional, List, Dict) → `docs.python.org/3/library/typing.html` ⏱️ ~20 min

---

## S0-T2 — Environnements virtuels & packages ⭐ Critique ⏱️ ~15 min

### Mini-exercice
Dans un **nouveau dossier vide**, exécute ces commandes dans le terminal :

```bash
# Crée et active un env virtuel
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
# .venv\Scripts\activate       # Windows

# Installe un package et vérifie
pip install httpx
python -c "import httpx; print('httpx version:', httpx.__version__)"

# Génère le requirements.txt
pip freeze > requirements.txt
cat requirements.txt            # Doit contenir httpx

# Vérifie l'isolation (l'env voit httpx, le système non)
deactivate
python -c "import httpx" 2>&1 || echo "✅ Isolation OK — httpx absent hors venv"
```

**Résultat attendu :** httpx importé dans le venv, absent hors venv.

**Alternative rapide (si tu préfères `uv`) :**
```bash
pip install uv
uv venv .venv && source .venv/bin/activate
uv pip install httpx
```

**Si tu bloques :**
- `realpython.com/python-virtual-environments-a-primer` ⏱️ ~20 min

---

## S0-T3 — Variables d'environnement & `.env` ⭐ Critique ⏱️ ~15 min

### Mini-exercice
Crée ces 2 fichiers dans ton dossier de test :

**`.env`** (ne jamais committer ce fichier !)
```
MY_API_KEY=sk-test-1234567890abcdef
MY_MODEL=gemini-2.5-flash
```

**`test_env.py`**
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Charge le .env

api_key = os.getenv("MY_API_KEY")
model = os.getenv("MY_MODEL")

assert api_key is not None, "❌ MY_API_KEY non chargée"
assert api_key.startswith("sk-"), "❌ Format inattendu"
assert model == "gemini-2.5-flash"

print(f"✅ Clé chargée : {api_key[:8]}... (tronquée)")
print(f"✅ Modèle : {model}")
```

```bash
pip install python-dotenv
python test_env.py
```

**Puis vérifie la sécurité Git :**
```bash
git init
echo ".env" >> .gitignore
git status   # .env ne doit PAS apparaître dans les fichiers à committer
```

**Résultat attendu :** clé chargée + `.env` ignoré par Git.

**Si tu bloques :**
- `pypi.org/project/python-dotenv` ⏱️ ~10 min

---

## S0-T4 — Git & GitHub ⭐ Critique ⏱️ ~20 min

### Mini-exercice
Crée et pousse ton repo de roadmap :

```bash
# Configure git si pas encore fait
git config --global user.name "Ton Nom"
git config --global user.email "ton@email.com"

# Initialise le repo
mkdir ai-engineer-roadmap && cd ai-engineer-roadmap
git init

# Structure de base
mkdir week-01-llm-playground
echo "# AI Engineer Roadmap" > README.md
echo ".env" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".venv/" >> .gitignore

# Premier commit
git add .
git commit -m "feat: initialise la structure de la roadmap AI Engineer"

# Pousse sur GitHub (crée d'abord le repo vide sur github.com)
git remote add origin https://github.com/TON_USERNAME/ai-engineer-roadmap.git
git branch -M main
git push -u origin main
```

**Vérifie sur GitHub :** le repo est visible, `.env` absent, `README.md` présent.

**Si tu bloques :**
- `docs.github.com/en/get-started/quickstart` ⏱️ ~20 min

---

## S0-T5 — Appel API REST & JSON ⭐ Critique ⏱️ ~20 min

### Mini-exercice
Fais un appel HTTP réel à une API publique gratuite et parse la réponse :

```python
# test_api.py
import httpx
import json

# Appel à une API publique (pas de clé requise)
response = httpx.get("https://httpbin.org/json")
assert response.status_code == 200, f"❌ Status: {response.status_code}"

data = response.json()
print("Réponse brute :", json.dumps(data, indent=2)[:200])

# Simule la structure d'une réponse LLM
fake_llm_response = {
    "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
    "type": "message",
    "role": "assistant",
    "content": [{"type": "text", "text": "Bonjour ! Comment puis-je vous aider ?"}],
    "model": "gemini-2.5-flash",
    "usage": {"input_tokens": 10, "output_tokens": 12}
}

# Parse
content = fake_llm_response["content"][0]["text"]
total_tokens = sum(fake_llm_response["usage"].values())

assert "Bonjour" in content
assert total_tokens == 22

print(f"✅ API REST OK — contenu : {content}")
print(f"✅ Tokens : {total_tokens}")
```

**Ce que ça teste :** `httpx`, status codes, `.json()`, dict imbriqué, `sum()`.

**Si tu bloques :**
- `realpython.com/python-requests` (similaire à httpx) ⏱️ ~20 min

---

## S0-T6 — Setup Ollama & premier modèle local ⏱️ ~30 min

*(Non critique — peut se faire en J2 de S1 si nécessaire)*

### Mini-exercice
```bash
# 1. Installe Ollama
# Mac : brew install ollama
# Linux : curl -fsSL https://ollama.com/install.sh | sh
# Windows : télécharge l'installeur sur ollama.com

# 2. Lance le serveur
ollama serve &

# 3. Télécharge un petit modèle (choisis selon ta RAM)
# < 8 Go RAM  → ollama pull qwen2.5:1.5b   (~1 Go)
# 8–16 Go RAM → ollama pull llama3.2:3b    (~2 Go)
# > 16 Go RAM → ollama pull llama3.1:8b    (~5 Go)

ollama pull qwen2.5:1.5b   # ajuste selon ta machine

# 4. Teste le modèle
ollama run qwen2.5:1.5b "Dis 'Bonjour' en français en 1 phrase."
```

**Puis teste via l'API HTTP (comme tu le feras dans le code Python) :**
```python
# test_ollama.py
import httpx

response = httpx.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen2.5:1.5b",
        "prompt": "Réponds juste 'OK' si tu fonctionnes.",
        "stream": False
    },
    timeout=60
)

data = response.json()
print("Réponse Ollama :", data["response"])
assert response.status_code == 200
print("✅ Ollama OK")
```

**Si tu bloques :**
- `ollama.com` → onglet « Docs » ⏱️ ~15 min

---

## S0-T7 — Compte Hugging Face & clé API Gemini ⏱️ ~20 min

*(Non critique — peut se faire en début de S1)*

### Mini-exercice

**Hugging Face :**
```bash
pip install huggingface_hub
python -c "
from huggingface_hub import HfApi
api = HfApi()
# Cherche un modèle d'embedding multilingue
models = list(api.list_models(search='bge-m3', limit=3))
print('Modèles trouvés :', [m.id for m in models])
print('✅ HuggingFace Hub accessible')
"
```

**Google AI Studio (Gemini) :**
1. Ouvre `aistudio.google.com`
2. Clique « Get API key » → crée une clé **sans carte bancaire**
3. Teste :
```python
# test_gemini.py
import os
import httpx
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
assert api_key, "❌ GEMINI_API_KEY manquante dans .env"

response = httpx.post(
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}",
    json={"contents": [{"parts": [{"text": "Réponds juste 'OK'."}]}]},
    timeout=30
)

assert response.status_code == 200, f"❌ {response.status_code}: {response.text}"
content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
print(f"✅ Gemini OK — réponse : {content.strip()}")
```

---

## S0-T8 — VS Code / IDE & structure du projet ⏱️ ~15 min

*(Non critique — adaptable à ton IDE)*

### Mini-exercice
Vérifie que ton environnement de développement est opérationnel :

```bash
# Structure finale de ton repo après Session 0
ai-engineer-roadmap/
├── .gitignore          # .env, __pycache__, .venv
├── README.md
├── .env                # clés (JAMAIS committé)
├── requirements.txt    # vide pour l'instant
└── week-01-llm-playground/
    └── .gitkeep        # dossier prêt pour S1
```

**Checklist VS Code (ou ton IDE) :**
- [ ] Extension **Python** installée + interpréteur pointant vers `.venv`
- [ ] Terminal intégré qui voit le bon env (`which python` → doit être dans `.venv`)
- [ ] `.env` n'est PAS indexé / suggéré par l'autocomplétion (respecte `.gitignore`)
- [ ] Tu peux exécuter un fichier `.py` avec `F5` ou `Run`

---

## Tableau de validation

Remplis ce tableau et donne-le à l'agent pour initialiser `PROGRESS_TRACKER.md` :

| ID | Prérequis | Statut | Notes |
|---|---|:---:|---|
| `S0-T1` | Python intermédiaire (dataclass, typing, json) | ⬜ | |
| `S0-T2` | Environnements virtuels & pip | ⬜ | |
| `S0-T3` | Variables d'env & `.env` sécurisé | ⬜ | |
| `S0-T4` | Git & GitHub (repo créé et poussé) | ⬜ | |
| `S0-T5` | Appel API REST & parsing JSON | ⬜ | |
| `S0-T6` | Ollama installé + modèle local ⬜/⏭️ | ⬜ | |
| `S0-T7` | HF Hub + clé Gemini testée | ⬜ | |
| `S0-T8` | IDE configuré + structure projet | ⬜ | |

> **Pour l'agent :** toutes les tâches `S0-T1` à `S0-T5` doivent être `✅` avant de démarrer `S1-J1-T1`. Si l'une d'elles est `❌`, générer un plan de rattrapage avant S1 (pas de plan S1 tant que les ⭐ Critique ne sont pas validées).

---

## Temps de rattrapage estimé par prérequis manquant

| Prérequis manquant | Ressource | Temps |
|---|---|:---:|
| Python de base (variables, boucles, fonctions) | `learnpython.org` | ~3–4 h |
| Python OOP (classes, héritage) | `realpython.com/python3-object-oriented-programming` | ~2 h |
| Environnements virtuels | `realpython.com/python-virtual-environments-a-primer` | ~30 min |
| Git (bases) | `docs.github.com/en/get-started/quickstart` | ~1 h |
| API REST (HTTP, JSON) | `realpython.com/python-requests` | ~1 h |
| async/await | `realpython.com/async-io-python` | ~1 h |

> Si tu as **≥ 3 prérequis critiques manquants**, prévois **1 semaine supplémentaire** avant S1 pour les combler — c'est plus efficace que de bloquer en cours de route.

---

*Fichier système — Roadmap AI Engineer (8 semaines). Créé en juin 2026.*
*Pour l'agent : ce fichier est lu une seule fois (Session 0). Les tâches `S0-Tx` sont ensuite suivies dans `PROGRESS_TRACKER.md`.*
