import os
from pathlib import Path
from typing import TypedDict, Annotated
from dotenv import load_dotenv

# Setup paths
ROADMAP_ROOT = Path(__file__).resolve().parent.parent
dotenv_path = ROADMAP_ROOT / ".env"
load_dotenv(dotenv_path)

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# 1. Définition de l'état (State)
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Définition du premier outil de calcul (S6-J2-T3)
@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two integers together. Use this tool when asked to multiply numbers."""
    print(f"\n[OUTIL] Appel de multiply({a}, {b})...")
    return a * b

tools = [multiply]
tool_node = ToolNode(tools)

# 3. Initialisation du LLM local (Ollama llama3.1)
llm = ChatOpenAI(
    model="llama3.1",
    api_key="ollama",
    base_url="http://localhost:11434/v1",
    temperature=0
)

# Liaison des outils au LLM
llm_with_tools = llm.bind_tools(tools)

# 4. Définition du nœud de l'agent
def call_model(state: State):
    messages = state["messages"]
    print(f"\n[AGENT] Réflexion de l'agent sur l'historique (taille: {len(messages)})...")
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 5. Construction du StateGraph (S6-J2-T2)
builder = StateGraph(State)

builder.add_node("agent", call_model)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

def test_agent():
    print("--- DÉMARRAGE DE L'AGENT LANGGRAPH ---")
    
    initial_state = {
        "messages": [
            SystemMessage(content="Tu es un assistant précis doté d'outils de calcul."),
            ("user", "Combien font 35 fois 12 ? Donne-moi le résultat exact.")
        ]
    }
    
    for chunk in graph.stream(initial_state, stream_mode="values"):
        if "messages" in chunk:
            last_msg = chunk["messages"][-1]
            print(f"\n[{last_msg.__class__.__name__}] :")
            if last_msg.content:
                print(last_msg.content)
            if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                print(f"  Appels d'outils détectés : {last_msg.tool_calls}")

if __name__ == "__main__":
    test_agent()
