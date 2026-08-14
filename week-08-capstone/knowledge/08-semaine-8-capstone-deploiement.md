# 🏁 Semaine 8 — Capstone, déploiement & portfolio

**📍 Partie 8 / 9** · Phase : 🚀 *Production* · Charge : **~20 h** (5 jours × ~4 h)
**🎯 Livrable de la semaine :** **UN projet end-to-end déployé** (RAG + agent + prod) avec **UI**, **Docker**, **lien public** et **writeup portfolio**.

> 🔄 **Refresh éclair (si un prérequis est fragile) :**
> - C'est une **semaine d'assemblage** : tu réutilises tes briques **S4–S7** (RAG, agent, tracing, garde-fous).
> - **Docker** (image, conteneur, ports, env) → cherche « docker get started » si besoin.
> - ⚠️ **Secrets** : sur un Space public, mets tes clés dans les **Secrets** de l'interface, **jamais** dans le code.

---

## 🎯 Objectifs

À la fin de la semaine (et de la roadmap !), tu sais :
- **Concevoir et livrer** un projet IA **end-to-end** (UI → API → agent/RAG → LLM + outils + observabilité).
- **Conteneuriser** ton app avec **Docker** (reproductible, déployable).
- **Déployer gratuitement** et obtenir un **lien public** (Hugging Face Spaces).
- Ajouter une **UI de démo** propre (Gradio / Chainlit / Streamlit).
- *(Optionnel)* Ajouter une **capacité multimodale** (voix via Whisper, ou vision).
- **Documenter pour un portfolio** crédible et **pitcher** ton projet.

---

## 🧩 Concepts clés

- **Architecture end-to-end** : `UI → API (FastAPI) → agent/RAG → LLM + outils + tracing/garde-fous`
- **Docker** : `Dockerfile`, image, conteneur, `EXPOSE` (port), variables d'env, `requirements.txt`
- **Déploiement HF Spaces** : **SDK Docker**, bloc **YAML** du README (`sdk: docker`, `app_port`), **Secrets** pour les clés, `HF_HOME=/tmp/huggingface` (cache), **cold start** (le Space s'endort après ~48 h d'inactivité)
- **Frameworks UI** (tous gratuits/open-source) : **Gradio** (démo la plus rapide, lien public 72 h via `share=True`), **Chainlit** (UI de chat pour **agents**, affiche les **étapes de raisonnement**), **Streamlit** (dashboards + chat)
- **Multimodal** : **STT** (Whisper) ; **vision** (modèle VL / Gemini)
- **Portfolio** : README soigné, **writeup** (problème → archi → choix techniques → résultats), **démo** (lien live + capture/vidéo)

---

## 📚 Ressources gratuites

> 📄 cours · 📖 doc · 📝 article · 💻 repo · 🎓 free tier | 🟢 fonda. · 🟡 inter. · 🔴 avancé · ⭐ incontournable

### Docker (J2)
- 📖 ⭐ **Docker — Get Started** 🟢 — `docs.docker.com/get-started`
- 📝 **Dockeriser une app FastAPI / Streamlit** (Dockerfile, port, `requirements.txt`) 🟡

### UI de démo (J2–J3)
- 📖 ⭐ **Gradio — Quickstart** (le plus rapide, natif HF Spaces) 🟢 — `gradio.app`
- 📖 ⭐ **Chainlit — Docs** (UI de chat pour agents : streaming, étapes, multimodal) 🟡 — `docs.chainlit.io`
- 📖 **Streamlit — Docs** (dashboards + chat) 🟢 — `docs.streamlit.io`

### Déploiement gratuit (J3–J4)
- 📖 ⭐ **Hugging Face Spaces — Docs** (SDK Docker, free **CPU Basic** : 2 vCPU / 16 Go) 🟡 — `huggingface.co/docs/hub/spaces`
- 📝 ⭐ **Deploy guide** (README YAML, `app_port`, `HF_HOME`, Secrets) 🟡 — tutos KDnuggets / HF
- 📖 **Streamlit Community Cloud** (gratuit, `share.streamlit.io`) 🟢
- 📖 **Render** (backend FastAPI, free tier) 🟢 — `render.com`

