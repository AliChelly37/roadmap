import os
from openai import OpenAI
import instructor
from pydantic import BaseModel

# 1. Configuration du client avec Instructor pour Ollama
# Ollama fournit une API locale compatible OpenAI sur le port 11434
client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama", # Requis par le SDK OpenAI mais ignoré par Ollama
    ),
    mode=instructor.Mode.JSON,
)

# 3. Le texte brut de l'annonce d'emploi (non structuré)
job_description = """
Nous recherchons un Ingénieur IA passionné pour rejoindre notre équipe chez TechVision.
Le candidat idéal a une solide expérience en Python et avec des frameworks comme PyTorch ou TensorFlow.
Une maîtrise des LLMs (OpenAI, Gemini) et du prompt engineering est exigée.
Le salaire proposé est compris entre 60000 et 80000 euros selon profil. Le poste est basé à Paris en hybride.
"""

# 4. Le Schéma d'extraction (Le Moule)
class JobPosting(BaseModel):
    title: str
    company: str
    salary_min: int | None = None
    salary_max: int | None = None
    required_skills: list[str]

# ==========================================
# 🎯 À TOI DE JOUER !
# ==========================================
# TODO : Écris la requête avec `client.chat.completions.create(...)` pour extraire les données
# de la variable `job_description` en forçant le LLM à respecter le modèle `JobPosting`.
# 
# Paramètres importants :
# - model="llama3.1"
# - response_model=JobPosting
# - messages=[...]
#
# Pense à donner une instruction claire au LLM, par exemple :
# "Extrais les informations de cette offre d'emploi : {job_description}"

job_info = client.chat.completions.create(
    model="llama3.1",
    response_model=JobPosting,
    messages=[
        {"role": "user", "content": f"Extrais les informations de cette offre d'emploi : {job_description}"}
    ]
)

# Une fois extrait, on affiche le résultat final en beau JSON :
print(job_info.model_dump_json(indent=2))
