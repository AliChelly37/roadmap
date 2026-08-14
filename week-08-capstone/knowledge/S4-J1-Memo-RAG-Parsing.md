# 📝 Mémo S4-J1 : Architecture RAG & Parsing PDF

*Ce document valide les tâches `S4-J1-T1` à `S4-J1-T4`.*

---

## 1. L'Architecture RAG (Retrieval-Augmented Generation)
Le RAG résout le problème des hallucinations des LLMs et de leur manque de connaissances récentes en leur fournissant un "livre ouvert" contenant des documents pertinents au moment de générer la réponse.

### Les Deux Phases du RAG
1.  **Phase Offline (Ingestion & Indexation)** :
    *   S'exécute à l'avance (une fois ou périodiquement), sans interaction utilisateur directe.
    *   **Étapes** : Ingestion du document (PDF/HTML) $\rightarrow$ Découpage en morceaux (Chunking) $\rightarrow$ Vectorisation (Embedding) $\rightarrow$ Stockage dans une base vectorielle (Chroma/Qdrant).
2.  **Phase Online (Recherche & Génération)** :
    *   S'exécute en temps réel à chaque requête de l'utilisateur.
    *   **Étapes** : L'utilisateur pose une question $\rightarrow$ Vectorisation de la question $\rightarrow$ Recherche des morceaux les plus proches (Retrieval) $\rightarrow$ Insertion des morceaux dans le prompt (Augmentation) $\rightarrow$ Appel au LLM pour rédiger la réponse (Génération).

---

## 2. Le Concept de "Grounding" (Ancrage)
Le grounding consiste à restreindre la réponse du LLM **uniquement** aux informations fournies dans le contexte du prompt.

*   **Le Prompt de Grounding** : On utilise des instructions système claires (ex. *"Réponds uniquement à l'aide du contexte fourni, si l'information n'est pas dedans dis 'je ne sais pas'"*) et on délimite le contexte à l'aide de balises structurales (comme des balises XML `<context>...</context>`).
*   **Résultat** : Le LLM passe d'un rôle d'écrivain (génération de mots probables à partir de sa mémoire) à un rôle de **lecteur/synthétiseur**, éliminant presque entièrement les hallucinations factuelles.

---

## 3. Le Parsing de Fichiers PDF
Le format PDF est complexe car il a été conçu pour l'impression physique et non pour l'extraction de texte structuré. Il ne contient pas de notions de paragraphes ou de tableaux natifs, mais seulement des coordonnées géométriques de caractères sur une page.

*   **PyMuPDF (`fitz`)** :
    *   **Forces** : Extrêmement rapide, léger, parfait pour extraire le texte brut des PDFs dits "textuels" (générés numériquement).
    *   **Faiblesses** : Perde la notion de structure sur les documents complexes (doubles colonnes, tableaux complexes).
*   **Docling (IBM)** :
    *   **Forces** : Analyseur basé sur des modèles de deep learning qui comprend la mise en page (*layout-aware*). Il extrait les tableaux et les structures complexes directement sous forme de Markdown propre.
    *   **Faiblesses** : Lourd, lent à s'exécuter, télécharge des poids de modèles neuronaux importants.

---

## 4. Propagation des Métadonnées pour les Citations
Pour qu'un système RAG soit fiable, il doit pouvoir **citer ses sources** (ex: *"D'après le document_test.pdf à la page 2..."*).
*   **La contrainte** : Lors de l'indexation, les pages sont découpées en dizaines de petits morceaux (chunks). Si nous ne copions pas le chemin du fichier (`source`) et le numéro de page (`page_number`) dans le dictionnaire `metadata` de **chaque chunk individuel**, cette information d'origine est définitivement perdue au moment de la recherche vectorielle.

---

## Flashcards (Anki / Active Recall)

#flashcard
Q: Quelle est la différence entre la phase Offline et Online du RAG ?
A: La phase Offline pré-traite les documents (lecture, découpage, stockage vectoriel). La phase Online traite la requête en temps réel (recherche de contexte et génération de la réponse par le LLM).

#flashcard
Q: Comment fonctionne le "grounding" pour réduire les hallucinations d'un LLM ?
A: Il force le LLM à répondre exclusivement à partir d'un contexte de faits délimité (ex: balises XML) inséré dans son prompt, avec consigne stricte de dire "Je ne sais pas" si l'info est absente.

#flashcard
Q: Pourquoi l'extraction de texte à partir de PDFs est-elle techniquement difficile ?
A: Parce que le PDF est conçu pour la mise en page visuelle (coordonnées de caractères sur une page) et ne contient pas de structure sémantique native (pas de marqueurs de paragraphes, de colonnes ou de cellules de tableaux).

#flashcard
Q: Pourquoi est-il indispensable de copier les métadonnées (nom du fichier, page) sur chaque chunk individuel ?
A: Car après le découpage, les morceaux de texte sont stockés indépendamment dans la base vectorielle. Sans cette copie, il serait impossible de remonter à la source exacte pour afficher des citations vérifiables.
