# 📝 Mémo S4-J2 : Stratégies de Chunking pour le RAG

*Ce document valide les tâches `S4-J2-T1` à `S4-J2-T4`.*

---

## 1. L'importance du Chunking
Le découpage en morceaux (chunking) consiste à diviser un document long en segments de taille contrôlée avant de les vectoriser. 
*   **Pourquoi découper ?** Les modèles d'embedding ont une limite de tokens (contexte) et peinent à capturer les détails fins d'un document complet. Un unique vecteur pour 10 pages dilue les informations spécifiques. Le chunking permet de conserver des "unités sémantiques" distinctes et ciblées.

---

## 2. Les 5 Niveaux de Découpage de Texte (Text Splitting)
Selon le framework de Greg Kamradt, il existe cinq niveaux de sophistication pour découper le texte :

1.  **Niveau 1 : Découpage par caractères (Character Splitting)** :
    *   Découpe bêtement à un nombre fixe de caractères (ex: tous les 500 caractères).
    *   *Problème* : Coupe souvent les mots ou les phrases en plein milieu.
2.  **Niveau 2 : Découpage récursif (Recursive Character Splitting)** :
    *   Utilise une liste ordonnée de séparateurs (`["\n\n", "\n", " ", ""]`).
    *   *Principe* : Tente de couper d'abord au niveau des paragraphes, puis des phrases, et enfin des mots si la taille limite est dépassée. Permet de garder le contexte des paragraphes intact.
3.  **Niveau 3 : Découpage spécifique au document (Document Specific Splitting)** :
    *   Découpe selon la structure native du document (ex: par en-têtes Markdown `#`, ou mots-clés syntaxiques Python `class`/`def` pour du code). Évite de casser des structures logiques.
4.  **Niveau 4 : Découpage sémantique (Semantic Splitting)** :
    *   Calcule l'embedding de chaque phrase et mesure la distance cosinus entre phrases consécutives (`Distance = 1 - CosineSimilarity`).
    *   *Fonctionnement* : Une coupure est créée lorsque la distance dépasse un seuil dynamique (`moyenne + 1.2 * ecart_type` des écarts de tout le document), signalant un changement de sujet.
5.  **Niveau 5 : Découpage agentique (Agentic Splitting)** :
    *   Utilise un LLM pour lire le document et décider de l'emplacement optimal des découpes. Très précis mais extrêmement lent et coûteux pour de larges volumes de données (non-déterministe).

---

## 3. Paramètres clés : Chunk Size & Chunk Overlap
*   **Chunk Size** : La taille maximale ciblée pour chaque morceau.
*   **Chunk Overlap (Recouvrement)** : La quantité de texte partagée entre la fin d'un chunk et le début du suivant (ex: taille 500, overlap 100).
    *   *Rôle de l'overlap* : Empêche la perte de contexte pour les phrases coupées en deux sur la frontière d'un chunk. Il assure une transition sémantique fluide entre les morceaux.

---

## 🧪 Travaux Pratiques Réalisés
Nous avons implémenté le script [chunk_and_index.py](../../week-04-rag-chat-docs/chunk_and_index.py) :
*   Chargement de `document_test.pdf` via PyMuPDF.
*   Découpage récursif avec `RecursiveCharacterTextSplitter` (size=500, overlap=100) en conservant les métadonnées de page.
*   Chaque page a été découpée de manière propre en 2 chunks (6 chunks au total).
*   Indexation réussie des 6 morceaux dans Chroma DB (`rag_document_test`) avec le modèle E5-Multilingual.

---

## Flashcards (Anki / Active Recall)

#flashcard
Q: Pourquoi l'ordre des séparateurs dans le `RecursiveCharacterTextSplitter` de LangChain est-il important ?
A: Parce qu'il commence par essayer de couper sur les plus grands blocs de sens (paragraphes `\n\n`), puis descend aux phrases (`\n`), et n'utilise les espaces (` `) qu'en dernier recours pour ne pas séparer les mots d'un paragraphe si possible.

#flashcard
Q: Quel est le rôle de l'overlap (recouvrement) lors du découpage de texte pour le RAG ?
A: Il copie une partie de la fin d'un chunk au début du suivant pour préserver la continuité sémantique et éviter de couper des informations importantes qui se trouvent à la frontière de deux morceaux.

#flashcard
Q: Comment fonctionne le découpage sémantique (Semantic Splitting) ?
A: Il calcule la distance cosinus entre les embeddings de chaque phrase consécutive. Il crée un nouveau chunk uniquement lorsque la distance franchit un seuil statistique, indiquant un changement de sujet (topic shift).

#flashcard
Q: Quel est l'inconvénient majeur du découpage agentique (Agentic Splitting) ?
A: Son coût très élevé (appels API LLM répétés), sa lenteur d'exécution sur de gros volumes, et son caractère non-déterministe (deux exécutions peuvent générer des découpes différentes).
