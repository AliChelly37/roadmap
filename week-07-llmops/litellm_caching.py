import os
import time
import litellm
from litellm import completion, completion_cost
from dotenv import load_dotenv
from pathlib import Path

# Setup
ROADMAP_ROOT = Path(__file__).resolve().parent.parent
dotenv_path = ROADMAP_ROOT / ".env"
load_dotenv(dotenv_path)

def measure_request(messages, attempt_name):
    print(f"\n--- {attempt_name} ---")
    start_time = time.time()
    
    response = completion(
        model="ollama/llama3.1",
        api_base="http://localhost:11434",
        messages=messages,
    )
    
    end_time = time.time()
    latency = end_time - start_time
    
    # Récupération des informations sur le cache
    # LiteLLM ajoute souvent hasattr ou dict key 'cache_hit' ou dans _hidden_params
    # Sur les versions récentes, getattr(response, '_hidden_params', {}).get('cache_hit') 
    # ou simplement si on regarde la réponse:
    # Pour un objet ModelResponse, il peut y avoir un booléen `cache_hit` s'il vient du cache
    is_cached = getattr(response, "cache_hit", False)
    if not is_cached and hasattr(response, "_hidden_params"):
         is_cached = response._hidden_params.get("cache_hit", False)
         
    try:
        cost = completion_cost(completion_response=response)
    except Exception:
        cost = 0.0 # Modèle local = 0$
        
    print(f"Reponse  : {response.choices[0].message.content.strip()}")
    print(f"Latence  : {latency:.4f} secondes")
    print(f"Cache Hit: {is_cached}")
    print(f"Cout     : {cost:.6f} USD")
    
    return latency, is_cached

def run_caching_demo():
    print("=== DÉMONSTRATION CACHING EXACT LITELLM ===")
    
    # 1. Activation du Cache Local (en mémoire RAM)
    # Toutes les requêtes identiques seront interceptées.
    litellm.cache = litellm.Cache(type="local")
    
    # Message identique pour nos 2 requêtes
    messages = [{"role": "user", "content": "Quelle est la capitale du Japon ? Reponds avec le nom uniquement."}]
    
    # Première requête : Pas de cache, appel réel au LLM (lent)
    lat1, _ = measure_request(messages, "REQUÊTE 1 (Appel initial)")
    
    # Petite pause pour bien séparer
    time.sleep(1)
    
    # Deuxième requête : Cache Hit (instantané)
    lat2, _ = measure_request(messages, "REQUÊTE 2 (Appel identique = Cache)")
    
    print("\n=== RÉSULTATS D'OPTIMISATION ===")
    if lat1 > 0:
        gain = (lat1 - lat2) / lat1 * 100
        print(f"Gain de temps (Latence) : {gain:.2f}% plus rapide ! ({lat1:.3f}s -> {lat2:.3f}s)")
    
    print("\n💡 Leviers d'optimisation identifiés :")
    print("1. Caching exact : Parfait pour les requêtes répétitives strictes (ex: tâches de CI, tests).")
    print("2. Modèles moins chers : Le routage LiteLLM permet d'utiliser 'gpt-4o-mini' au lieu de 'gpt-4o' pour des tâches simples.")

if __name__ == "__main__":
    run_caching_demo()
