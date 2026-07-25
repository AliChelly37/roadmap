from fastapi import APIRouter, HTTPException, status
import uuid  # Module natif Python pour générer des IDs uniques (ex: "a1b2-c3d4-...")
from app.storage import load_data, save_data
from app.schemas import IssueCreation, IssueOut, IssueStatus

# --- Création du Router ---
# APIRouter est comme une "mini-application" FastAPI qui gère un groupe de routes.
# prefix="/api/V1/issues" : toutes les routes de ce fichier commenceront par cette URL.
# tags=["issues"] : regroupe ces routes dans la doc Swagger sous l'onglet "issues".
router = APIRouter(prefix="/api/V1/issues", tags=["issues"])


@router.get("")  # Route complète : GET /api/V1/issues
async def get_issues():
    """Retourne la liste de tous les tickets existants."""
    data = load_data()  # On lit le fichier JSON
    return data  # FastAPI convertit automatiquement la liste Python en JSON


@router.post("/", response_model=IssueOut, status_code=status.HTTP_201_CREATED)
# response_model=IssueOut : FastAPI s'assure que la réponse respecte ce modèle Pydantic
# status_code=201 : on répond "201 Created" au lieu du "200 OK" par défaut
def create_issue(payload: IssueCreation):
    """
    Crée un nouveau ticket.
    FastAPI valide automatiquement le JSON entrant selon le modèle IssueCreation.
    """
    data = load_data()               # 1. Charge les tickets existants
    issue_id = str(uuid.uuid4())     # 2. Génère un ID unique (ex: "550e8400-e29b-...")

    # 3. Crée l'objet IssueOut (le ticket complet avec son ID et son statut initial)
    new_issue = IssueOut(
        id=issue_id,
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        status=IssueStatus.OPEN      # Tout nouveau ticket commence avec le statut "ouvert"
    )

    # 4. Ajoute le ticket (converti en dictionnaire) à la liste des données
    data.append(new_issue.model_dump())

    # 5. Sauvegarde les données mises à jour dans le fichier JSON
    save_data(data)

    # 6. Retourne l'objet Pydantic (FastAPI le convertira en JSON pour le client)
    return new_issue
