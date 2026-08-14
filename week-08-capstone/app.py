import os
import gradio as gr
from dotenv import load_dotenv
from pathlib import Path
from langchain_core.messages import SystemMessage, HumanMessage

# Charger les variables d'environnement
ROADMAP_ROOT = Path(__file__).resolve().parent.parent
dotenv_path = ROADMAP_ROOT / ".env"
load_dotenv(dotenv_path)

# Importer les modules locaux
from core.rag import index_roadmap_files
from core.observability import setup_observability, guardrail_check
from core.agent import graph

# S'assurer que le RAG est indexé au démarrage
index_roadmap_files()
setup_observability()

def chat_function(message, history):
    # Vérification des garde-fous
    if not guardrail_check(message):
        yield "⚠️ Désolé, je ne peux pas traiter cette requête pour des raisons de sécurité."
        return

    system_prompt = "Tu es un AI Roadmap Assistant. Utilise l'outil search_local_docs pour trouver des informations sur les semaines 1 à 7 de la formation AI Engineering. Réponds toujours en français."
    
    # Reconstruire l'état initial
    initial_state = {
        "messages": [SystemMessage(content=system_prompt), HumanMessage(content=message)]
    }
    
    config = {"configurable": {"thread_id": "gradio_thread"}}
    
    full_response = ""
    
    try:
        # Streaming des événements LangGraph
        for event in graph.stream(initial_state, config=config, stream_mode="updates"):
            for node_name, update in event.items():
                if node_name == "tools":
                    # Si c'est l'outil qui a répondu, on peut l'afficher dans l'UI Gradio
                    yield full_response + "\n\n*(J'ai consulté la base de connaissances)*\n\n"
                    
                elif node_name == "agent":
                    # L'agent a produit un message
                    agent_msg = update["messages"][-1]
                    if agent_msg.content:
                        full_response = agent_msg.content
                        yield full_response
    except Exception as e:
        yield f"❌ Une erreur s'est produite : {str(e)}"

# Interface Gradio
demo = gr.ChatInterface(
    fn=chat_function,
    title="🚀 AI Roadmap Assistant",
    description="Posez-moi vos questions sur les semaines 1 à 7 de la formation AI Engineering !",
    examples=["Qu'est-ce que LiteLLM ?", "Comment fonctionne le RAG ?", "Quelles sont les bonnes pratiques d'observabilité de la semaine 7 ?"]
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
