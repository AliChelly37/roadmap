import os
import json
import requests
from pathlib import Path
from typing import TypedDict, Annotated, List
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Setup paths
ROADMAP_ROOT = Path(__file__).resolve().parent.parent
dotenv_path = ROADMAP_ROOT / ".env"
load_dotenv(dotenv_path)

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
import chromadb
from chromadb.utils import embedding_functions

# 1. Définition de l'état
class ReportState(TypedDict):
    messages: Annotated[List[AIMessage | HumanMessage | SystemMessage | ToolMessage], add_messages]
    topic: str
    draft: str
    critique: str
    iteration: int
    filename: str

# 2. Définition des outils de production
@tool
def web_search(query: str) -> str:
    """Searches the web for information using DuckDuckGo. Use this tool to get up-to-date facts."""
    print(f"\n[OUTIL] Recherche Web pour : '{query}'...")
    try:
        ddg = DuckDuckGoSearchRun()
        return ddg.invoke(query)
    except Exception as e:
        return f"Erreur de recherche : {e}"

@tool
def scrape_url(url: str) -> str:
    """Scrapes and extracts all text content from a web page URL. Use this to read details of specific pages."""
    print(f"\n[OUTIL] Scraping URL : '{url}'...")
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for s in soup(["script", "style"]):
            s.decompose()
        text = soup.get_text(separator=' ')
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        # Tronquer à 3500 caractères pour ne pas saturer le contexte
        return text[:3500]
    except Exception as e:
        return f"Erreur lors du scraping de l'URL : {e}"

@tool
def search_my_docs(query: str) -> str:
    """Searches our local database of technical documents. Use this first for topics related to Raft, multi-agents, or consensus."""
    print(f"\n[OUTIL] Recherche dans la base locale (RAG) pour : '{query}'...")
    try:
        db_path = str(ROADMAP_ROOT / "week-04-rag-chat-docs" / "chroma_db")
        client = chromadb.PersistentClient(path=db_path)
        sbert_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="intfloat/multilingual-e5-base")
        
        # Interroger la collection de référence
        collection = client.get_collection(name="rag_document_test", embedding_function=sbert_fn)
        results = collection.query(
            query_texts=[f"query: {query}"],
            n_results=3
        )
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        
        if not documents:
            return "Aucun document local pertinent trouvé."
            
        formatted_docs = []
        for idx, doc in enumerate(documents):
            meta = metadatas[idx] if idx < len(metadatas) else {}
            formatted_docs.append(f"Document {idx+1} [Page {meta.get('page', 'Inconnue')}]:\n{doc}")
        return "\n\n".join(formatted_docs)
    except Exception as e:
        return f"Erreur d'accès à la base locale RAG : {e}"

@tool
def save_markdown(content: str, filename: str) -> str:
    """Saves the final report as a markdown file on the local machine."""
    print(f"\n[OUTIL] Sauvegarde du rapport dans '{filename}'...")
    try:
        # Enregistrer dans le dossier week-06-agent
        output_dir = Path(__file__).parent
        filepath = output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Rapport sauvegardé avec succès dans '{filepath.resolve()}' !"
    except Exception as e:
        return f"Erreur de sauvegarde : {e}"

# Configuration des outils pour LangGraph
tools = [web_search, scrape_url, search_my_docs, save_markdown]
tool_node = ToolNode(tools)

# Initialisation du LLM local
llm = ChatOpenAI(
    model="llama3.1",
    api_key="ollama",
    base_url="http://localhost:11434/v1",
    temperature=0
)
llm_with_tools = llm.bind_tools(tools)

# 3. Définition des nœuds du Graphe

def research_node(state: ReportState):
    """Nœud 1 : Détermine si de nouvelles informations sont requises et appelle les outils."""
    messages = state["messages"]
    iteration = state["iteration"]
    topic = state["topic"]
    critique = state["critique"]
    
    print(f"\n--- NŒUD : RECHERCHE (Itération {iteration}/4) ---")
    
    # Construction du prompt de recherche
    system_prompt = f"""Tu es un chercheur expert chargé de rassembler des faits solides pour rédiger un rapport sur le sujet : '{topic}'.
Tu as accès à la recherche locale (search_my_docs), la recherche web (web_search) et le scraping de pages (scrape_url).

Consignes :
1. Recherche activement des détails précis. Si tu as déjà des retours d'auto-critique, fais des recherches ciblées pour combler ces lacunes.
2. Si tu estimes avoir récolté assez de faits pertinents, réponds simplement : 'RECHERCHE_TERMINEE'."""

    if critique:
        system_prompt += f"\n\nVoici les lacunes identifiées lors du dernier examen critique, concentre tes recherches là-dessus :\n{critique}"

    # Appel au modèle
    response = llm_with_tools.invoke([SystemMessage(content=system_prompt)] + messages)
    return {"messages": [response]}

def draft_node(state: ReportState):
    """Nœud 2 : Rédige ou révise le brouillon du rapport en se basant sur les recherches."""
    messages = state["messages"]
    topic = state["topic"]
    critique = state["critique"]
    current_draft = state["draft"]
    
    print(f"\n--- NŒUD : RÉDACTION ---")
    
    prompt = f"""Rédige un rapport analytique complet, structuré et professionnel sur le sujet : '{topic}'.

Base-toi uniquement sur les faits collectés dans la conversation.
Si un brouillon existe déjà, intègre les corrections demandées par l'auto-critique pour l'améliorer."""

    if critique:
        prompt += f"\n\nAuto-critique à appliquer :\n{critique}\n\nBrouillon actuel :\n{current_draft}"

    response = llm.invoke([SystemMessage(content=prompt)] + messages)
    return {"draft": response.content}

