# L'Architecture Transformer & Tokens

**Subject/Roadmap:** [[PROGRESS_TRACKER]]
**Date learned:** 2026-07-12
**Status:** 🌱 new

## Core idea (my own words)
- Le Transformer utilise le "Self-Attention" pour comprendre le contexte d'un mot en calculant son association mathématique avec tous les autres mots de la phrase. 
- Les mots sont découpés en "tokens". Les tokens sont sensibles aux majuscules et aux espaces (" apple" ≠ "apple"), ce qui aide le modèle à situer le mot dans la phrase.

## Why it matters / when I'd use it
- L'attention multi-têtes (Multi-Headed Attention) permet de capter simultanément plusieurs types de relations grammaticales et sémantiques (ex: lier un pronom à un nom, et un verbe à un sujet).
- Comprendre que le LLM voit des tokens (et non des mots du dictionnaire) aide à formuler de meilleurs prompts.

## Flashcards
#flashcard
Q: Dans l'architecture Transformer, que représentent les matrices Query (Q), Key (K) et Value (V) dans le mécanisme d'attention ?
A: **Query** : ce que le mot cherche (ex: un nom singulier). **Key** : l'étiquette des autres mots (ex: je suis un nom singulier). **Value** : le sens réel du mot qui sera extrait si le match Q/K est fort.

#flashcard
Q: Pourquoi utilise-t-on la "Multi-Headed Attention" (attention multi-têtes) plutôt qu'une seule tête d'attention ?
A: Pour permettre au modèle d'analyser simultanément **plusieurs types de relations** dans une phrase (ex: une tête pour lier pronom/sujet, une autre pour verbe/adverbe).

#flashcard
Q: Pourquoi "apple", " Apple" et "APPLE" ont-ils des ID de tokens différents ?
A: Parce que la tokenisation prend en compte la casse et les espaces. Cela donne au modèle des indices syntaxiques cruciaux (ex: majuscule = début de phrase, espace = milieu de phrase).

#flashcard
Q: Mathématiquement, quelle opération est utilisée pour déterminer le score d'attention (le "match") entre un vecteur Query et un vecteur Key ?
A: Le **produit scalaire** (dot product). Plus les vecteurs sont alignés dans l'espace, plus le produit scalaire est élevé, ce qui signifie un score d'attention fort.

## Links
- [[S1-J1-Memo-Fondations-LLM]]
