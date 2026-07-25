import sys
import os
import json

# Ajoute le dossier racine du projet au chemin Python pour importer prompt_template.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi import APIRouter, HTTPException
from openai import AsyncOpenAI

from app.schemas import ExtractRequest, PersonExtract
from prompt_template import PromptTemplate

# --- Router ---
router = APIRouter(prefix="/extract", tags=["extract"])

# --- Client LLM (Ollama local) ---
client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# --- Template de prompt dédié à l'extraction ---
# Ce template est conçu pour forcer le LLM à ne retourner QUE du JSON.
# On utilise des exemples few-shot pour lui montrer exactement le format attendu.
# Plus les exemples sont clairs, moins le LLM a de chance de "dévier" du format.
extract_template = PromptTemplate(
    system_prompt=(
        "Tu es un extracteur d'information expert. "
        "Analyse le texte fourni et extrais les informations suivantes : nom, age, profession, ville. "
        "Tu dois répondre UNIQUEMENT avec un objet JSON valide, sans texte avant ni après. "
        "Si une information est absente du texte, mets null pour ce champ. "
        "Format de réponse attendu : {\"nom\": \"...\", \"age\": ..., \"profession\": \"...\", \"ville\": \"...\"}"
    ),
    examples=[
        # Exemple few-shot 1 : toutes les infos présentes
        {
            "user": "<user_input>\nJe suis Sarah Dupont, ingénieure en IA à Paris, j'ai 32 ans.\n</user_input>",
            "assistant": '{"nom": "Sarah Dupont", "age": 32, "profession": "ingénieure en IA", "ville": "Paris"}'
        },
        # Exemple few-shot 2 : infos manquantes → null
        {
            "user": "<user_input>\nMon nom est Karim et je travaille comme médecin.\n</user_input>",
            "assistant": '{"nom": "Karim", "age": null, "profession": "médecin", "ville": null}'
        }
    ]
)


@router.post("/", response_model=PersonExtract)
async def extract(payload: ExtractRequest):
    """
    Extrait des informations structurées (nom, age, profession, ville)
    depuis un texte brouillon en langage naturel.

    Exemple de body JSON à envoyer :
    {
        "text": "Je m'appelle Mohamed, j'ai 28 ans et je travaille comme dev Python à Lyon."
    }

    Retourne un JSON structuré conforme au modèle PersonExtract.
    """

    # Étape 1 : Formater les messages avec le template d'extraction.
    # Le texte brouillon de l'utilisateur est injecté comme user_input.
    messages = extract_template.format_messages(user_input=payload.text)

    # Étape 2 : Appeler le LLM en mode JSON.
    # response_format={"type": "json_object"} force Ollama à retourner du JSON valide.
    # Cela évite que le modèle réponde "Voici le JSON : {...}" (ce qu'on ne veut pas).
    try:
        completion = await client.chat.completions.create(
            model=payload.model,
            messages=messages,
            temperature=0.0,                              # 0 = déterministe : pas de créativité pour l'extraction
            response_format={"type": "json_object"},      # Force le LLM à ne retourner que du JSON
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Le LLM est injoignable. Vérifie qu'Ollama tourne. Erreur : {str(e)}"
        )

    # Étape 3 : Récupérer le texte brut de la réponse du LLM.
    raw_text = completion.choices[0].message.content

    # Étape 4 : Convertir le texte JSON en dictionnaire Python, puis en objet Pydantic.
    # Pydantic va valider les types (ex: age doit être un int ou None, pas une string).
    try:
        extracted_data = json.loads(raw_text)  # str → dict Python
        return PersonExtract(**extracted_data)  # dict → objet Pydantic (avec validation)
    except (json.JSONDecodeError, Exception) as e:
        # Si le LLM n'a pas respecté le format JSON malgré nos instructions,
        # on renvoie une erreur 422 avec le texte brut pour le débogage.
        raise HTTPException(
            status_code=422,
            detail=f"Le LLM n'a pas retourné un JSON valide. Réponse brute : {raw_text}"
        )
