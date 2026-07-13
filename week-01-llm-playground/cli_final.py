# -*- coding: utf-8 -*-
"""
CLI Final - Semaine 1 AI Engineering
Combine : multi-provider, extraction structuree (Instructor), tool calling.

Usage:
  python cli_final.py chat   "Ta question ici"
  python cli_final.py extract "Texte de l'offre d'emploi ici"
  python cli_final.py weather "Quelle est la meteo a Paris ?"
"""

import sys
import json
import argparse
from openai import OpenAI
import instructor
from pydantic import BaseModel, Field

# ============================================================
# CONFIGURATION UNIQUE DU CLIENT (Ollama local)
# ============================================================
BASE_URL = "http://localhost:11434/v1"
MODEL = "llama3.1"

raw_client = OpenAI(base_url=BASE_URL, api_key="ollama")
instructor_client = instructor.from_openai(raw_client, mode=instructor.Mode.JSON)


# ============================================================
# MODE 1 : CHAT LIBRE
# Envoie un message et recoit une reponse texte classique.
# ============================================================
def mode_chat(question: str):
    print(f"\n[CHAT] Question : {question}\n")
    response = raw_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Tu es un assistant concis et utile. Reponds en francais."},
            {"role": "user", "content": question}
        ]
    )
    print("[REPONSE] " + response.choices[0].message.content)


# ============================================================
# MODE 2 : EXTRACTION STRUCTUREE (Instructor + Pydantic)
# Extrait les informations cles d'un texte d'offre d'emploi.
# ============================================================
class JobPosting(BaseModel):
    title: str = Field(description="Titre du poste.")
    company: str = Field(description="Nom de l'entreprise. Si absent, retourner 'Non specifie'.")
    salary_min: int = Field(description="Salaire minimum en euros. Si absent, retourner 0.")
    salary_max: int = Field(description="Salaire maximum en euros. Si absent, retourner 0.")
    required_skills: list[str] = Field(description="Liste des competences requises.")

def mode_extract(texte: str):
    print(f"\n[EXTRACT] Texte source :\n  {texte[:100]}...\n")
    try:
        job = instructor_client.chat.completions.create(
            model=MODEL,
            response_model=JobPosting,
            max_retries=3,
            messages=[{"role": "user", "content": f"Extrais les informations de cette offre d'emploi : {texte}"}]
        )
        print("[REPONSE JSON]")
        print(job.model_dump_json(indent=2))
    except Exception as e:
        print(f"[ERREUR] L'extraction a echoue : {e}")


# ============================================================
# MODE 3 : TOOL CALLING (Meteo)
# Le LLM decide d'appeler une vraie fonction Python.
# ============================================================
def get_weather(location: str) -> str:
    """Simule un appel API meteo."""
    print(f"  --> [OUTIL] get_weather('{location}') execute !")
    db = {"paris": "Nuageux, 15C", "tunis": "Ensoleille, 32C", "london": "Pluvieux, 10C"}
    for city, weather in db.items():
        if city in location.lower():
            return weather
    return "Meteo inconnue pour cette ville."

WEATHER_TOOL = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Donne la meteo actuelle pour une ville donnee.",
        "parameters": {
            "type": "object",
            "properties": {"location": {"type": "string", "description": "Nom de la ville."}},
            "required": ["location"]
        }
    }
}

def mode_weather(question: str):
    print(f"\n[WEATHER] Question : {question}\n")
    messages = [
        {"role": "system", "content": "Tu es un assistant meteo. Tu DOIS utiliser l'outil 'get_weather' pour repondre aux questions sur la meteo."},
        {"role": "user", "content": question}
    ]
    response = raw_client.chat.completions.create(model=MODEL, messages=messages, tools=[WEATHER_TOOL])
    msg = response.choices[0].message

    if msg.tool_calls:
        for call in msg.tool_calls:
            if call.function.name == "get_weather":
                args = json.loads(call.function.arguments)
                result = get_weather(args["location"])
                messages.append(msg)
                messages.append({"role": "tool", "tool_call_id": call.id, "name": "get_weather", "content": result})

        final = raw_client.chat.completions.create(model=MODEL, messages=messages)
        print("[REPONSE] " + final.choices[0].message.content)
    else:
        print("[INFO] Le LLM n'a pas utilise l'outil.")
        print("[REPONSE] " + msg.content)


# ============================================================
# POINT D'ENTREE CLI
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="CLI AI Engineering - Semaine 1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples :
  python cli_final.py chat    "C'est quoi un LLM ?"
  python cli_final.py extract "Poste : Data Scientist chez ACME, salaire 50k-70k, Python requis."
  python cli_final.py weather "Il fait quel temps a Paris ?"
        """
    )
    parser.add_argument("mode", choices=["chat", "extract", "weather"], help="Mode de fonctionnement.")
    parser.add_argument("texte", help="La question ou le texte a traiter.")

    args = parser.parse_args()

    if args.mode == "chat":
        mode_chat(args.texte)
    elif args.mode == "extract":
        mode_extract(args.texte)
    elif args.mode == "weather":
        mode_weather(args.texte)

if __name__ == "__main__":
    main()
