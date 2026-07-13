import json
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# ==========================================
# 1. NOTRE VRAIE FONCTION PYTHON (L'Outil)
# ==========================================
def get_weather(location: str):
    print(f"[OUTIL PYTHON EXECUTE] Je verifie la meteo pour : {location}...")
    if "paris" in location.lower():
        return "Nuageux, 15°C"
    elif "tunis" in location.lower():
        return "Ensoleillé, 32°C"
    else:
        return "Météo inconnue, 20°C"

# ==========================================
# 2. ON DÉCRIT NOTRE OUTIL AU LLM
# ==========================================
# On utilise le format JSON Schema standard (OpenAI)
tools_list = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Donne la météo actuelle pour une ville donnée.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Le nom de la ville, ex: Paris, Tunis"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# ==========================================
# 3. LE CYCLE DE VIE DU "TOOL CALLING"
# ==========================================
messages = [
    {
        "role": "system",
        "content": "Tu es un assistant météo. Quand l'utilisateur demande la météo d'une ville, tu DOIS ABSOLUMENT utiliser l'outil 'get_weather'. N'invente jamais de réponse sur la météo."
    },
    {"role": "user", "content": "Coucou ! Fait-il beau à Tunis en ce moment ?"}
]

print("[ETAPE 1] Le LLM lit la question et voit qu'il a acces a des outils...")
response = client.chat.completions.create(
    model="llama3.1",
    messages=messages,
    tools=tools_list,
)

message_retourne = response.choices[0].message

# DEBUG : Voir ce que le LLM a vraiment renvoyé
print(f"\n[DEBUG] tool_calls = {message_retourne.tool_calls}")

# Est-ce que le LLM a décidé qu'il avait besoin d'un outil ?
if message_retourne.tool_calls:
    for tool_call in message_retourne.tool_calls:
        # Il veut utiliser get_weather !
        if tool_call.function.name == "get_weather":
            # Le LLM a extrait les arguments de la phrase (ex: {"location": "Tunis"})
            arguments = json.loads(tool_call.function.arguments)
            ville = arguments.get("location")
            
            # C'EST ICI LA MAGIE : C'est NOUS qui exécutons le code, pas le LLM !
            resultat_meteo = get_weather(ville)
            
            # On met à jour l'historique pour lui donner le résultat
            messages.append(message_retourne) # Sa demande d'outil
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": "get_weather",
                "content": str(resultat_meteo) # On lui donne le résultat texte
            })
            
            print("\n[ETAPE 2] On renvoie le resultat au LLM. Il formule sa reponse finale...")
            final_response = client.chat.completions.create(
                model="llama3.1",
                messages=messages
            )
            print("\n[OK] REPONSE FINALE DU LLM :")
            print(final_response.choices[0].message.content)
else:
    # Le LLM n'a pas utilise d'outil
    print("\n[OK] REPONSE FINALE DU LLM :")
    print(message_retourne.content)
