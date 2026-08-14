# 🧱 Semaine 1 — Fondations LLM & stack moderne

**📍 Partie 1 / 9** · Phase : 🧱 *Fondations* · Charge : **~20 h** (5 jours × ~4 h)
**🎯 Livrable de la semaine :** un **« LLM Playground » en Python** qui parle à ≥2 fournisseurs, renvoie une **sortie structurée** validée et exécute un **outil (function calling)**.

> 🔄 **Refresh éclair (si un prérequis est fragile) :**
> - Variables d'env & `.env` → cherche « python-dotenv quickstart » ⏱️ ~10 min
> - JSON ↔ objets Python → revois `json.loads` / `json.dumps` ⏱️ ~10 min
> - Async (utile dès le streaming) → notion de `async`/`await`, pas bloquant cette semaine

---

## 🎯 Objectifs

À la fin de la semaine, tu sais :
- Expliquer **comment fonctionne un LLM** (tokenisation, fenêtre de contexte, inférence, hallucinations) sans hand-waving.
- Appeler **plusieurs LLM** (1 frontier via API + 1 modèle open en local) derrière **une interface unifiée**.
- Régler les **paramètres clés** (température, max tokens, system prompt) et savoir ce qu'ils changent.
- Forcer des **sorties structurées fiables** (JSON validé par Pydantic) plutôt que du texte libre à parser.
- Faire **appeler un outil** au modèle (*function calling / tool use*) et exploiter le résultat.

---

## 🧩 Concepts clés

- **Tokenisation** (BPE), vocabulaire, pourquoi « compter les lettres » est dur pour un LLM
- **Fenêtre de contexte**, tokens d'entrée/sortie, coût ≈ tokens
- **Inférence** : prédiction du token suivant, échantillonnage, **température** / top-p
- **Rôles de messages** : `system` / `user` / `assistant`
- **API propriétaire vs modèle open** (local) : arbitrages coût / privacy / contrôle
- **Structured outputs** : JSON mode, schémas, validation **Pydantic**, librairie **Instructor**
- **Tool use / function calling** : déclarer un schéma d'outil → le modèle décide → tu exécutes → tu renvoies le résultat
- **Sécurité de base** : clés dans `.env`, jamais commitées

---

## 📚 Ressources gratuites

> Légende : 📄 cours · 📖 doc · 🎥 vidéo · 📝 article · 🛠️ playground · 🎓 accès API gratuit | 🟢 fonda. · 🟡 intermédiaire · 🔴 avancé · ⭐ incontournable

### Modèle mental (à voir/lire en J1)
- 🎥 ⭐ **Andrej Karpathy — « [1hr Talk] Intro to Large Language Models »** 🟢 ⏱️ ~1 h — la meilleure vue d'ensemble. Chaîne : `youtube.com/@AndrejKarpathy` (cherche le titre exact)
- 🎥 🔴 *(optionnel, approfondi)* **Karpathy — « Deep Dive into LLMs like ChatGPT »** ⏱️ ~3,5 h — version mirror avec chapitres horodatés : `classcentral.com/course/youtube-deep-dive-into-llms-like-chatgpt-428188`
- 📝 ⭐ **Jay Alammar — The Illustrated Transformer** 🟡 ⏱️ ~45 min — `jalammar.github.io/illustrated-transformer/`
- 🎥 **3Blue1Brown — « Attention in transformers, visually explained »** 🟡 ⏱️ ~26 min — chaîne : `youtube.com/@3blue1brown`
- 🛠️ ⭐ **Tiktokenizer** — visualise la tokenisation en direct 🟢 — `tiktokenizer.vercel.app`

### Cours structurés (étalés sur la semaine)
- 📄 ⭐ **Hugging Face — LLM Course**, chapitres 1–2 pour cette semaine 🟡 ⏱️ ~6 h/ch. — `huggingface.co/learn/llm-course`
- 📄 **Maxime Labonne — LLM Course** (parcours + notebooks) 🟡 — `github.com/mlabonne/llm-course`

### Docs officielles (référence pendant le code)
- 📖 ⭐ **Anthropic — Get started & Tool use** 🟡 — `platform.claude.com/docs` (→ *Build with Claude* → *Tool use*)
- 📖 **OpenAI — Function calling & Structured outputs** 🟡 — `developers.openai.com/api/docs` (→ *Guides*)
- 📖 **Google AI for Developers — Gemini API quickstart** 🟢 — `ai.google.dev/gemini-api/docs`
- 📖 **Ollama — Quickstart** 🟢 — `ollama.com` (et `github.com/ollama/ollama`)
- 📖 **Pydantic — Models** 🟢 — `docs.pydantic.dev`
- 📖 ⭐ **Instructor — Getting started** (structured outputs en pratique) 🟡 — `python.useinstructor.com`

