from fastapi.testclient import TestClient
from main import app

# Utilisation du TestClient de FastAPI pour simuler une requête sans avoir à lancer le serveur
client = TestClient(app)

def run_test():
    print("🚀 Envoi d'une requête de test à /extract...")
    
    # Le texte non structuré qu'on veut analyser
    texte_brouillon = "Je m'appelle Thomas, je suis un développeur web de 29 ans et j'habite à Bordeaux."
    print(f"Texte d'entrée : '{texte_brouillon}'\n")
    
    response = client.post(
        "/extract/",
        json={
            "text": texte_brouillon,
            "model": "llama3.2"  # Assure-toi que ce modèle existe dans ton Ollama
        }
    )
    
    print(f"Statut HTTP : {response.status_code}")
    if response.status_code == 200:
        print("✅ Réponse structurée (Pydantic validé) :")
        print(response.json())
    else:
        print("❌ Erreur :")
        print(response.text)

if __name__ == "__main__":
    run_test()
