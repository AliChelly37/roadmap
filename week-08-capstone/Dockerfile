FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . .

# Exposer le port par défaut (Render utilise souvent 10000, mais gère la variable PORT)
EXPOSE 7860

# Créer un utilisateur non-root pour des raisons de sécurité
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app
COPY --chown=user . $HOME/app

# Variables d'environnement
ENV HOST=0.0.0.0
# Gradio ne pas créer de share link dans Docker
ENV GRADIO_SHARE=False

# Lancer l'application Gradio
CMD ["python", "app.py"]
