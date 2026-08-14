import os
from typing import TypedDict, Annotated, List
from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

# Nos modules internes
from core.rag import search_roadmap, DEFAULT_N_RESULTS
from core.observability import observe
from core.llm_gateway import get_llm_response

class AgentState(TypedDict):
    messages: Annotated[List[AIMessage | HumanMessage | SystemMessage | ToolMessage], add_messages]

SYSTEM_PROMPT = (
    "Tu es l'AI Roadmap Assistant. Ta base de connaissances est constituée des "
    "MÉMOS personnels rédigés par l'utilisateur pendant sa formation AI Engineering "
    "de 8 semaines : fondations LLM, prompt engineering, embeddings, RAG de base "
    "puis avancé, agents, LLMOps, capstone, plus quelques mémos transverses "
    "(Git, garde-fous, system design).\n"
    "Règles :\n"
    "1. Utilise TOUJOURS l'outil search_local_docs avant de répondre.\n"
    "2. Interroge-le avec des termes techniques précis (« cross-encoder reranking », "
    "« HNSW »), pas avec des méta-mots comme « semaine 5 » ou « formation ».\n"
    "3. Réponds uniquement à partir du contexte récupéré, et cite le mémo source.\n"
    "4. Ce sont les notes de l'utilisateur : tu lui restitues ce que LUI a écrit. "
    "Si l'information n'y est pas, dis-le franchement plutôt que de compléter avec "
    "tes connaissances générales.\n"
    "5. Réponds toujours en français."
)


@tool
def search_local_docs(query: str) -> str:
    """Recherche dans les mémos de la formation (RAG, agents, LLMOps, embeddings...).

    Formule la requête avec des termes techniques précis. Évite les méta-mots
    (« semaine 5 », « formation ») : ils matchent large et noient le mémo visé.
    """
    print(f"\n[OUTIL] Recherche RAG pour : '{query}'...")
    return search_roadmap(query, n_results=DEFAULT_N_RESULTS)

tools = [search_local_docs]
tool_node = ToolNode(tools)

# On wrap l'appel LiteLLM pour LangGraph
def call_model(state: AgentState):
    messages = state["messages"]
    
    from langchain_openai import ChatOpenAI
    
    # Si on a la clé OpenRouter, on l'utilise (pour la Prod HF Spaces / Cloud)
    if os.getenv("OPENROUTER_API_KEY"):
        llm = ChatOpenAI(
            model="meta-llama/llama-3.1-8b-instruct",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
            temperature=0
        )
    else:
        # Fallback sur Ollama en local
        llm = ChatOpenAI(
            model="llama3.1",
            api_key="ollama",
            base_url="http://localhost:11434/v1",
            temperature=0
        )
        
    llm_with_tools = llm.bind_tools(tools)
    
    print("\n--- NŒUD : AGENT ---")
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

# Assemblage
builder = StateGraph(AgentState)
builder.add_node("agent", call_model)
builder.add_node("tools", tool_node)
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
builder.add_edge("tools", "agent")

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

@observe(name="agent_workflow") # Tracing Langfuse
def run_agent(user_input: str, thread_id: str = "thread_1"):
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "messages": [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_input)
        ]
    }
    
    final_state = graph.invoke(initial_state, config=config)
    return final_state["messages"][-1].content
