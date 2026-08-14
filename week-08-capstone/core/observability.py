import os
from functools import wraps
from langfuse import observe

# Nous utiliserons le décorateur @observe pour tracer les appels de l'agent.
# Les clés Langfuse (LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_HOST)
# doivent être dans l'environnement.

def setup_observability():
    """Vérifie que les clés d'observabilité sont bien présentes."""
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    
    if not public_key or not secret_key:
        print("[WARNING] Clés Langfuse manquantes. L'observabilité ne fonctionnera pas correctement.")
        return False
    print("[INFO] Observabilité Langfuse prête.")
    return True

# Exemple simple de garde-fou manuel
def guardrail_check(input_text: str) -> bool:
    """Vérifie s'il y a des injections ou des mots interdits de base."""
    forbidden_words = ["ignore previous instructions", "system prompt", "hack"]
    text_lower = input_text.lower()
    for word in forbidden_words:
        if word in text_lower:
            print(f"[GUARDRAIL] Mot interdit détecté : {word}")
            return False
    return True
