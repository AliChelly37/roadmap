import os
import litellm
from litellm import completion, completion_cost
from dotenv import load_dotenv
from pathlib import Path

# Setup
ROADMAP_ROOT = Path(__file__).resolve().parent.parent
dotenv_path = ROADMAP_ROOT / ".env"
load_dotenv(dotenv_path)

def run_gateway():
    print("=== DÉMONSTRATION GATEWAY LITELLM ===")
    
    # 1. Définition des Fallbacks
    # Si le modèle principal échoue, LiteLLM basculera sur ceux de cette liste
    fallbacks = [{"model": "openai/llama3.1", "api_base": "http://localhost:11434/v1", "api_key": "ollama"}]
    
    messages = [{"role": "user", "content": "Quelle est la capitale de l'Australie ? Réponds en un seul mot."}]
    
    print("\n[INFO] Tentative de requête vers un modèle défaillant ('openai/fake-failing-model')...")
    print("[INFO] Fallback configuré vers : 'ollama/llama3.1'")
    
    try:
        # 2. Appel unifié et routage avec LiteLLM
        response = completion(
            model="openai/fake-failing-model",
            messages=messages,
            fallbacks=fallbacks,
            # 3. Retries : s'il s'agit d'une erreur transitoire (ex: Timeout), on réessaie
            num_retries=2, 
        )
        
        print("\n--- SUCCES ---")
        # On vérifie quel modèle a réellement répondu
        print(f"Modèle ayant finalement répondu : {response.model}")
        print(f"Réponse : {response.choices[0].message.content}")
        
        # 4. Suivi des coûts
        cost = completion_cost(completion_response=response)
        print(f"\n[COUT] Estimation du prix de cette requête : {cost:.6f} USD")
        
    except litellm.exceptions.RateLimitError as e:
        # Exemple de gestion de rate limiting si on veut lever une alerte
        print(f"\n[RATE LIMIT] Vous avez dépassé votre quota : {e}")
    except litellm.exceptions.NotFoundError as e:
        print(f"\n[ERREUR] Modèle introuvable (même après fallback) : {e}")
    except Exception as e:
        print(f"\n[ERREUR INATTENDUE] : {e}")

if __name__ == "__main__":
    # Activation du mode verbeux de LiteLLM pour voir ce qui se passe sous le capot (les erreurs interceptées)
    litellm.set_verbose = True
    run_gateway()
