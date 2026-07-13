import os
from openai import OpenAI
import instructor
from pydantic import BaseModel, Field

# Configuration du client avec Instructor pour Ollama
client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama", 
    ),
    mode=instructor.Mode.JSON,
)

# 1. Un texte trompeur où il manque des informations !
job_description = """
Nous recherchons urgemment un Ingénieur IA pour un CDD de 6 mois.
Salaire : compétitif, à débattre. 
Compétences requises : Python, et avoir entendu parler des LLMs.
"""

# 2. Le Schéma d'extraction AVEC contraintes (Field)
# On oblige certains comportements pour compliquer la tâche du LLM.
class JobPosting(BaseModel):
    title: str
    company: str = Field(description="Nom de l'entreprise. S'il n'est pas mentionné dans le texte, le LLM DOIT retourner exactement la chaîne 'Non spécifié'.")
    salary_min: int = Field(description="Le salaire minimum en euros. Si non mentionné, le LLM DOIT retourner 0.")
    required_skills: list[str]

print("⏳ Lancement de l'extraction (cela peut prendre un moment s'il doit se corriger)...")

try:
    # 3. L'extraction AVEC RETRIES
    job_info = client.chat.completions.create(
        model="llama3.1",
        response_model=JobPosting,
        max_retries=3, # 🪄 LA MAGIE EST ICI
        messages=[
            {"role": "user", "content": f"Extrais les informations de cette offre d'emploi : {job_description}"}
        ]
    )
    print("\n✅ Extraction réussie :")
    print(job_info.model_dump_json(indent=2))
except Exception as e:
    print("\n❌ L'extraction a échoué même après 3 tentatives :")
    print(e)