### Multimodal *(optionnel, J4)*
- 🎓 ⭐ **Groq — Whisper** (`whisper-large-v3-turbo`, STT rapide, **gratuit**) 🟡 — `console.groq.com`
- 💻 **`faster-whisper`** — STT local/gratuit 🟡 — `github.com/SYSTRAN/faster-whisper`
- 🎓 **Gemini vision** (analyse d'image, free tier) 🟢 — `aistudio.google.com`

### Portfolio & carrière (J5)
- 📝 ⭐ **Cookbooks Anthropic / OpenAI** — inspiration de projets & bonnes pratiques 🟡 — `github.com/anthropics/anthropic-cookbook`, `github.com/openai/openai-cookbook`
- 📝 **« How to host your portfolio on HF Spaces »** (KDnuggets) 🟢
- 📝 Voir aussi la **Partie 9 (Annexes)** : certifs gratuites, communautés, newsletters

---

## 💻 Repos GitHub (à lire / forker)

- 💻 ⭐ **`gradio-app/gradio`** — démos ML
- 💻 ⭐ **`Chainlit/chainlit`** — UI de chat pour agents
- 💻 **`SYSTRAN/faster-whisper`** — STT local
- 💻 *(exemples de déploiement)* repos « LLM RAG Streamlit + Docker + HF Spaces » (cherche `streamlit-llmapp` / `IntelliAgentUI`)
- 💻 *(réf. S1)* **`anthropics/anthropic-cookbook`** — patterns end-to-end

---

## 🛠️ Projet / Livrable : Capstone end-to-end **déployé**

🎯 Assemble **UN seul projet cohérent** qui combine tout ton travail des 7 semaines.

**Architecture cible :**
`UI (Gradio/Chainlit) → API FastAPI → Agent (S6) → [RAG S4–S5 comme outil + recherche web] → LLM (via LiteLLM, S7) → tracing + garde-fous + cache (S7)`

**Idées de thème** (choisis-en **un** qui te motive) :
- 🔎 *Assistant de recherche* sur un domaine que tu connais (tes docs/PDFs).
- 🧠 *Agent de connaissance personnel* (ton « second brain » interrogeable).
- 💻 *Q&A sur une codebase* (la doc d'une lib open-source).
- 📄 *Agent d'analyse de documents* (contrats, rapports, articles).

**Cahier des charges (Definition of Done) :**
1. **End-to-end** — UI utilisable → backend → **agent qui appelle ton RAG** (+ ≥1 autre outil).
2. **Instrumenté** — au moins **tracing (S7)** + **1 garde-fou** actif en production.
3. **Conteneurisé** — un **Dockerfile** qui build et tourne **en local**.
4. **Déployé** — en ligne sur **HF Spaces** (Docker), **lien public** qui fonctionne, **clés dans Secrets**.
5. **Documenté** — **README** complet (archi, lancement, démo) + un **writeup portfolio** (problème → solution → choix techniques → résultats/limites).
6. **Repo** — `ai-engineer-roadmap/week-08-capstone/` propre et lisible.

**🌟 Bonus :**
- **Multimodal** : entrée **voix** (Whisper via Groq) ou **vision** (image/PDF).
- **CI/CD** : auto-déploiement **GitHub Actions → HF Spaces** à chaque push.
- **Badge d'éval** dans le README (tes métriques RAGAS de la S5).
- **Vidéo de démo** (1-2 min) pour le portfolio.

---

## 🗓️ Plan jour par jour

> IDs : `S8-J{jour}-T{tâche}`. Durées indicatives. 🧪 = code · 🎯 = contribue au livrable.

### J1 — Cadrage & architecture *(~4 h)*
- [x] **S8-J1-T1** — Choisir le **thème** du capstone + définir le **scope minimal** (pas trop ambitieux) ⏱️ ~45 min
- [x] **S8-J1-T2** — 🧪 Dessiner l'**architecture** (UI → API → agent → outils → obs.) ⏱️ ~45 min
- [x] **S8-J1-T3** — 🧪 🎯 **Rassembler tes briques** S4–S7 dans un projet propre ⏱️ ~1 h 30
- [x] **S8-J1-T4** — 🧪 🎯 Faire tourner le **flux complet en local** (sans UI ni Docker) ⏱️ ~1 h

### J2 — Intégration UI & Dockerfile *(~4 h)*
- [x] **S8-J2-T1** — Choisir l'UI (**Chainlit** si agent/chat ; **Gradio** si démo rapide) + lire le quickstart ⏱️ ~45 min
- [x] **S8-J2-T2** — 🧪 🎯 Brancher l'**UI** sur ton backend (streaming + étapes de l'agent) ⏱️ ~1 h 45
- [x] **S8-J2-T3** — 🧪 🎯 Écrire un **Dockerfile** (port, env, `requirements.txt`) ⏱️ ~1 h 30

### J3 — Conteneurisation & déploiement *(~4 h)*
- [ ] **S8-J3-T1** — 🧪 🎯 **Build & run** l'image Docker **en local**, corriger les erreurs ⏱️ ~1 h 30
- [ ] **S8-J3-T2** — Lire le **deploy guide HF Spaces** (YAML README, `app_port`, Secrets, `HF_HOME`) ⏱️ ~30 min
- [ ] **S8-J3-T3** — 🧪 🎯 Créer le **Space (Docker)**, pousser le code, configurer les **Secrets** ⏱️ ~1 h
- [ ] **S8-J3-T4** — 🧪 🎯 **Tester le lien public**, corriger les erreurs de build/runtime ⏱️ ~1 h

### J4 — Multimodal (option) & finitions *(~4 h)*
- [ ] **S8-J4-T1** — 🧪 *(bonus)* Ajouter une entrée **voix** (Whisper/Groq) ou **vision** ⏱️ ~1 h 30
- [ ] **S8-J4-T2** — 🧪 🎯 Vérifier **tracing + garde-fou** en production (sur le Space) ⏱️ ~1 h
- [ ] **S8-J4-T3** — 🧪 Polir l'**UX** (messages d'erreur, exemples, états de chargement) ⏱️ ~1 h
- [ ] **S8-J4-T4** — 🧪 *(bonus)* **CI/CD** GitHub Actions → HF Spaces ⏱️ ~30 min

