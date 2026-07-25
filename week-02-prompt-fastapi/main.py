from fastapi import FastAPI
from app.routes.issues import router as issues_router
from app.routes.chat import router as chat_router  # On importe aussi le router de chat
from app.routes.extract import router as extract_router  # On importe le router d'extraction

# On instancie l'application FastAPI principale
# C'est le "chef d'orchestre" qui reçoit toutes les requêtes HTTP
app = FastAPI()

# On "branche" le router issues sur l'application principale.
# Toutes les routes définies dans issues.py (avec le préfixe /api/V1/issues)
# sont maintenant accessibles via cette application.
app.include_router(issues_router)

# On branche le router chat.
# Toutes les routes de chat.py (avec le préfixe /chat) sont maintenant actives.
app.include_router(chat_router)

# On branche le router extract.
app.include_router(extract_router)

from fastapi.responses import HTMLResponse
import os

@app.get("/", response_class=HTMLResponse)
async def read_index():
    """Sert la page d'accueil avec l'interface de chat en streaming."""
    file_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

