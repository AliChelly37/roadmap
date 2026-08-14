# 📝 Mémo S1-J1 : Fondations LLM (Karpathy)

*Ce document valide la tâche `S1-J1-T4`.*

## 1. L'anatomie d'un LLM
Un modèle comme LLaMA-2 70B se résume fondamentalement à **deux fichiers** :
- **Un fichier de paramètres (les poids)** : ex. 140 Go de nombres (les paramètres du réseau de neurones). C'est le "cerveau" compressé.
- **Un fichier d'exécution (le code)** : ex. ~500 lignes de C. C'est le moteur qui prend les poids et génère le texte. 

## 2. Les deux étapes de création d'un Assistant
- **Pre-training (Étape 1)** : Entraînement sur une énorme portion d'Internet avec un objectif très simple : **prédire le prochain mot**. C'est une compression "avec perte" (*lossy compression*) d'Internet. Le modèle apprend énormément de connaissances du monde, mais à ce stade, c'est juste un générateur de pages web (si on lui pose une question, il génère souvent plus de questions).
- **Fine-tuning (Étape 2)** : L'alignement. On lui donne des milliers de documents d'exemples "Question/Réponse" parfaits (souvent écrits par des humains) pour lui apprendre à adopter la forme d'un Assistant utile. C'est là qu'il devient capable de répondre intelligemment.

## 3. Hallucinations et "Rêves"
Puisque le modèle est une compression "lossy", il ne stocke pas les faits comme une vraie base de données. S'il lui manque une info précise, il va générer du texte qui *ressemble* à l'info correcte, statistiquement. Il "rêve" des documents Internet, ce qui crée des **hallucinations** (ex. inventer un faux code ISBN qui a parfaitement la bonne forme).

## 4. System 1 vs System 2
Inspiré de *Thinking, Fast and Slow* :
- **System 1** : Réflexe rapide, sans réflexion profonde (ex: 2+2=4). 
- **System 2** : Raisonnement lent, méthodique, arbre de décisions (ex: 17x24=?).
**Aujourd'hui, les LLMs n'ont que le System 1**. Ils crachent des mots un par un à vitesse constante, sans avoir de processus interne de "réflexion" ou d'ajustement avant de répondre. C'est le prochain grand défi de l'IA.

## 5. Le LLM comme OS (Système d'Exploitation)
Il ne faut pas voir le LLM comme un simple "chatbot", mais comme le noyau (Kernel) d'un OS émergeant :
- **Mémoire RAM** = La fenêtre de contexte.
- **Disque dur / Internet** = Le navigateur web, la RAG (fichiers locaux).
- **Outils** = Exécution de code Python, Calculatrice.
Le LLM coordonne tous ces outils pour résoudre des problèmes, exactement comme un système d'exploitation.

## 6. Scaling Laws (Lois d'échelle)
La performance d'un LLM (sa précision à prédire le prochain mot) est une fonction mathématique lisse et prédictible basée sur deux variables : **N** (le nombre de paramètres) et **D** (la quantité de texte). L'industrie investit massivement dans la puissance de calcul car la progression des modèles est "garantie" en augmentant ces deux facteurs.

## 7. Tool Use & Multimodalité
Les modèles récents ne se contentent plus de générer du texte dans le vide. Ils sont capables de faire appel à des outils externes (recherche web, calculatrice, exécution de code Python) et intègrent la multimodalité (voir des images, entendre, parler).

## 8. RLHF (Étape 3 du Fine-Tuning)
Au-delà de l'apprentissage par imitation (Stage 2), il existe une 3e étape utilisant des "étiquettes de comparaison". Il est souvent plus facile pour un humain d'évaluer la meilleure réponse parmi plusieurs générées par le modèle que d'écrire la réponse parfaite de zéro.

## 9. Le défi de l'auto-amélioration (Self-Improvement)
Contrairement à AlphaGo qui a pu s'auto-améliorer en jouant des millions de parties contre lui-même (car la condition de victoire est binaire et claire), le langage n'a pas de fonction de récompense simple. Découvrir comment un LLM peut s'auto-améliorer de façon générale est l'un des plus grands défis actuels.

---
## Flashcards
#flashcard
Q: L'anatomie d'un LLM comme LLaMA 2 se résume à 2 fichiers. Lesquels, et que font-ils ?
A: 1. Le fichier des paramètres/poids (~140Go) : le cerveau compressé. 2. Le fichier d'exécution (code C) : le moteur d'inférence qui fait tourner le réseau neuronal et ne fait aucun entraînement.

#flashcard
Q: Quelle est la différence fondamentale entre le Pre-training et le Fine-tuning ?
A: Le Pre-training apprend au modèle à prédire le prochain mot (compression d'Internet). Le Fine-tuning lui apprend le format d'Assistant via des exemples Q/A de haute qualité.

#flashcard
Q: Pourquoi un LLM a-t-il tendance à halluciner ?
A: Parce qu'il fonctionne comme une compression "avec perte" (lossy compression). Il ne stocke pas une base de données exacte de faits, donc s'il lui manque une info, il "rêve" statistiquement d'une réponse plausible.

#flashcard
Q: Dans l'analogie du "LLM OS" de Karpathy, que représente la RAM (mémoire vive) et pourquoi est-elle considérée comme "finie" ?
A: La RAM est la **fenêtre de contexte**. Elle est finie non pas seulement pour des raisons de coût, mais à cause de la limite architecturale du Transformer (le modèle ne peut mathématiquement traiter qu'un nombre maximal défini de tokens à la fois).

#flashcard
Q: Quelle est la différence entre le System 1 (actuel) et le System 2 (futur) pour les LLMs ?
A: System 1 : Le LLM génère des mots de façon instinctive et réflexe, à vitesse constante. System 2 : Permettre au modèle de "réfléchir" plus longtemps (explorer un arbre de possibilités) pour convertir du temps de calcul en précision.
