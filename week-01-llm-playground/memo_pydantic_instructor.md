# Mémo : Pydantic, Instructor & Extraction Structurée

Ce mémo résume les concepts clés abordés concernant l'extraction de données structurées à l'aide de LLMs.

## 1. Pydantic : Le Moule Strict
Pydantic est une librairie de validation de données en Python.
- **Concept :** On définit un schéma (un "Modèle") via une classe qui hérite de `BaseModel`.
- **Validation :** Si on passe des données qui ne respectent pas le type attendu (ex: une string `"vingt"` pour un entier), Pydantic lève une `ValidationError` claire et détaillée. S'il peut convertir (ex: `"1200"` en entier `1200`), il le fait automatiquement.
- **Utilité pour l'IA :** Les Modèles Pydantic (qui peuvent être imbriqués) servent de contrat strict pour la sortie attendue d'un LLM.

## 2. Instructor : Le Pont entre le LLM et Pydantic
Les LLMs génèrent naturellement du texte libre, ce qui rend le "parsing" (l'extraction) difficile et instable.
- **Rôle d'Instructor :** Il "enveloppe" les clients d'API (OpenAI, Groq, Gemini) pour qu'ils renvoient directement un objet Pydantic valide.
- **Fonctionnement :**
  1. On initialise le client en l'enveloppant avec Instructor (ex: `instructor.from_gemini(...)`).
  2. Lors de la requête, on ajoute le paramètre magique `response_model=MonModelePydantic`.
  3. La réponse retournée n'est plus une string, mais directement l'objet Python instancié et validé.
- **Le super pouvoir (Auto-Retry) :** Si le LLM se trompe (ex: il oublie un champ obligatoire), Instructor intercepte la `ValidationError` de Pydantic et relance automatiquement le LLM avec le message d'erreur pour qu'il se corrige lui-même.

## 3. Comment l'IA comprend-elle et place-t-elle les mots ? (Function Calling)
L'alliance entre la compréhension sémantique de l'IA et la rigueur de Pydantic fonctionne en 3 étapes :
1. **Compréhension :** Le LLM lit le prompt ("Je m'appelle Jean et j'ai 32 ans") et comprend sémantiquement les entités (Prénom, Âge).
2. **Le Contrat (JSON Schema) :** Instructor convertit le modèle Pydantic en JSON Schema et l'envoie via l'API au LLM comme un "outil" (Tool Calling / Function Calling). Le LLM reçoit l'ordre strict d'utiliser cet outil avec les bons paramètres.
3. **Génération contrainte :** Sous cette contrainte mathématique, l'API force le LLM à générer des tokens qui respectent parfaitement l'architecture JSON demandée (`{"name": "Jean", "age": 32}`). 

## Exemple de Code (Gemini + Instructor)
```python
import os
import google.generativeai as genai
import instructor
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class UserInfo(BaseModel):
    name: str
    age: int

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Enveloppe le client Gemini avec instructor
client = instructor.from_gemini(
    client=genai.GenerativeModel(model_name="models/gemini-2.5-flash"),
    mode=instructor.Mode.GEMINI_JSON,
)

# Extraction structurée via response_model
user_info = client.messages.create(
    response_model=UserInfo,
    messages=[
        {"role": "user", "content": "je m'appelle Jean et j'ai 32 ans."}
    ]
)

print(user_info.name) # "Jean"
```