### 🎓 Accès LLM gratuit (pour rester à 0 €)
- **Google AI Studio (Gemini 2.5 Flash)** — ~1 500 req/jour, contexte 1M, **sans carte** — `aistudio.google.com`
- **Groq** — inférence ultra-rapide sur modèles open (Llama/Qwen…), **sans carte** — `console.groq.com`
- **OpenRouter** — 1 clé, 28+ modèles gratuits (suffixe `:free`) — `openrouter.ai`
- ⚠️ **OpenAI & Anthropic** : l'**API** exige une carte (pas de tier gratuit permanent). Leur **chat** reste gratuit (`claude.ai`, `chatgpt.com`). Tu peux faire toute la semaine avec Gemini + Groq + Ollama.

---

## 💻 Repos GitHub (à lire / forker)

- 💻 ⭐ **`anthropics/anthropic-cookbook`** — recettes *tool use* & sorties structurées
- 💻 ⭐ **`openai/openai-cookbook`** — recettes *function calling* & *structured outputs*
- 💻 ⭐ **`instructor-ai/instructor`** — extraction structurée multi-providers
- 💻 **`ollama/ollama`** — exécuter des modèles en local
- 💻 **`mlabonne/llm-course`** — notebooks pédagogiques
- 💻 **`HandsOnLLM/Hands-On-Large-Language-Models`** — notebooks (gratuits) du livre *Hands-On LLMs*
- 💻 **`cheahjs/free-llm-api-resources`** — liste **à jour** des APIs LLM gratuites et de leurs quotas

---

## 🛠️ Projet / Livrable : « LLM Playground » (CLI Python)

🎯 Construis un petit outil en ligne de commande qui démontre les 3 piliers de la semaine.

