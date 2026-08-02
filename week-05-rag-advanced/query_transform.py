import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Setup paths
ROADMAP_ROOT = Path(__file__).resolve().parent.parent
dotenv_path = ROADMAP_ROOT / ".env"
load_dotenv(dotenv_path)

from query_hybrid import HybridRAG, build_prompt
from query_rerank import RerankedRAG
from sentence_transformers import CrossEncoder
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document

class RAGFusionPipeline:
    def __init__(self):
        # 1. Charger le RerankedRAG (qui inclut déjà le HybridRAG et le Reranker)
        self.reranked_rag = RerankedRAG()
        # 2. Client LLM local pour générer les requêtes alternatives
        self.llm = ChatOpenAI(
            model="llama3.1",
            api_key="ollama",
            base_url="http://localhost:11434/v1",
            temperature=0.2
        )

    def generate_alternatives(self, query: str, count: int = 3) -> list[str]:
        """
        Génère des formulations alternatives de la question d'origine.
        """
        print(f"\nGénération de {count} requêtes alternatives pour : '{query}'...")
        prompt = f"""Tu es un assistant IA spécialisé dans l'optimisation de recherche d'information.
Génère exactement {count} formulations alternatives de la question suivante pour aider à chercher des documents dans une base de données.
Tes variations doivent utiliser des synonymes ou aborder le problème sous un autre angle, tout en conservant le sens d'origine.
Donne uniquement les questions générées, une par ligne, sans aucun blabla, ni numérotation, ni introduction.

Question originale : {query}
Variations alternatives :"""
        
        try:
            response = self.llm.invoke(prompt)
            lines = response.content.strip().split("\n")
            # Nettoyage des lignes (au cas où le modèle met des tirets ou numéros)
            queries = []
            for line in lines:
                cleaned = line.strip()
                if not cleaned:
                    continue
                # Supprimer les tirets ou numéros de liste
                if cleaned.startswith("- ") or cleaned.startswith("* "):
                    cleaned = cleaned[2:]
                elif cleaned[0].isdigit() and cleaned[1:3] in (". ", ") "):
                    cleaned = cleaned[3:]
                queries.append(cleaned.strip())
            
            # Limiter au nombre demandé
            final_queries = queries[:count]
            print("Requêtes générées :")
            for q in final_queries:
                print(f"  - {q}")
            return final_queries
        except Exception as e:
            print(f"Erreur génération de requêtes : {e}")
            return []

    def retrieve_rag_fusion(self, query: str, retrieve_top_k: int = 20, rerank_top_n: int = 5) -> list[Document]:
        """
        Exécute la recherche RAG-Fusion : Multi-Query -> Hybrid Retrieval -> RRF -> Reranking.
        """
        # A. Générer les alternatives
        alt_queries = self.generate_alternatives(query, count=3)
        all_queries = [query] + alt_queries
        
        # B. Lancer les recherches pour toutes les requêtes
        print(f"\nExécution des recherches hybrides pour les {len(all_queries)} requêtes...")
        
        # RRF de RAG-Fusion : Dictionnaire pour combiner les rangs de toutes les requêtes
        fusion_scores = {}
        doc_map = {}
        k_const = 60  # Constante de lissage RRF
        
        for q_idx, q in enumerate(all_queries):
            # Pour chaque requête, récupérer le top-10 hybride
            q_docs = self.reranked_rag.hybrid_rag.retrieve(q, top_n=10)
            
            for rank, doc in enumerate(q_docs, start=1):
                doc_key = doc.page_content.strip()
                doc_map[doc_key] = doc
                
                if doc_key not in fusion_scores:
                    fusion_scores[doc_key] = 0.0
                
                # Additionner les scores réciproques de tous les retrievals
                fusion_scores[doc_key] += 1.0 / (k_const + rank)
        
        # C. Classer tous les documents fusionnés
        sorted_keys = sorted(fusion_scores.keys(), key=lambda x: fusion_scores[x], reverse=True)
        fused_docs = [doc_map[key] for key in sorted_keys[:retrieve_top_k]]
        
        # Conserver le score RAG-Fusion pour le débogage
        for doc in fused_docs:
            doc.metadata["fusion_score"] = fusion_scores[doc.page_content.strip()]
            
        # D. Rerank sur les candidats fusionnés
        print(f"Reranking de {len(fused_docs)} candidats fusionnés uniques...")
        pairs = [[query, doc.page_content] for doc in fused_docs]
        scores = self.reranked_rag.reranker.predict(pairs)
        
        for doc, score in zip(fused_docs, scores):
            doc.metadata["rerank_score"] = float(score)
            
        sorted_docs = sorted(fused_docs, key=lambda x: x.metadata["rerank_score"], reverse=True)
        
        # Audit logs
        print("\n--- AUDIT RAG-FUSION & RERANKING (Top 10) ---")
        for idx, d in enumerate(sorted_docs[:10]):
            ret_type = d.metadata.get("retriever", "inconnu")
            fus = d.metadata.get("fusion_score", 0.0)
            rerank_val = d.metadata.get("rerank_score", 0.0)
            print(f"Rang {idx+1} | Rerank: {rerank_val:.4f} | Fusion: {fus:.6f} | Type: {ret_type} | Texte: {d.page_content[:90].replace(chr(10), ' ')}...")
            
        return sorted_docs[:rerank_top_n]

def ask_fusion_rag(question):
    pipeline = RAGFusionPipeline()
    docs = pipeline.retrieve_rag_fusion(question, retrieve_top_k=20, rerank_top_n=5)
    
    if not docs:
        print("Aucun document n'a été trouvé.")
        return
        
    prompt = build_prompt(question, docs)
    
    # Appel LLM Ollama local
    try:
        response = pipeline.llm.invoke(prompt)
        print("\n--- REPONSE ANCREE RAG-FUSION (OLLAMA LLAMA3.1) ---")
        print(response.content)
        print("---------------------------------\n")
    except Exception as e:
        print(f"Erreur lors de la génération avec Ollama : {e}")

if __name__ == "__main__":
    question = "Raft consensus, Paxos et latence"
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        
    ask_fusion_rag(question)
