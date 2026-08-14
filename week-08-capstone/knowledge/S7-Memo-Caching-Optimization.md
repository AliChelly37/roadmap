# 📊 Mémo : Caching & Optimisation des Coûts (Semaine 7 - J3)

Ce mémo résume en détail les stratégies d'optimisation des performances (latence) et de réduction des coûts (FinOps) dans une architecture LLM.

## 🎯 Caching : Exact vs Sémantique

Quelle est la différence fondamentale entre un Cache Exact et un Cache Sémantique ? #flashcard
- **Cache Exact** : Le système vérifie si la chaîne de caractères (le prompt) est *strictement 100% identique* à une requête précédente. C'est rapide mais très rigide. La moindre virgule en trop provoque un "Cache Miss".
- **Cache Sémantique** : Le système comprend le sens de la phrase. Si deux questions sont formulées différemment mais demandent la même chose (ex: "Météo Paris" vs "Quel temps fait-il à Paris ?"), le cache reconnaît la similarité et sert la réponse.

Comment fonctionne techniquement un Cache Sémantique (ex: GPTCache) sous le capot ? #flashcard
1. **Embedding** : La requête utilisateur est transformée en un vecteur mathématique (via un modèle d'embedding très rapide et peu coûteux).
2. **Recherche Vectorielle** : Ce vecteur est comparé aux anciennes requêtes stockées dans une base de données vectorielle (ex: ChromaDB, FAISS, Redis).
3. **Seuil de similarité (Cosine Similarity)** : Si la distance entre les deux vecteurs dépasse un certain seuil (ex: 95% de similarité), c'est un "Cache Hit".
4. **Retour direct** : La réponse associée est renvoyée, évitant l'appel au grand modèle LLM.

Y a-t-il un coût caché au Cache Sémantique ? #flashcard
Oui. Contrairement au cache exact qui est gratuit, le cache sémantique nécessite de générer un **Embedding** pour chaque nouvelle question. Cependant, les modèles d'embedding (ex: `text-embedding-3-small`) sont infiniment moins chers et plus rapides que les modèles de génération (LLMs). L'économie réalisée sur la génération compense très largement le coût de l'embedding.

Qu'est-ce que le "Cache Hit Rate" en LLMOps ? #flashcard
C'est le pourcentage de requêtes qui sont interceptées et servies par le cache, par rapport au nombre total de requêtes. Un Cache Hit Rate de 30% signifie que 30% de vos requêtes ont coûté 0$ d'inférence LLM et ont été répondues instantanément.

## 🛠️ Implémentation avec LiteLLM

Comment activer un cache exact basique en mémoire ou via Redis avec LiteLLM ? #flashcard
Pour un cache en mémoire (RAM) idéal pour des tests locaux :
```python
import litellm
litellm.cache = litellm.Cache(type="local")
```
Pour la production (partagé entre plusieurs serveurs), on utilise Redis :
```python
litellm.cache = litellm.Cache(type="redis", host="localhost", port=6379)
```

## 💰 Optimisation des Coûts (FinOps LLM)

Quels sont les 3 leviers majeurs de réduction de coûts en production ? #flashcard
1. **Caching** : Ne jamais payer pour générer deux fois la même réponse.
2. **Model Routing Intelligent** : Envoyer dynamiquement les requêtes complexes vers des modèles "chers et intelligents" (GPT-4o, Claude 3.5 Sonnet) et les requêtes simples de formatage ou de traduction vers des modèles "petits et économiques" (GPT-4o-mini, Haiku, Llama3-8B).
3. **Réduction du Prompt Bloat** : Optimiser la taille des messages envoyés au modèle.

Qu'est-ce que le "Prompt Bloat" et comment le réduire ? #flashcard
Le "Prompt Bloat" est la mauvaise habitude d'envoyer trop d'informations inutiles au LLM (ex: des instructions sur-détaillées, ou un historique de conversation de 50 messages) ce qui fait exploser les coûts de tokens en entrée (Input Tokens). 
**Techniques de réduction :**
- Limiter l'historique de chat aux N derniers messages (ex: Fenêtre glissante).
- Demander à un petit LLM de résumer régulièrement l'historique complet en un court paragraphe.
- En RAG, filtrer strictement les chunks de contexte non-pertinents avant de les insérer dans le prompt.
