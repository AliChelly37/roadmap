# Mémo S2-J1 : Fondations du Prompt Engineering (Anthropic)

Ce mémo résume les concepts clés appris dans les chapitres 1 à 5 du tutoriel interactif de Prompt Engineering d'Anthropic. Ces principes forment la base pour obtenir des résultats fiables, structurés et prévisibles avec n'importe quel grand modèle de langage (LLM).

---

## 1. Structure Basique et Clarté (Chapitres 1 & 3)

Un bon prompt ne laisse pas de place à l'interprétation. Les LLMs ne lisent pas dans les pensées.
- **Être spécifique :** Au lieu de "Écris un poème sur la mer", utiliser "Écris un poème de 4 lignes sur la mer en utilisant des rimes croisées (ABAB)."
- **Montrer plutôt que dire :** Donner des exemples (few-shot) est souvent plus efficace que de donner de longues descriptions de ce qui est attendu.
- **Le contexte est roi :** Toujours fournir le contexte nécessaire à la prise de décision.

## 2. Le System Prompt (Chapitre 2)

Le *System Prompt* définit le cadre global dans lequel le modèle va opérer. Il est lu avant le message de l'utilisateur.
- **Persona / Rôle :** Dire au modèle *qui* il est ("Tu es un expert en cybersécurité...", "Tu es un correcteur orthographique intraitable..."). Cela l'aide à adopter le bon ton et le bon vocabulaire.
- **Règles absolues :** C'est le bon endroit pour définir des règles strictes ("Ne réponds qu'en JSON", "Ne justifie jamais tes réponses").

## 3. Séparation Données / Instructions avec les balises XML (Chapitre 4)

L'un des plus grands défis est d'empêcher le modèle de confondre tes instructions avec les données fournies par l'utilisateur (ce qui peut mener à l'échec ou à des failles comme l'injection de prompt).
- Anthropic recommande fortement l'utilisation de **balises XML** (`<doc>`, `<instructions>`, `<user_input>`) pour délimiter clairement les différentes parties du prompt.
- **Exemple :**
  ```xml
  Voici un document à résumer :
  <document>
  Le texte du document va ici...
  </document>
  
  Instructions : Résume le texte ci-dessus en 3 points clés.
  ```

## 4. Formatage et Extraction (Chapitre 3 & 5)

Demander un format spécifique permet d'intégrer le LLM dans un pipeline logiciel classique.
- **Pré-remplir la réponse (Prefilling) :** Claude et d'autres LLMs modernes permettent de forcer le début de la réponse de l'assistant. Par exemple, terminer le prompt par `{` ou `<output>` force le LLM à commencer directement par générer le JSON ou le format voulu, évitant les phrases comme "Voici votre JSON :".

## 5. Décomposition de Tâches (Task Decomposition) (Chapitre 5)

Les LLMs ont du mal à résoudre un problème complexe en une seule étape.
- **Casser la complexité :** Diviser une tâche large en une séquence de sous-tâches (ex: 1. Extraire les faits, 2. Analyser les faits, 3. Rédiger la synthèse).
- Cela permet au modèle de traiter chaque partie avec plus de précision et réduit drastiquement les hallucinations.

## 6. Paradigmes de Prompting (promptingguide.ai)

Ces trois techniques fondamentales dictent la manière dont le modèle aborde la tâche :
- **Zero-Shot Prompting :** Demander au modèle de réaliser une tâche sans lui fournir d'exemples préalables. Utile pour les tâches générales où le modèle a déjà une bonne compréhension (ex: traduire une phrase basique).
- **Few-Shot Prompting :** Fournir au modèle quelques exemples (input/output) dans le prompt avant de poser la question finale. Indispensable pour forcer le modèle à adopter un ton spécifique, à utiliser un format de sortie particulier (ex: JSON avec certaines clés) ou à comprendre une logique de classification inhabituelle.
- **Chain-of-Thought (CoT) Prompting :** Demander explicitement au modèle de "réfléchir étape par étape" ("Think step by step") avant de donner sa réponse finale. Cela pousse le modèle à générer un raisonnement intermédiaire, ce qui augmente considérablement ses performances sur les problèmes logiques, mathématiques ou de réflexion complexe, car cela lui donne le temps (sous forme de tokens générés) de structurer sa pensée.

## 7. Techniques Avancées (Anthropic Chapitres 6 à 9)

Les derniers chapitres du tutoriel Anthropic poussent plus loin le contrôle du modèle :
- **Pensée préalable (Precognition / Thinking) :** Demander au LLM de réfléchir dans des balises `<thinking>` avant de donner sa réponse finale dans des balises `<answer>`. Cela permet de "cacher" le raisonnement si besoin (en post-processing) tout en forçant le modèle à planifier sa réponse. C'est l'application concrète du Chain-of-Thought adaptée au format Anthropic.
- **Éviter les hallucinations (Garde-fous) :** Donner explicitement une "porte de sortie" au modèle. Par exemple : *"Si l'information n'est pas dans le texte, réponds exactement 'Je ne sais pas' au lieu d'inventer une réponse."*
- **Combinaison de techniques :** Les prompts les plus performants en production combinent généralement : un System Persona + des balises XML pour les données + des exemples Few-Shot + une demande de réflexion dans des balises `<thinking>` + un prefilling pour forcer le format de sortie.

## 8. Concepts Avancés pour Systèmes IA (promptingguide.ai)

- **Self-Consistency (Cohérence interne) :** Technique utilisée pour améliorer drastiquement les performances sur les tâches logiques et mathématiques. Plutôt que de demander au modèle de raisonner une seule fois (où il pourrait faire une erreur d'inattention), on lui demande de générer plusieurs chemins de raisonnements différents (ex: 5 essais avec une légère "température"). Un script sélectionne ensuite la conclusion finale qui apparaît le plus souvent (vote majoritaire).
- **ReAct (Reason + Act) :** C'est le pattern fondamental pour créer des "Agents Autonomes". Le LLM alterne entre 3 étapes : **Pensée** (analyser ce qu'il faut faire), **Action** (demander à utiliser un outil externe comme une calculatrice ou le web), et **Observation** (lire le retour de l'outil injecté par le code). Cela permet au modèle de compenser ses faiblesses (manque de connaissances récentes, mauvais en calcul mathématique) en interagissant avec l'extérieur.

---
*Ces techniques transforment l'interaction avec un LLM : on passe d'une "discussion" incertaine à une "programmation en langage naturel" robuste.*
