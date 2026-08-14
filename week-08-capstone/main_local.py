import os
from dotenv import load_dotenv
from pathlib import Path

# Load env variables from root
ROADMAP_ROOT = Path(__file__).resolve().parent.parent
dotenv_path = ROADMAP_ROOT / ".env"
load_dotenv(dotenv_path)

from core.rag import index_roadmap_files
from core.observability import setup_observability, guardrail_check
from core.agent import run_agent

def main():
    print("=== DÉMARRAGE DU CAPSTONE EN LOCAL ===")
    
    # 1. Check env & observability
    setup_observability()
    
    # 2. Index RAG (si pas déjà fait)
    index_roadmap_files()
    
    print("\n[INFO] Assistant prêt ! Posez votre question (ou tapez 'quit' pour quitter).")
    
    while True:
        user_input = input("\nVous: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            break
            
        # 3. Guardrails (Vérification simple)
        if not guardrail_check(user_input):
            print("Assistant: Désolé, je ne peux pas traiter cette requête pour des raisons de sécurité.")
            continue
            
        # 4. Agent Execution (RAG + LLM)
        try:
            response = run_agent(user_input)
            print(f"\nAssistant:\n{response}")
        except Exception as e:
            print(f"\n[ERREUR] Une erreur s'est produite : {e}")

if __name__ == "__main__":
    main()
