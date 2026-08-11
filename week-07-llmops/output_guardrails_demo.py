import json
from pydantic import BaseModel, Field, ValidationError

# --- 1. Definition du schema attendu (Pydantic) ---
# On s'attend a ce que l'IA renvoie TOUJOURS ce format strict
class AIResponseSchema(BaseModel):
    summary: str = Field(description="Resume de la reponse")
    confidence: float = Field(ge=0.0, le=1.0, description="Score de confiance entre 0 et 1")

# --- 2. Configuration du scanner de modération LLM Guard ---
try:
    from llm_guard.output_scanners import NoRefusal
    # NoRefusal verifie si l'IA a refuse de repondre (ex: "As an AI, I cannot...")
    refusal_scanner = NoRefusal(threshold=0.5)
except ImportError:
    print("Erreur: llm-guard non installe.")
    exit(1)

def run_output_guardrails():
    print("=== DEMONSTRATION GARDE-FOUS (OUTPUT) ===\n")
    
    # --- Cas 1 : Le LLM refuse de repondre (Moderation) ---
    print("--- CAS 1 : REPONSE REFUSEE PAR L'IA ---")
    simulated_refusal = "Je suis desole, mais en tant qu'intelligence artificielle, je ne peux pas repondre a cette question."
    print(f"[LLM OUTPUT] : '{simulated_refusal}'")
    
    # On scanne la reponse (prompt vide simulé car on ne teste que l'output)
    sanitized_output, is_valid, risk_score = refusal_scanner.scan(prompt="", output=simulated_refusal)
    if not is_valid:
        print("[ALERTE MODERATION] : L'IA a refuse de repondre. On peut declencher une logique de 'Retry' automatique ou un Fallback.")
    else:
        print("[VALIDE] : L'IA a repondu normalement.")

    print("\n-------------------------------------------------\n")

    # --- Cas 2 : Le LLM hallucine le format JSON (Validation de Schema) ---
    print("--- CAS 2 : REPONSE HORS FORMAT (Hallucination structurelle) ---")
    simulated_bad_format = '{"summary": "Voici la reponse", "score_de_confiance_invente": "tres fort"}'
    print(f"[LLM OUTPUT] : '{simulated_bad_format}'")
    
    try:
        # On tente de parser le JSON brut en dictionnaire
        data = json.loads(simulated_bad_format)
        # On valide avec Pydantic
        validated_data = AIResponseSchema(**data)
        print("[VALIDE] Schema respecte :", validated_data)
    except json.JSONDecodeError:
        print("[ALERTE SCHEMA] : La reponse n'est pas un JSON valide.")
    except ValidationError as e:
        print("[ALERTE SCHEMA] : La reponse ne respecte pas le schema Pydantic !")
        # Pydantic nous dit precisement ce qui manque
        for error in e.errors():
            print(f"  -> Erreur sur le champ '{error['loc'][0]}': {error['msg']}")
        print("  -> Action : On doit demander au LLM de corriger son format (Retry avec erreur en prompt).")


if __name__ == "__main__":
    run_output_guardrails()
