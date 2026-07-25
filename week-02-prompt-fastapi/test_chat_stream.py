import httpx
import sys

def test_chat_stream():
    print("🚀 Envoi d'une requête de chat en streaming à /chat...")
    
    payload = {
        "message": "Raconte-moi une blague courte en une phrase.",
        "system_prompt": "Tu es un humoriste concis.",
        "model": "llama3.2"  # Assure-toi que ce modèle existe dans ton Ollama
    }
    
    # On utilise httpx.stream pour ouvrir une connexion persistante et lire le flux
    with httpx.stream("POST", "http://127.0.0.1:8000/chat/", json=payload, timeout=20.0) as response:
        print(f"Statut HTTP : {response.status_code}")
        print("Média Type :", response.headers.get("content-type"))
        print("\nRéponse en streaming : ", end="", flush=True)
        
        # On lit chaque ligne (chunk) envoyée par le serveur FastAPI
        for line in response.iter_lines():
            if line:
                # Les lignes du protocole SSE commencent par "data: "
                if line.startswith("data:"):
                    # On extrait le texte après "data: "
                    token = line[len("data: "):]
                    # On ne strip que pour les commandes système
                    if token.strip() == "[DONE]":
                        print("\n\n✅ Stream terminé !")
                        break
                    elif token.strip().startswith("[ERREUR]"):
                        print(f"\n❌ Erreur dans le flux : {token.strip()}")
                        break
                    else:
                        print(token, end="", flush=True)

if __name__ == "__main__":
    test_chat_stream()