### J5 — Documentation, portfolio & suite *(~4 h)*
- [ ] **S8-J5-T1** — 🧪 🎯 Écrire le **README** final (archi, lancement, lien, capture) ⏱️ ~1 h 15
- [ ] **S8-J5-T2** — 🧪 🎯 Rédiger le **writeup portfolio** (problème → archi → choix → résultats/limites) ⏱️ ~1 h
- [ ] **S8-J5-T3** — 🧪 *(bonus)* Enregistrer une **démo vidéo** (1-2 min) ⏱️ ~45 min
- [ ] **S8-J5-T4** — Lire la section **« Et après ? »** ci-dessous + choisir tes **2 prochains pas** ⏱️ ~1 h

---

## ✅ Critères de réussite (validation finale)

- [ ] J'ai **un projet end-to-end** qui combine **RAG + agent + prod**.
- [ ] Il est **conteneurisé (Docker)** et tourne **en local**.
- [ ] Il est **déployé** et accessible via un **lien public** (HF Spaces).
- [ ] Il a une **UI utilisable** (chat avec streaming/étapes).
- [ ] Il est **instrumenté** (tracing + ≥1 garde-fou) **en production**.
- [ ] J'ai un **README** + un **writeup portfolio** + une **démo** (lien/capture).
- [ ] Je peux **pitcher le projet en 2 min** : problème, architecture, choix techniques, limites.

> 🎉 **Si toutes les cases sont cochées : tu as bouclé 8 livrables + 1 capstone déployé.** Tu n'as pas « appris l'IA », tu as **construit** un portfolio d'ingénieur IA.

---

## 🚀 Et après ? (suite après les 8 semaines)

**Approfondir (techniques) :**
- **Fine-tuning** : LoRA / QLoRA avec **Unsloth** ou **Axolotl** (gratuit, Colab) — quand le prompting/RAG ne suffit plus.
- **Serving open-source** : **vLLM** (inférence haute performance) pour héberger tes propres modèles.
- **Agents avancés** : patterns multi-agents complexes, **MCP** en profondeur, *evaluator-optimizer*.
- **Évaluation** : evals custom, red-teaming systématique (Garak/PyRIT).

**Te spécialiser :** choisis une **verticale** (santé, finance, juridique, code…) et construis 1-2 projets ciblés — c'est ce qui te démarque.

**Te rendre visible :**
- **Build in public** (partage tes projets/démos), **contribue à de l'open-source** (LangChain, LlamaIndex, un repo que tu utilises).
- **Certifs gratuites** : certificats **Hugging Face** (LLM Course, Agents Course), short courses **DeepLearning.AI**.
- **Job prep** : *system design* d'apps LLM, optimisation coûts/latence, sécurité — et ton **portfolio** comme preuve.

**Rester à jour :** newsletters, papers, communautés → voir la **Partie 9 (Annexes)** pour la liste complète.

---

## 🔜 Suite

➡️ **Partie 9 — Annexes** — la **bibliothèque complète** de ressources gratuites (cours, ebooks, chaînes YouTube, newsletters, docs), le **répertoire des repos GitHub**, des **cheat sheets**, un **glossaire**, et des **idées de projets** pour aller plus loin.

---

*Partie 8 d'un guide en 9 parties. Liens vérifiés en juin 2026 — les offres gratuites de déploiement et les modèles multimodaux évoluent, revérifie le moment venu. Bravo pour être arrivé au bout du parcours ! 🎓*
