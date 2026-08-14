import os
import re
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


def get_langfuse_handler():
    """Retourne un callback handler LangChain, ou None si Langfuse n'est pas configuré.

    Le décorateur @observe ne trace que `run_agent`, or l'UI Gradio appelle
    `graph.stream()` directement : sans ce handler passé dans le config LangGraph,
    aucune trace ne remonte en production. C'est le chemin canonique pour tracer
    LangGraph (chaque nœud et chaque appel LLM devient un span).
    """
    if not setup_observability():
        return None
    try:
        from langfuse.langchain import CallbackHandler
        return CallbackHandler()
    except Exception as exc:  # pas de tracing => l'app doit continuer de tourner
        print(f"[WARNING] Handler Langfuse indisponible : {exc}")
        return None

# Garde-fou d'entrée : détection d'injection de prompt (OWASP LLM01).
#
# On cible des TOURNURES d'injection, pas des mots-clés isolés. L'ancienne liste
# bloquait « system prompt » et « hack », ce qui refusait des questions parfaitement
# légitimes — le prompt engineering est le sujet de la Semaine 2, un utilisateur a
# toute raison de demander « explique-moi le system prompt de la semaine 2 ».
# Un garde-fou qui refuse le cœur du corpus est un bug, pas une sécurité.
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions?",
    r"disregard\s+(all\s+)?(previous|prior|above)",
    r"oublie[sz]?\s+(tes|les|toutes\s+les)\s+instructions?",
    r"ignore[sz]?\s+(tes|les)\s+instructions?",
    r"(reveal|show|print|répète|repete|affiche)\s+(me\s+)?(your|ton|le)\s+(system\s+)?prompt",
    r"you\s+are\s+now\s+(a|an)\b",
    r"tu\s+es\s+maintenant\s+un",
    r"\bDAN\b\s+mode",
    r"</?(system|instruction)>",
]


def guardrail_check(input_text: str) -> bool:
    """False si l'entrée ressemble à une tentative d'injection de prompt."""
    text = input_text.lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            print(f"[GUARDRAIL] Motif d'injection détecté : {pattern}")
            return False
    return True
