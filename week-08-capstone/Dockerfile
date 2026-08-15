FROM python:3.11-slim

# Utilisateur non-root (exigé par HF Spaces, qui lance le conteneur en UID 1000).
# Le répertoire de travail est créé ET donné à `user` ici : un `WORKDIR` exécuté
# pendant qu'on est encore root crée le dossier en root:root, et chromadb ne peut
# alors pas y écrire sa base une fois passé en `user` (Permission denied, os error 13).
RUN useradd -m -u 1000 user \
    && mkdir -p /home/user/app \
    && chown -R user:user /home/user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/home/user/.cache/huggingface

USER user
WORKDIR /home/user/app

# torch en version CPU AVANT le reste. sentence-transformers tire `torch`, et la
# roue PyPI par défaut embarque toute la pile CUDA (nvidia-cudnn, cublas, triton…) :
# ~6 Go de bibliothèques GPU inutiles sur un Space CPU. En installant d'abord la
# roue CPU, les dépendances suivantes la trouvent déjà satisfaite.
RUN pip install --no-cache-dir --user \
    --index-url https://download.pytorch.org/whl/cpu torch

# Puis le reste. Cette couche est mise en cache tant que requirements.txt ne bouge
# pas, donc un changement de code ne réinstalle rien.
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Puis le code et le corpus
COPY --chown=user . .

# Indexation au BUILD, pas au démarrage. Deux raisons :
#  - le conteneur démarre instantanément au lieu d'encoder 297 chunks à froid ;
#  - le modèle d'embeddings est téléchargé ici, donc figé dans l'image (pas de
#    dépendance réseau au runtime, pas de pic mémoire au premier message).
# C'est ce pic au démarrage qui provoquait les OOM sur le free tier Render.
RUN python -c "from core.rag import index_roadmap_files; index_roadmap_files()"

# Vérifie que le corpus est réellement interrogeable : mieux vaut casser le build
# qu'expédier un assistant qui répond sans connaissances.
RUN python test_retrieval.py

EXPOSE 7860
ENV PORT=7860

# uvicorn en direct : app.py n'est plus qu'un module FastAPI depuis l'abandon
# de Gradio. Un seul worker — l'index et le modèle d'embeddings sont chargés
# en mémoire une fois, les dupliquer coûterait ~500 Mo par worker.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1"]
