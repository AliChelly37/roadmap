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
from sentence_transformers import CrossEncoder
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document

class RerankedRAG:
    def __init__(self):
        # 1. Initialiser le RAG hybride (BM25 + Chroma)
        self.hybrid_rag = HybridRAG()
        # 2. Charger le reranker local
        print("Chargement du Reranker local BAAI/bge-reranker-v2-m3...")
        self.reranker = CrossEncoder("BAAI/bge-reranker-v2-m3")

    def retrieve_and_rerank(self, query: str, retrieve_top_k: int = 20, rerank_top_n: int = 5) -> list[Document]:
        """
        Récupère top_k documents via recherche hybride, puis les ordonne via Reranker pour renvoyer top_n.
        """
        # A. Retrieval hybride large (top-k)
        docs = self.hybrid_rag.retrieve(query, top_n=retrieve_top_k)
        if not docs:
            return []
            
        # B. Calcul des scores du Reranker
        print(f"Reranking de {len(docs)} documents candidats...")
        pairs = [[query, doc.page_content] for doc in docs]
        scores = self.reranker.predict(pairs)
        
        # C. Injection des scores dans les métadonnées et tri
        for doc, score in zip(docs, scores):
            doc.metadata["rerank_score"] = float(score)
            
        sorted_docs = sorted(docs, key=lambda x: x.metadata["rerank_score"], reverse=True)
        
        # Affichage du classement comparé RRF vs Reranker pour l'audit
        print("\n--- AUDIT RERANKING (Top 10) ---")
        for idx, d in enumerate(sorted_docs[:10]):
            ret_type = d.metadata.get("retriever", "inconnu")
            rrf = d.metadata.get("rrf_score", 0.0)
            rerank_val = d.metadata.get("rerank_score", 0.0)
            print(f"Rang {idx+1} | Rerank-Score: {rerank_val:.4f} | RRF-Score: {rrf:.6f} | Type: {ret_type} | Texte: {d.page_content[:90].replace(chr(10), ' ')}...")
            
        return sorted_docs[:rerank_top_n]

def ask_reranked_rag(question):
    rag = RerankedRAG()
    # Récupérer top-20 hybride -> Rerank -> Top-5
    docs = rag.retrieve_and_rerank(question, retrieve_top_k=20, rerank_top_n=5)
    
    if not docs:
        print("Aucun document n'a été trouvé.")
        return
        
    prompt = build_prompt(question, docs)
    
    # Appel LLM Ollama local
    try:
        llm = ChatOpenAI(
            model="llama3.1",
            api_key="ollama",
            base_url="http://localhost:11434/v1",
            temperature=0
        )
        response = llm.invoke(prompt)
        print("\n--- REPONSE ANCREE AVEC RERANKER (OLLAMA LLAMA3.1) ---")
        print(response.content)
        print("---------------------------------\n")
    except Exception as e:
        print(f"Erreur lors de la génération avec Ollama : {e}")

if __name__ == "__main__":
    question = "Qu'est-ce que le protocole Raft et quels sont ses trois états ?"
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
        
    ask_reranked_rag(question)
