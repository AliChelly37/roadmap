import sys
import os

# On ajoute le dossier parent (week-02-prompt-fastapi/) au chemin de recherche Python
# pour pouvoir importer prompt_template.py qui est à la racine du projet,
# et non dans le dossier app/.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI  # On utilise le client asynchrone pour le streaming

from app.schemas import ChatRequest
from prompt_template import PromptTemplate  # Notre classe de templating (Semaine 2 Jour 2)

# --- Création du Router ---
# prefix="/chat" : toutes les routes de ce fichier commenceront par /chat
# tags=["chat"] : groupe ces routes dans la doc Swagger sous l'onglet "chat"
router = APIRouter(prefix="/chat", tags=["chat"])

# --- Initialisation du client LLM ---
# On utilise le SDK OpenAI en lui donnant l'URL d'Ollama qui tourne en local.
# api_key="ollama" : Ollama n'a pas besoin d'une vraie clé, mais le SDK l'exige.
# Pour passer sur Groq ou Gemini, il suffit de changer base_url et api_key ici.
client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# --- Template de prompt par défaut ---
# On crée un template réutilisable avec quelques exemples few-shot pour montrer
# au LLM comment on attend qu'il se comporte.
default_template = PromptTemplate(
    system_prompt="$system_prompt",  # Variable remplacée dynamiquement à chaque appel
    examples=[
        # Exemple few-shot : montre au LLM qu'on veut des réponses concises
        {"user": "Qu'est-ce que Python ?", "assistant": "Python est un langage de programmation interprété, connu pour sa lisibilité et sa polyvalence."}
    ]
)


@router.post("/")
async def chat(payload: ChatRequest):
    """
    Route principale de chat avec le LLM en streaming.
    Reçoit un message utilisateur, l'envoie au LLM via Ollama, et retourne la réponse
    token par token (Server-Sent Events).
    """

    messages = default_template.format_messages(
        system_prompt=payload.system_prompt,
        user_input=payload.message
    )

    async def stream_generator():
        try:
            # On appelle le LLM avec stream=True
            stream = await client.chat.completions.create(
                model=payload.model,
                messages=messages,
                temperature=0.7,
                stream=True  # Active le streaming
            )
            
            # On itère sur chaque morceau de texte (chunk) reçu
            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    # Format SSE (Server-Sent Events)
                    yield f"data: {content}\n\n"
                    
            # Optionnel : Marquer la fin du stream pour le client
            yield "data: [DONE]\n\n"
            
        except Exception as e:
            yield f"data: [ERREUR] Le LLM est injoignable ou a echoue : {str(e)}\n\n"

    # On retourne une StreamingResponse avec le bon type de média pour du SSE
    return StreamingResponse(stream_generator(), media_type="text/event-stream")