**Cahier des charges (Definition of Done) :**
1. **Multi-provider** — une fonction `chat(prompt, provider=...)` qui parle à **≥2 fournisseurs** parmi : Gemini (API), Groq (API), un modèle **Ollama local**. Interface identique quel que soit le backend.
2. **Sortie structurée** — au moins une tâche renvoie un objet **Pydantic** validé (ex. extraire `{titre, entreprise, compétences[], séniorité}` depuis une offre d'emploi collée en texte). Utilise **Instructor** ou le JSON mode natif.
3. **Function calling** — déclare **≥1 outil** que le modèle peut appeler (ex. `get_current_weather(city)` ou une calculatrice), exécute l'appel, et renvoie le résultat au modèle pour la réponse finale.
4. **Sécurité & repo** — clés dans `.env` (+ `.env` dans `.gitignore`), code poussé dans `ai-engineer-roadmap/week-01-llm-playground/` avec un **README** (installation, usage, exemples).

**🌟 Bonus (si tu as de l'avance) :**
- Log des **tokens & coût estimé** par appel.
- Ajout d'un **3ᵉ provider** ou bascule auto si quota atteint (preview du *routing* de S7).
- Premier essai de **streaming** de la réponse (transition douce vers S2).

---

## 🗓️ Plan jour par jour

> Format des IDs : `S1-J{jour}-T{tâche}`. Durées indicatives, à re-répartir selon ton temps réel. 🧪 = tâche de code.

### J1 — Modèle mental des LLM *(~4 h)*
- [ ] **S1-J1-T1** — Visionner Karpathy « Intro to LLMs » (1 h) ⏱️ ~1 h
- [ ] **S1-J1-T2** — Lire *The Illustrated Transformer* + jouer avec **Tiktokenizer** (colle 3-4 phrases, observe les tokens) ⏱️ ~1 h
- [ ] **S1-J1-T3** — Vidéo 3Blue1Brown sur l'attention ⏱️ ~30 min
- [ ] **S1-J1-T4** — 🧪 Rédiger dans ton journal un **mémo perso** (½ page) : tokenisation, contexte, température, hallucinations ⏱️ ~30 min
- [ ] **S1-J1-T5** — *(optionnel 🔴)* commencer le « Deep Dive » de Karpathy ⏱️ ~1 h

### J2 — Setup & premier appel API *(~4 h)*
- [ ] **S1-J2-T1** — 🧪 Terminer la **checklist S0** (env, repo, clés Gemini/Groq, Ollama) si pas déjà fait ⏱️ ~45 min
- [ ] **S1-J2-T2** — Lire le **quickstart Gemini** + créer une clé sur AI Studio ⏱️ ~30 min
- [ ] **S1-J2-T3** — 🧪 Premier appel API à **Gemini** (message simple, lire la réponse) ⏱️ ~45 min
- [ ] **S1-J2-T4** — 🧪 Premier appel à **Groq** (modèle Llama/Qwen) ⏱️ ~45 min
- [ ] **S1-J2-T5** — 🧪 Expérimenter **température / max tokens / system prompt** : comparer 2-3 réglages ⏱️ ~45 min

### J3 — Modèles locaux & interface unifiée *(~4 h)*
- [ ] **S1-J3-T1** — 🧪 `ollama pull` d'un petit modèle (ex. Llama 3.x 8B ou Qwen) et le lancer en local ⏱️ ~45 min
- [ ] **S1-J3-T2** — HF LLM Course ch. 1 (transformers, `pipeline`) ⏱️ ~1 h 15
- [ ] **S1-J3-T3** — 🧪 Écrire une fonction `chat(prompt, provider)` unifiant **Gemini + Groq + Ollama** ⏱️ ~1 h 30
- [ ] **S1-J3-T4** — 🧪 Tester la même requête sur les 3 backends, noter les différences ⏱️ ~30 min

### J4 — Sorties structurées *(~4 h)*
- [ ] **S1-J4-T1** — Lire **Pydantic – Models** (l'essentiel) ⏱️ ~30 min
- [ ] **S1-J4-T2** — Lire **Instructor – Getting started** ⏱️ ~30 min
- [ ] **S1-J4-T3** — 🧪 🎯 Définir un modèle Pydantic `JobPosting` et **extraire** des champs depuis une offre d'emploi en texte ⏱️ ~1 h 30
- [ ] **S1-J4-T4** — 🧪 Rendre l'extraction **robuste** (validation, retry, champ manquant) ⏱️ ~1 h

### J5 — Function calling & assemblage *(~4 h)*
- [ ] **S1-J5-T1** — Lire **Tool use** (Anthropic) ou **Function calling** (OpenAI) + 1 recette du cookbook ⏱️ ~45 min
- [ ] **S1-J5-T2** — 🧪 🎯 Implémenter **1 outil** (`get_weather` ou calculatrice) et le faire appeler par le modèle ⏱️ ~1 h 30
- [ ] **S1-J5-T3** — 🧪 🎯 Assembler le **CLI final** (multi-provider + structured + tool) ⏱️ ~1 h
- [ ] **S1-J5-T4** — 🧪 Écrire le **README** et **pousser sur GitHub** ⏱️ ~45 min

---

## ✅ Critères de réussite (validation de la semaine)

- [ ] J'appelle **≥2 fournisseurs LLM** depuis un même script, via une interface unique.
- [ ] J'obtiens une **sortie structurée validée par Pydantic** (pas du parsing de texte fragile).
- [ ] Le modèle **appelle correctement ≥1 outil** et j'exploite le résultat.
- [ ] Mes **clés sont dans `.env`** et **jamais** commitées (`.env` est dans `.gitignore`).
- [ ] Le code est **sur GitHub** avec un README clair.
- [ ] Je peux **expliquer à voix haute** : tokenisation, fenêtre de contexte, température, et la différence entre *structured output* et *tool calling*.

> 🧭 **Auto-éval rapide :** si tu cales sur l'un de ces points, ce n'est pas grave — note-le dans ton journal. Le second brain peut transformer chaque point manquant en tâche de rattrapage pour le week-end.

---

## 🔜 Suite

➡️ **Partie 2 — Semaine 2 : Prompt engineering & premières apps LLM** — prompting avancé (CoT, few-shot, ReAct), templating, première **API FastAPI** avec **streaming**, et bases de l'évaluation. Tu réutiliseras directement ton « LLM Playground » de cette semaine.

---

*Partie 1 d'un guide en 9 parties. Liens vérifiés en juin 2026 — les quotas des offres gratuites changent souvent, vérifie les chiffres avant de t'appuyer dessus (repo `cheahjs/free-llm-api-resources` pour le suivi).*
