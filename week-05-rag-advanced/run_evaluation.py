import os
import sys
import json
import types
import time
import asyncio
from pathlib import Path
from unittest.mock import MagicMock
from dotenv import load_dotenv

# Enforce UTF-8 encoding on standard output for Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 1. Configuration & Environnement
ROADMAP_ROOT = Path(__file__).resolve().parent.parent
dotenv_path = ROADMAP_ROOT / ".env"
load_dotenv(dotenv_path)

# Patch Ragas Vertex AI import bug
dummy_module = types.ModuleType("langchain_community.chat_models.vertexai")
dummy_module.ChatVertexAI = MagicMock
sys.modules["langchain_community.chat_models.vertexai"] = dummy_module

# 2. Imports Ragas & Langchain
from ragas import evaluate
from datasets import Dataset
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from langchain_community.embeddings import HuggingFaceEmbeddings
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import BaseRagasLLM
from langchain_core.prompt_values import PromptValue
from langchain_core.outputs import LLMResult, Generation
from google import genai
from google.genai import types as genai_types
from ragas.run_config import RunConfig

# 3. Import du RAG de la semaine 4
WEEK4_PATH = ROADMAP_ROOT / "week-04-rag-chat-docs"
sys.path.append(str(WEEK4_PATH))

import query_rag
# Surcharge de la base de données vers le dossier physique de la S4
query_rag.DB_PATH = str(WEEK4_PATH / "chroma_db")

# 4. Custom LLM Wrapper pour Ragas n'est plus nécessaire (utilisation d'Ollama en local)

# 5. Exécution du RAG sur le dataset
def run_rag_on_dataset(eval_set_path, results_output_path):
    print(f"Chargement du jeu de test : {eval_set_path}")
    with open(eval_set_path, "r", encoding="utf-8") as f:
        eval_set = json.load(f)

    # Initialisation du client de production pour S4
    ai_client = genai.Client()
    results = []

    print("\n--- Étape 1/2 : Génération des réponses RAG (Baseline S4) ---")
    for i, item in enumerate(eval_set):
        question = item["question"]
        print(f"\n[{i+1}/{len(eval_set)}] Question : {question}")
        
        # Ingestion S4 : Retrieval
        contexts = query_rag.retrieve_chunks(question, k=3)
        context_texts = [c["text"] for c in contexts] if contexts else []
        
        # Ingestion S4 : Garde de score
        SCORE_THRESHOLD = 0.22
        best_distance = contexts[0]['distance'] if contexts else 1.0
        
        if best_distance > SCORE_THRESHOLD:
            print(f"  [Garde de Score activée] Distance : {best_distance:.4f} > {SCORE_THRESHOLD}")
            answer = "Je ne sais pas."
        else:
            prompt = query_rag.build_prompt(question, contexts)
            try:
                response = ai_client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=prompt,
                    config=genai_types.GenerateContentConfig(
                        temperature=0.0,
                        max_output_tokens=1000
                    )
                )
                answer = response.text or ""
            except Exception as e:
                print(f"  Erreur génération RAG : {e}")
                answer = "Erreur de génération."
        
        print(f"  Réponse : {answer}")
        
        results.append({
            "question": question,
            "contexts": context_texts,
            "answer": answer,
            "ground_truth": item["ground_truth"]
        })

    with open(results_output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nRésultats intermédiaires sauvegardés dans {results_output_path}")
    return results

def main():
    eval_set_path = Path(__file__).parent / "eval_set.json"
    results_path = Path(__file__).parent / "baseline_results_temp.json"
    
    if not results_path.exists():
        rag_data = run_rag_on_dataset(eval_set_path, results_path)
    else:
        print(f"Chargement des réponses RAG existantes depuis {results_path}...")
        with open(results_path, "r", encoding="utf-8") as f:
            rag_data = json.load(f)

    # 6. Préparation des données pour RAGAS
    questions = [item["question"] for item in rag_data]
    answers = [item["answer"] for item in rag_data]
    contexts_list = [item["contexts"] for item in rag_data]
    ground_truths = [item["ground_truth"] for item in rag_data]
    
    hf_dataset = Dataset.from_dict({
        "question": questions,
        "contexts": contexts_list,
        "answer": answers,
        "ground_truth": ground_truths
    })
    
    # 7. Initialisation des composants d'évaluation
    print("\n--- Étape 2/2 : Évaluation RAGAS ---")
    from langchain_openai import ChatOpenAI
    from ragas.llms import LangchainLLMWrapper
    
    print("Initialisation d'Ollama avec le modèle local llama3.1...")
    ollama_llm = ChatOpenAI(
        model="llama3.1",
        api_key="ollama",
        base_url="http://localhost:11434/v1",
        temperature=0
    )
    evaluator_llm = LangchainLLMWrapper(ollama_llm)
    
    # Configuration de l'evaluator LLM sur les métriques
    faithfulness.llm = evaluator_llm
    answer_relevancy.llm = evaluator_llm
    context_precision.llm = evaluator_llm
    context_recall.llm = evaluator_llm
    
    # Embeddings locaux pour l'évaluation de la similarité cosinus
    print("Initialisation des embeddings locaux (multilingual-e5-base)...")
    embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base")
    ragas_embeddings = LangchainEmbeddingsWrapper(embeddings)
    
    # Run Config (utilisation de 2 workers parallèles car Ollama s'exécute localement)
    run_config = RunConfig(
        max_workers=2,
        timeout=180
    )
    
    print("Lancement de l'évaluation RAGAS...")
    results = evaluate(
        dataset=hf_dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        llm=evaluator_llm,
        embeddings=ragas_embeddings,
        run_config=run_config
    )
    
    print("\n==========================================")
    print(" RÉSULTATS DE L'ÉVALUATION BASELINE S4")
    print("==========================================")
    print(results)
    
    # Formatage du tableau Markdown
    print("\n### Baseline S4 Results Table")
    print("| Metric | Score |")
    print("|---|---|")
    for k, v in results._repr_dict.items():
         print(f"| {k} | {v:.4f} |")
         
    # Sauvegarde du rapport final
    report_path = Path(__file__).parent / "baseline_eval_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results._repr_dict, f, indent=2, ensure_ascii=False)
    print(f"\nRapport final sauvegardé dans {report_path}")

if __name__ == "__main__":
    main()
