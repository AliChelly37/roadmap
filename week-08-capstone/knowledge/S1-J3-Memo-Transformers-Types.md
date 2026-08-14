# Modèles Encoder vs Decoder (Transformers)

**Subject/Roadmap:** [[PROGRESS_TRACKER]]
**Date learned:** 2026-07-12
**Status:** 🌱 new

## Core idea (my own words)
- **Encoder (ex: BERT)** : Analyse toute la phrase en même temps (bidirectionnel). Idéal pour *comprendre* le texte (classification, analyse de sentiment, spam).
- **Decoder (ex: GPT, Llama)** : Analyse les mots précédents pour prédire le suivant (unidirectionnel). Idéal pour *générer* du texte.
- **Sequence-to-Sequence (ex: T5, BART)** : Combine les deux. Un encoder lit l'entrée, un decoder génère la sortie. Idéal pour la traduction ou le résumé.

## Why it matters / when I'd use it
- En AI Engineering, si je veux construire un chatbot, j'utilise un Decoder (Llama, GPT). Si je veux trier des millions de documents internes par catégorie sans générer de texte, un Encoder (BERT) est souvent beaucoup plus rapide et plus précis.

## Flashcards
#flashcard
Q: Quelle est la différence principale entre un modèle Encoder (ex: BERT) et un modèle Decoder (ex: GPT) ?
A: L'**Encoder** excelle dans la *compréhension* du texte (classification) car il analyse toute la phrase d'un coup. Le **Decoder** excelle dans la *génération* de texte car il prédit le mot suivant de façon séquentielle.

#flashcard
Q: Dans quelle catégorie de modèles se situent ChatGPT et Llama ?
A: Ce sont des modèles **Decoder-only** (Auto-regressifs), optimisés pour la génération et la prédiction du token suivant.

#flashcard
Q: Quel type d'architecture Transformer utiliseriez-vous pour une tâche de traduction automatique (Anglais -> Français) ?
A: Un modèle **Sequence-to-Sequence** (Encoder-Decoder), car l'Encoder peut comprendre la phrase complète en anglais, et le Decoder peut ensuite générer la phrase en français.

## Links
- [[S1-J1-Memo-Transformer]]
