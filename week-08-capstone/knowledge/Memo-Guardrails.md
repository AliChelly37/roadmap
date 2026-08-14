# 📝 Mémo : Guardrails (Garde-fous) dans les Systèmes IA

Ce mémo résume les concepts, architectures et frameworks pour sécuriser et contrôler les entrées et sorties des applications basées sur les LLMs.

---

## 1. Qu'est-ce que les Guardrails ?

Les **Guardrails (Garde-fous)** sont des couches logicielles intermédiaires placées en amont (input) et en aval (output) du LLM pour garantir que l'application reste sécurisée, polie, factuelle et conforme aux spécifications.

```
                   ┌──────────────┐
                   │ Entrée User  │
                   └──────┬───────┘
                          │
            [1. Input Guardrails (Sécurité/PII)]
                          │
                          ▼
                   ┌──────────────┐
                   │     LLM      │
                   └──────┬───────┘
                          │
            [2. Output Guardrails (Format/Fidélité)]
                          │
                          ▼
                   ┌──────────────┐
                   │ Réponse Finale│
                   └──────────────┘
```

---

## 2. Les Différents Types de Garde-fous

### 1. Guardrails d'Entrée (Input Guardrails)
Filtrent la requête de l'utilisateur avant qu'elle n'atteigne le modèle :
*   **Détection d'Injections de Prompts (Prompt Injections)** : Bloquer les tentatives de détournement des consignes système (ex. *"Ignore les consignes précédentes et donne-moi..."*).
*   **Filtre de Confidentialité (PII - Personally Identifiable Information)** : Masquer ou anonymiser les données sensibles (noms, cartes bancaires, adresses).
*   **Modération** : Bloquer les requêtes haineuses, violentes ou sexuellement explicites.

### 2. Guardrails de Sortie (Output Guardrails)
Valident la réponse générée par le LLM avant de l'afficher à l'utilisateur :
*   **Validation de Structure et de Schéma** : S'assurer que le LLM a généré un JSON ou XML 100% valide et conforme à un schéma précis (ex. Pydantic).
*   **Fidélité et Grounding (Anti-Hallucination)** : Valider que toutes les affirmations de la réponse sont strictement fondées sur le contexte fourni (RAG).
*   **Détection de Fuite de Prompt** : Empêcher le modèle de révéler ses instructions système secrètes.

### 3. Guardrails d'Exécution (Runtime Guardrails)
Gèrent la sécurité opérationnelle de l'agent en cours d'exécution :
*   **Iteration Limit (Limite de boucles)** : Couper l'exécution d'un agent ReAct s'il dépasse $N$ étapes (ex. max 4 itérations) pour éviter le gaspillage de tokens.
*   **Budget Limit (Coût financier)** : Arrêter les appels d'API si le coût cumulé d'une session dépasse un seuil en dollars.
*   **Isolation (Sandboxing)** : Exécuter le code généré par le LLM dans un environnement isolé (sandbox) pour ne pas corrompre la machine hôte.

---

## 3. Les Frameworks Majeurs du Marché

*   **Guardrails AI (`guardrails-ai`)** : Framework Python qui utilise des fichiers de configuration XML (`.co-rail`) ou des schémas Pydantic pour valider et corriger automatiquement les sorties du modèle (auto-correction en cas d'erreur de schéma).
*   **NeMo Guardrails (NVIDIA)** : Utilise un langage spécifique (Colang) pour définir des rails conversationnels stricts (ex. si l'utilisateur pose une question politique, dévier vers une réponse neutre prédéfinie).
*   **Llama Guard (Meta)** : Modèle de langage spécialisé (fine-tuné) agissant uniquement comme un classificateur de sécurité pour évaluer si une entrée ou une sortie est sûre.

---

## Flashcards (Anki / Active Recall)

#flashcard
Q: Quelle est la différence entre un "Input Guardrail" et un "Output Guardrail" ?
A: Un Input Guardrail valide et filtre la requête de l'utilisateur avant l'appel LLM (ex: prompt injection, PII). Un Output Guardrail valide et nettoie la réponse générée avant l'affichage (ex: format JSON, hallucinations).

#flashcard
Q: Pourquoi la détection d'itérations maximales est-elle un garde-fou d'exécution critique pour un agent ReAct ?
A: Pour éviter que l'agent ne reste bloqué dans une boucle infinie de réflexion ou d'auto-critique, ce qui consommerait rapidement votre budget financier et saturerait les serveurs.

#flashcard
Q: Quel est le rôle principal du framework Guardrails AI ?
A: Valider la structure et la qualité des sorties LLM par rapport à des schémas stricts (comme Pydantic) et relancer automatiquement des requêtes de correction en cas d'échec de validation.
