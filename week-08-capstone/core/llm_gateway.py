import os
import litellm
from litellm import completion
from litellm.caching import Cache

# Active le cache LiteLLM (cache local simple en mémoire)
litellm.cache = Cache(type="local")

def get_llm_response(messages, model="openai/llama3.1", use_cache=True):
    """
    Passe par la Gateway LiteLLM.
    Gère le fallback, les retries, et le cache.
    """
    fallbacks = [
        {"model": "openai/llama3.1", "api_base": "http://localhost:11434/v1", "api_key": "ollama"}
    ]
    
    # Configuration par défaut pour Ollama
    if "llama" in model.lower() and "openai/" in model:
        api_base = "http://localhost:11434/v1"
        api_key = "ollama"
    else:
        api_base = None
        api_key = None

    try:
        response = completion(
            model=model,
            messages=messages,
            api_base=api_base,
            api_key=api_key,
            fallbacks=fallbacks,
            num_retries=2,
            caching=use_cache
        )
        return response
    except Exception as e:
        print(f"[Gateway Error] {e}")
        return None
