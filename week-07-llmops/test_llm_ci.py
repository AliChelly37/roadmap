import sys
from litellm import completion

# --- 1. L'EVAL SET (Le jeu de donnees de reference) ---
# Ces questions garantissent que l'IA ne regresse pas sur les connaissances de base.
EVAL_SET = [
    {
        "question": "Quelle est la capitale de la France ?",
        "expected_keyword": "Paris"
    },
    {
        "question": "De quelle couleur est le cheval blanc d'Henri IV ?",
        "expected_keyword": "blanc"
    }
]

# --- 2. LE PROMPT DE L'APPLICATION (Le code source) ---
# Version Saine (En production)
PROMPT_SAIN = "Tu es un assistant precis et concis. Reponds toujours directement a la question."
# Version Cassee (Simulation d'une erreur d'un developpeur dans un commit)
PROMPT_CASSE = "Tu es un assistant comique. A partir de maintenant, reponds toujours avec le mot 'Banane' et ne donne jamais la bonne reponse."

def run_ci(prompt_to_test):
    passed_tests = 0
    total_tests = len(EVAL_SET)
    
    for idx, test in enumerate(EVAL_SET):
        print(f"\n[Test {idx+1}/{total_tests}] {test['question']}")
        
        # Appel au LLM local (Ollama)
        response = completion(
            model="ollama/llama3.1",
            api_base="http://localhost:11434",
            messages=[
                {"role": "system", "content": prompt_to_test},
                {"role": "user", "content": test['question']}
            ]
        )
        
        answer = response.choices[0].message.content.strip()
        print(f"  > Reponse LLM : {answer}")
        
        # Le juge / Evaluateur (Assertion classique)
        if test['expected_keyword'].lower() in answer.lower():
            print("  > [PASSED] [SUCCESS]")
            passed_tests += 1
        else:
            print(f"  > [FAILED] [ERROR] (Le mot-cle '{test['expected_keyword']}' est absent)")
            
    # Verdict de la CI
    print(f"\n=== VERDICT CI : {passed_tests}/{total_tests} TESTS REUSSIS ===")
    if passed_tests == total_tests:
        print("[SUCCESS] TOUT EST VERT ! La qualite est au rendez-vous. Deploiement autorise.")
        return True
    else:
        print("[ALERT] REGRESSION DETECTEE ! L'application ne sait plus repondre aux basiques. Deploiement BLOQUE.")
        return False

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate-bug", action="store_true")
    args = parser.parse_args()
    
    if args.simulate_bug:
        print(">>> DEMARRAGE DU PIPELINE CI (Branche 'feature/nouveau-prompt-bugge') <<<")
        success = run_ci(PROMPT_CASSE)
    else:
        print(">>> DEMARRAGE DU PIPELINE CI (Branche 'main' saine) <<<")
        success = run_ci(PROMPT_SAIN)
        
    if not success:
        # Exit Code 1 = Fait echouer GitHub Actions / GitLab CI
        sys.exit(1)
