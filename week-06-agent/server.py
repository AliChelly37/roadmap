import os
import json
import asyncio
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Setup paths
ROADMAP_ROOT = Path(__file__).resolve().parent.parent
dotenv_path = ROADMAP_ROOT / ".env"
load_dotenv(dotenv_path)

from advanced_agent import graph

app = FastAPI(title="LangGraph Agent Streaming API", version="1.0")

class AgentRequest(BaseModel):
    topic: str
    filename: str = "rapport_stream_final.md"

@app.get("/")
def read_root():
    return {"message": "LangGraph Streaming Server is running!"}

@app.post("/agent")
async def stream_agent(request: AgentRequest):
    """
    Exécute le graphe LangGraph de recherche et rédaction de rapports
    et diffuse la trace des étapes en temps réel via Server-Sent Events (SSE).
    """
    config = {"configurable": {"thread_id": f"thread_{os.urandom(4).hex()}"}}
    
    initial_state = {
        "messages": [],
        "topic": request.topic,
        "draft": "",
        "critique": "",
        "iteration": 0,
        "filename": request.filename
    }

    async def event_generator():
        try:
            # Exécution synchrone dans un thread séparé pour ne pas bloquer l'event loop
            # On stream de manière itérative
            for event in graph.stream(initial_state, config, stream_mode="updates"):
                sse_data = {}
                for node_name, update in event.items():
                    sse_data["node"] = node_name
                    if "iteration" in update:
                        sse_data["iteration"] = update["iteration"]
                    if "critique" in update:
                        sse_data["critique"] = update["critique"]
                    if "draft" in update:
                        sse_data["draft_size"] = len(update["draft"])
                        sse_data["draft_preview"] = update["draft"][:100] + "..."
                
                yield f"data: {json.dumps(sse_data, ensure_ascii=False)}\n\n"
                await asyncio.sleep(0.5)
                
            yield "data: {\"status\": \"COMPLETED\"}\n\n"
        except Exception as e:
            yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
