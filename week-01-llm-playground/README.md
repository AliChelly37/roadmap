# Semaine 1 - LLM Playground

Livrable de la **Semaine 1** du cursus AI Engineering.  
Ce dossier contient tous les scripts explorés et le CLI final qui combine les 3 compétences clés.

---

## Compétences acquises

| # | Compétence | Script |
|---|---|---|
| 1 | Appels API multi-provider (Gemini, Groq, Ollama) | `chat_unified.py` |
| 2 | Extraction structurée avec Pydantic + Instructor | `extract_job.py`, `extract_job_robust.py` |
| 3 | Tool Calling (function calling) | `tool_use_weather.py` |

---

## Installation

```bash
# 1. Créer et activer l'environnement virtuel
python -m venv .venv
.venv\Scripts\activate

# 2. Installer les dépendances
pip install openai instructor pydantic python-dotenv google-generativeai

# 3. Avoir Ollama installé avec le modèle llama3.1
ollama pull llama3.1
```

---

## CLI Final - `cli_final.py`

Point d'entrée unique qui combine les 3 modes.  
**Prérequis :** Ollama doit tourner en arrière-plan (`ollama serve`).

### Mode 1 : Chat libre

```bash
python cli_final.py chat "C'est quoi un transformer ?"
```

Envoie une question au LLM et reçoit une réponse texte.

### Mode 2 : Extraction structurée

```bash
python cli_final.py extract "Poste : Data Scientist chez ACME, salaire 50k-70k, Python requis."
```

Extrait un objet JSON `JobPosting` structuré depuis un texte non structuré.  
Utilise **Instructor** pour garantir la conformité Pydantic, avec jusqu'à 3 tentatives automatiques.

**Exemple de sortie :**
```json
{
  "title": "Data Scientist",
  "company": "ACME",
  "salary_min": 50000,
  "salary_max": 70000,
  "required_skills": ["Python"]
}
```

### Mode 3 : Tool Calling (météo)

```bash
python cli_final.py weather "Il fait quel temps a Paris ?"
```

Le LLM décide d'appeler la fonction Python `get_weather()`.  
**Principe :** le LLM identifie la ville, le script Python exécute la vraie fonction, le LLM formule la réponse finale.

---

## Architecture du Tool Calling

```
Utilisateur -> Question -> LLM (Llama 3.1)
                              |
                   [Décide d'appeler get_weather]
                              |
                    Script Python exécute la fonction
                              |
                   Résultat renvoyé au LLM
                              |
                       Réponse finale
```

---

## Concepts clés appris

- **Tokenisation & Contexte** : Comment un LLM "lit" le texte (tokens, températures, max_tokens)
- **Pydantic** : Définir des schémas de données stricts avec validation automatique
- **Instructor** : Forcer un LLM à renvoyer un objet Pydantic valide (avec auto-retry)
- **Tool Calling** : Donner des "outils" Python à un LLM — il décide quand les appeler, nous les exécutons
- **Provider abstraction** : Même interface (OpenAI SDK) pour Ollama local, Groq, Cloudflare, Gemini
