"""AI Roadmap Assistant — serveur FastAPI + front statique.

Gradio a été abandonné : en v6 il ne laisse plus passer de CSS sur
ChatInterface et son DOM lui appartient, ce qui rend un habillage précis
(neumorphisme = contrôle du fond et des deux ombres sur chaque surface)
impossible à tenir dans la durée.

Le streaming SSE reprend la brique de la Semaine 6 (week-06-agent/server.py),
et le front statique le motif des Semaines 2 à 4 (index.html écrit à la main).
"""
import json
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

BASE_DIR = Path(__file__).resolve().parent
ROADMAP_ROOT = BASE_DIR.parent
load_dotenv(ROADMAP_ROOT / ".env")

from core.rag import index_roadmap_files, NO_RELEVANT_CONTENT
from core.observability import get_langfuse_handler, guardrail_check
from core.agent import graph, SYSTEM_PROMPT

# En Docker l'index est déjà construit au build : cet appel ne fait que le vérifier.
index_roadmap_files()
LANGFUSE_HANDLER = get_langfuse_handler()

app = FastAPI(title="AI Roadmap Assistant", docs_url=None, redoc_url=None)


class ChatRequest(BaseModel):
    message: str
    session_id: str = "anonymous"
    history: list = []


def _history_to_messages(history):
    """Historique client -> messages LangChain."""
    messages = []
    for item in history or []:
        role = item.get("role")
        content = (item.get("content") or "").strip()
        if not content:
            continue
        messages.append(HumanMessage(content=content) if role == "user"
                        else AIMessage(content=content))
    return messages


def _sse(payload: dict) -> str:
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


def _run_agent(message: str, session_id: str, history: list):
    """Générateur SSE : consultation de l'outil, réponse, provenance."""
    # Garde-fou d'entrée (OWASP LLM01) — avant tout appel au modèle.
    if not guardrail_check(message):
        yield _sse({
            "type": "blocked",
            "content": ("Cette requête cherche à modifier mes instructions, je ne peux "
                        "pas la traiter. Pose ta question sur le contenu de tes mémos."),
        })
        return

    # Un thread par session : sans ça tous les visiteurs partageraient le
    # checkpointer LangGraph, donc la mémoire de conversation de chacun.
    config = {"configurable": {"thread_id": session_id or "anonymous"}}
    if LANGFUSE_HANDLER is not None:
        config["callbacks"] = [LANGFUSE_HANDLER]

    state = {
        "messages": [SystemMessage(content=SYSTEM_PROMPT)]
        + _history_to_messages(history)
        + [HumanMessage(content=message)]
    }

    answer = ""
    weeks, transverse = set(), False
    searched, grounded = False, False

    try:
        for event in graph.stream(state, config=config, stream_mode="updates"):
            for node, update in event.items():
                if node == "tools":
                    tool_text = str(update["messages"][-1].content)
                    searched = True
                    # Au moins une recherche a ramené du contenu réel.
                    grounded = grounded or NO_RELEVANT_CONTENT[:24] not in tool_text
                    weeks |= {int(w) for w in re.findall(r"\[S(\d)\]", tool_text)}
                    transverse = transverse or "[transverse]" in tool_text
                    yield _sse({"type": "tool", "weeks": sorted(weeks)})

                elif node == "agent":
                    msg = update["messages"][-1]
                    if msg.content:
                        answer = msg.content
                        yield _sse({"type": "message", "content": answer})

        # Filet déterministe. Le système prompt demande déjà de refuser hors corpus,
        # mais un modèle 8B suit mal cette consigne quand il « connaît » la réponse :
        # il a répondu « Sydney » pour la capitale de l'Australie (faux de surcroît).
        # Ici on ne demande plus, on impose : si aucune recherche n'a ramené de
        # contenu pertinent, la réponse du modèle est écartée.
        if searched and not grounded:
            answer = ("Ce sujet n'est pas couvert par tes mémos. Je ne réponds qu'à "
                      "partir de tes notes de la formation — pour le reste, mieux vaut "
                      "une source dédiée.")
            yield _sse({"type": "message", "content": answer})

        elif not answer:
            answer = ("Je n'ai rien trouvé là-dessus dans tes mémos. Vise une "
                      "notion précise — « reranking », « HNSW », « LangGraph ».")
            yield _sse({"type": "message", "content": answer})

        # Les mémos transverses n'ont pas de position sur le rail : on ne les
        # signale que s'ils ont répondu seuls, sinon la pastille ne dit rien.
        yield _sse({
            "type": "done",
            "weeks": sorted(weeks),
            "transverse": transverse and not weeks,
        })

    except Exception as exc:
        print(f"[ERREUR] {type(exc).__name__}: {exc}")
        yield _sse({
            "type": "error",
            "content": "Le service LLM ne répond pas. Réessaie dans un instant.",
        })


@app.post("/api/chat")
def chat(req: ChatRequest):
    return StreamingResponse(
        _run_agent(req.message, req.session_id, req.history),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/health")
def health():
    from core.rag import get_collection
    return {"status": "ok", "chunks": get_collection().count()}


@app.get("/")
def index():
    return FileResponse(BASE_DIR / "static" / "index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))
