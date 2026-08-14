# 📊 Mémo : Gateway LLMOps avec LiteLLM (Semaine 7 - J2)

Ce mémo résume l'utilisation de LiteLLM pour centraliser et sécuriser l'accès aux LLMs dans une architecture de production.

## 🎯 Concepts Clés

Qu'est-ce que LiteLLM ? #flashcard
LiteLLM est une bibliothèque Python (et un proxy serveur) qui standardise les appels vers plus de 100 API LLMs (OpenAI, Anthropic, Ollama, etc.) en utilisant le même format que l'API d'OpenAI. C'est le point d'entrée unique (Gateway) de l'application vers les modèles.

Pourquoi utiliser un système de Fallback ? #flashcard
En production, les fournisseurs d'API LLM peuvent tomber en panne ou imposer des limites de débit (Rate Limits). Un Fallback permet de basculer automatiquement sur un modèle de secours (ex: de GPT-4 vers Llama-3 local) sans que l'application ne crashe ni que l'utilisateur final ne s'en rende compte.

Qu'est-ce qu'un Retry dans LiteLLM ? #flashcard
C'est un mécanisme de résilience qui relance automatiquement la même requête vers le modèle si celui-ci échoue à cause d'une erreur transitoire (comme un Timeout ou un Rate Limit temporaire) avant de lever une erreur ou de passer au Fallback.

## 🛠️ Implémentation

Comment activer le routage et le fallback avec LiteLLM ? #flashcard
On utilise `litellm.completion` et on passe l'argument `fallbacks` contenant une liste de modèles de secours :
```python
response = litellm.completion(
    model="openai/gpt-4",
    messages=[{"role": "user", "content": "Hello"}],
    fallbacks=["ollama/llama3.1", "anthropic/claude-3-haiku-20240307"],
    num_retries=2
)
```

Comment suivre le coût d'une requête spécifique avec LiteLLM ? #flashcard
On utilise la fonction `completion_cost()` en lui passant la réponse :
```python
from litellm import completion_cost
cost = completion_cost(completion_response=response)
```
