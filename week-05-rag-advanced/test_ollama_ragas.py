import os
import sys
import types
from unittest.mock import MagicMock
from dotenv import load_dotenv

# Apply import patching for Vertex AI
dummy_module = types.ModuleType("langchain_community.chat_models.vertexai")
dummy_module.ChatVertexAI = MagicMock
sys.modules["langchain_community.chat_models.vertexai"] = dummy_module

from langchain_openai import ChatOpenAI
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import faithfulness, answer_relevancy
from ragas import evaluate
from datasets import Dataset
from langchain_community.embeddings import HuggingFaceEmbeddings
from ragas.embeddings import LangchainEmbeddingsWrapper

try:
    print("Initializing ChatOpenAI pointing to Ollama llama3.1...")
    ollama_llm = ChatOpenAI(
        model="llama3.1",
        api_key="ollama",  # Dummy API key for Ollama
        base_url="http://localhost:11434/v1",
        temperature=0
    )
    evaluator_llm = LangchainLLMWrapper(ollama_llm)
    print("Ollama wrapped successfully.")
    
    # Configure LLM on metrics
    faithfulness.llm = evaluator_llm
    answer_relevancy.llm = evaluator_llm
    
    # Setup local HuggingFace embeddings
    print("Initializing local HuggingFace embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-base")
    ragas_embeddings = LangchainEmbeddingsWrapper(embeddings)
    
    data = {
        "question": ["Quel est le protocole de consensus dans Raft ?"],
        "contexts": [["Le protocole Raft décompose le consensus en l'élection du leader, la réplication des logs et la sécurité."]],
        "answer": ["Raft décompose le consensus en élection du leader, réplication des logs et sécurité."],
        "ground_truth": ["L'élection du leader, la réplication des logs et la sécurité."]
    }
    
    dataset = Dataset.from_dict(data)
    print("Dataset created. Running evaluate...")
    
    results = evaluate(
        dataset=dataset,
        metrics=[faithfulness, answer_relevancy],
        llm=evaluator_llm,
        embeddings=ragas_embeddings
    )
    print("Evaluation completed successfully!")
    print("Results:", results)

except Exception as e:
    import traceback
    print("Error:")
    traceback.print_exc()
