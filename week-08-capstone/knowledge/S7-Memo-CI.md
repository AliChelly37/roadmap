# 🧪 Mémo : Évaluation Continue (CI) et Tests (Semaine 7 - J5)

Ce mémo résume l'importance de tester continuellement les performances d'une application IA pour garantir sa fiabilité en production.

## 🎯 Concepts Clés

Qu'est-ce que l'Intégration Continue (CI) appliquée aux LLMs ? #flashcard
C'est un processus automatisé qui déclenche une batterie de tests (un Eval Set) à chaque modification du code, du prompt, ou du modèle d'IA. Si les performances de l'IA chutent par rapport aux attentes, le système bloque automatiquement la mise en production pour éviter un incident.

Qu'est-ce qu'une Régression en IA ? #flashcard
C'est une baisse soudaine de la qualité des réponses de l'IA, souvent causée par une modification humaine (ex: un développeur modifie le "System Prompt" pour ajouter une fonctionnalité, ce qui rend l'IA confuse et lui fait rater des tâches basiques qu'elle réussissait avant).

Qu'est-ce qu'un "Eval Set" (Jeu d'évaluation) ? #flashcard
C'est une liste de questions de référence couplées aux réponses (ou mots-clés) attendues. C'est la boussole du projet. Ex : 
- Q: "Quelle est la capitale de la France ?" 
- Attendue: [Doit contenir "Paris"]

## 🛠️ Outils et Implémentation

Pourquoi préfère-t-on des outils de CI automatisés (comme GitHub Actions) plutôt que des tests manuels ? #flashcard
Parce qu'une application IA est probabiliste. Une modification mineure du prompt peut avoir des effets papillon imprévisibles sur des dizaines de cas d'usage. Il est humainement impossible de retester manuellement des centaines de questions à chaque changement de code. L'automatisation garantit une couverture constante.

Quel est l'intérêt du "Red-Teaming" automatisé (Bonus) ? #flashcard
Plutôt que d'attendre qu'un vrai pirate attaque l'application, on utilise un outil (comme `promptfoo` ou un script Python) qui va générer automatiquement des centaines d'injections de prompt malveillantes ("Ignore tes instructions...") pour vérifier si les garde-fous résistent à un bombardement d'attaques variées.