def critique_node(state: ReportState):
    """Nœud 3 : Analyse le brouillon et produit une auto-critique constructive."""
    draft = state["draft"]
    topic = state["topic"]
    
    print(f"\n--- NŒUD : AUTO-CRITIQUE ---")
    
    prompt = f"""Analyse de manière rigoureuse le rapport d'analyse ci-dessous par rapport au sujet demandé : '{topic}'.
Tu dois identifier ce qui manque, ce qui est vague ou ce qui manque de sources.

Format de sortie structuré obligatoire (uniquement un objet JSON valide, pas d'explication externe) :
{{
  "approved": true ou false (met true uniquement si le rapport est parfait, sourcé et complet),
  "critique": "Détail précis des lacunes à corriger, ou 'Aucune' si approuvé."
}}

Rapport à évaluer :
{draft}
"""
    response = llm.invoke(prompt)
    content = response.content.strip()
    
    # Extraction sécurisée du JSON
    try:
        # Trouver les accolades
        start = content.find('{')
        end = content.rfind('}')
        data = json.loads(content[start:end+1])
        approved = data.get("approved", False)
        critique_text = data.get("critique", "Rejeté pour réévaluation.")
    except Exception:
        approved = False
        critique_text = "Échec du parsing de l'auto-critique. Rejeté pour réévaluation générale."

    print(f"  Approuvé par l'auto-critique : {approved}")
    print(f"  Critique : {critique_text}")
    
    return {
        "critique": critique_text,
        "iteration": state["iteration"] + 1,
        # On ajoute le statut d'approbation temporaire dans l'historique sous forme de message
        "messages": [AIMessage(content=f"Evaluation critique : {critique_text} (Approuvé : {approved})")]
    }

def save_node(state: ReportState):
    """Nœud 4 : Enregistre le rapport final sous format Markdown."""
    draft = state["draft"]
    filename = state["filename"]
    iteration = state["iteration"]
    
    print(f"\n--- NŒUD : SAUVEGARDE FINALE ---")
    
    final_content = draft
    # Si la limite est atteinte, ajouter les pistes non explorées (critère de sécurité)
    if iteration >= 4:
        final_content += "\n\n## 🔍 Pistes non explorées (Limite d'itérations atteinte)\n"
        final_content += "- Analyse comparative approfondie à grande échelle.\n"
        final_content += "- Retour d'expérience utilisateur en production.\n"
        final_content += f"- Retours d'auto-critique restants : {state['critique']}\n"
        
    save_markdown.invoke({"content": final_content, "filename": filename})
    return {"messages": [AIMessage(content=f"Rapport sauvegardé dans {filename}")]}

# 4. Définition de la logique d'aiguillage (Routing)

def should_continue_research(state: ReportState):
    """Détermine s'il faut appeler un outil de recherche ou passer à la rédaction."""
    last_message = state["messages"][-1]
    
    # S'il y a des appels d'outils, on va sur le nœud tools
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
         return "tools"
         
    # Si l'agent estime avoir fini ou s'il a renvoyé le signal d'arrêt de recherche
    if last_message.content and "RECHERCHE_TERMINEE" in last_message.content:
         return "draft"
         
    return "draft"

def should_loop_back(state: ReportState):
    """Vérifie si l'auto-critique a validé le rapport ou si la limite d'itérations est atteinte."""
    last_msg_content = state["messages"][-1].content
    approved = "(Approuvé : True)" in last_msg_content or "(Approuvé : true)" in last_msg_content
    iteration = state["iteration"]
    
    if approved or iteration >= 4:
         return "save"
    return "research"

# 5. Assemblage du StateGraph complet

builder = StateGraph(ReportState)

builder.add_node("research", research_node)
builder.add_node("tools", tool_node)
builder.add_node("draft", draft_node)
builder.add_node("critique", critique_node)
builder.add_node("save", save_node)

builder.add_edge(START, "research")

builder.add_conditional_edges(
    "research",
    should_continue_research,
    {
        "tools": "tools",
        "draft": "draft"
    }
)
builder.add_edge("tools", "research")

builder.add_edge("draft", "critique")

builder.add_conditional_edges(
    "critique",
    should_loop_back,
    {
        "research": "research",
        "save": "save"
    }
)

builder.add_edge("save", END)

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

def run_analytical_agent(topic: str, filename: str = "rapport_final.md"):
    print(f"\n=== LANCEMENT DE L'AGENT ANALYTIQUE POUR LE SUJET : '{topic}' ===")
    config = {"configurable": {"thread_id": "report_thread_1"}}
    
    initial_state = {
        "messages": [],
        "topic": topic,
        "draft": "",
        "critique": "",
        "iteration": 0,
        "filename": filename
    }
    
    for event in graph.stream(initial_state, config, stream_mode="updates"):
        for node_name, update in event.items():
            print(f"\n[Mise à jour Graphe - Nœud: '{node_name}']")
            if "draft" in update:
                 print(f"  -> Brouillon généré ({len(update['draft'])} caractères).")
            if "critique" in update:
                 print(f"  -> Auto-Critique : {update['critique']}")
            if "iteration" in update:
                 print(f"  -> Compteur itération : {update['iteration']}")

if __name__ == "__main__":
    run_analytical_agent(
        topic="Analyse des avantages du protocole Raft par rapport à Paxos dans les systèmes multi-agents",
        filename="rapport_raft_multi_agents.md"
    )
