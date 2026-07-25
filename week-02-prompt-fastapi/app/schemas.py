from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

# --- Enumerations ---
# Une Enum est une liste de valeurs autorisées.
# Ici on hérite de str pour que la valeur JSON soit une string lisible
# au lieu d'un entier (ex: "ouvert" au lieu de 0).

class IssueStatus(str, Enum):
    """Les états possibles d'un ticket."""
    OPEN = "ouvert"
    IN_PROGRESS = "en cours"
    CLOSED = "fermé"

class IssuePriority(str, Enum):
    """Les niveaux de priorité possibles pour un ticket."""
    LOW = "basse"
    MEDIUM = "moyenne"
    HIGH = "haute"

# --- Modèles Pydantic ---
# Ces classes définissent le format JSON attendu ou renvoyé par l'API.
# Pydantic valide automatiquement les données et renvoie une erreur 422
# si le format ne correspond pas.

class IssueCreation(BaseModel):
    """
    Modèle pour la CRÉATION d'un ticket (ce que l'utilisateur envoie via POST).
    Field(...) signifie que le champ est obligatoire (le "..." = requis).
    """
    title: str = Field(..., min_length=5, description="Titre du problème")
    description: str = Field(..., min_length=10, description="Description détaillée du problème")
    priority: IssuePriority = IssuePriority.MEDIUM  # Valeur par défaut : priorité moyenne

class IssueUpdate(BaseModel):
    """
    Modèle pour la MISE À JOUR d'un ticket (PATCH/PUT).
    Tous les champs sont Optional car l'utilisateur peut n'en modifier qu'un seul.
    None signifie "non modifié".
    """
    title: Optional[str] = Field(None, min_length=5, description="Nouveau titre")
    description: Optional[str] = Field(None, min_length=10, description="Nouvelle description")
    priority: Optional[IssuePriority] = None
    status: Optional[IssueStatus] = None

class IssueOut(BaseModel):
    """
    Modèle de RÉPONSE renvoyé par l'API (ce que le client reçoit).
    Contient toutes les infos d'un ticket, y compris l'ID généré et le statut.
    """
    id: str
    title: str
    description: str
    priority: IssuePriority
    status: IssueStatus


# --- Modèles pour la route /chat ---

class ChatRequest(BaseModel):
    """
    Ce que le client envoie pour parler au LLM.
    - message : le texte de l'utilisateur.
    - system_prompt : permet de personnaliser le rôle du LLM (optionnel).
                      Ex: "Tu es un expert en cybersécurité."
    - model : le modèle LLM à utiliser (optionnel, valeur par défaut : llama3.2).
    """
    message: str = Field(..., description="Le message de l'utilisateur")
    system_prompt: Optional[str] = Field(
        default="Tu es un assistant IA utile et concis. Réponds toujours en français.",
        description="Le rôle et le comportement du LLM"
    )
    model: Optional[str] = Field(default="llama3.2", description="Le modèle LLM à utiliser")


class ChatResponse(BaseModel):
    """
    Ce que l'API renvoie après avoir interrogé le LLM.
    - response : la réponse textuelle du LLM.
    - model : le modèle qui a généré la réponse (pour traçabilité).
    """
    response: str
    model: str


# --- Modèles pour la route /extract ---

class PersonExtract(BaseModel):
    """
    Le JSON structuré extrait par le LLM à partir d'un texte brouillon.
    Tous les champs sont Optional car le texte fourni peut ne pas contenir l'info.
    Ex: "Je m'appelle Ali, j'ai 30 ans" → pas de profession ni de ville.
    """
    nom: Optional[str] = Field(None, description="Nom complet de la personne")
    age: Optional[int] = Field(None, description="Age de la personne")
    profession: Optional[str] = Field(None, description="Métier ou profession")
    ville: Optional[str] = Field(None, description="Ville de résidence")


class ExtractRequest(BaseModel):
    """
    Ce que le client envoie à la route /extract.
    - text : le texte brouillon à analyser.
    - model : le modèle LLM à utiliser (optionnel).
    """
    text: str = Field(..., description="Le texte brouillon dont on veut extraire les infos")
    model: Optional[str] = Field(default="llama3.2", description="Le modèle LLM à utiliser")
