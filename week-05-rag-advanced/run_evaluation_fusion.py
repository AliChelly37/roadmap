import os
import sys
import json
import types
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
from ragas.run_config import RunConfig

# 3. Import du RAG-Fusion Pipeline
from query_transform import RAGFusionPipeline, build_prompt

def run_fusion_rag_on_dataset(eval_set_path, results_output_path):
    print(f"Chargement du jeu de test : {eval_set_path}")
    with open(eval_set_path, "r", encoding="utf-8") as f:
        eval_set = json.load(f)

    # Initialisation du pipeline RAG-Fusion
    pipeline = RAGFusionPipeline()
    results = []

    print("\n--- Étape 1/2 : Génération des réponses RAG (RAG-Fusion) ---")

    for i, item in enumerate(eval_set):
        question = item["question"]
        print(f"\n[{i+1}/{len(eval_set)}] Question : {question}")
        
        # Exécution du RAG-Fusion avec Reranker (top-20 candidats -> top-5)
        docs = pipeline.retrieve_rag_fusion(question, retrieve_top_k=20, rerank_top_n=5)
        context_texts = [d.page_content for d in docs]
        
        if not docs:
            print("  Aucun document trouvé.")
            answer = "Je ne sais pas."
        else:
            best_rerank_score = docs[0].metadata.get("rerank_score", 0.0)
            
            # Garde sémantique
            if best_rerank_score < 0.01:
                print(f"  [Garde de Rerank activée] Meilleur score : {best_rerank_score:.4f} < 0.01")
                answer = "Je ne sais pas."
                context_texts = []
            else:
                prompt = build_prompt(question, docs)
                try:
                    response = pipeline.llm.invoke(prompt)
                    answer = response.content or ""
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
    results_path = Path(__file__).parent / "fusion_results_temp.json"
    
    if not results_path.exists():
        rag_data = run_fusion_rag_on_dataset(eval_set_path, results_path)
    else:
        print(f"Chargement des réponses RAG existantes depuis {results_path}...")
        with open(results_path, "r", encoding="utf-8") as f:
            rag_data = json.load(f)

    # 4. Préparation des données pour RAGAS
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
    
    # 5. Évaluation RAGAS
    print("\n--- Étape 2/2 : Évaluation RAGAS ---")
    from ragas.llms import LangchainLLMWrapper
    from langchain_openai import ChatOpenAI
    
    print("Initialisation d'Ollama avec le modèle local llama3.1 pour l'évaluateur...")
    ollama_llm = ChatOpenAI(
        model="llama3.1",
        api_key="ollama",
        base_url="http://localhost:11434/v1",
        temperature=0
    )
    evaluator_llm = LangchainLLMWrapper(ollama_llm)
    
    faithfulness.llm = evaluator_llm
    answer_relevancy.llm = evaluator_llm
    context_precision.llm = evaluator_llm
    context_recall.llm = evaluator_llm
    
    embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base")
    ragas_embeddings = LangchainEmbeddingsWrapper(embeddings)
    
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
    print(" RÉSULTATS DE L'ÉVALUATION RAG-FUSION")
    print("==========================================")
    print(results)
    
    # Tableau Markdown
    print("\n### RAG-Fusion Results Table")
    print("| Metric | Score |")
    print("|---|---|")
    for k, v in results._repr_dict.items():
         print(f"| {k} | {v:.4f} |")
         
    # Sauvegarde du rapport final
    report_path = Path(__file__).parent / "fusion_eval_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
         json.dump(results._repr_dict, f, indent=2, ensure_ascii=False)
    print(f"\nRapport final sauvegardé dans {report_path}")

if __name__ == "__main__":
    main()
