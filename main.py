"""
Point d'entrée FastAPI : routes HTTP, montage des fichiers statiques, validation des requêtes.

Lancer en développement :
    python -m venv venv
    .\\venv\\Scripts\\activate        (Windows)
    pip install -r requirements.txt
    uvicorn main:app --reload

Puis ouvrir http://127.0.0.1:8000
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Literal

from pydantic import BaseModel, Field

from config import get_settings
from tutor import OFF_TOPIC_REPLY, ask_tutor
from grade_calculator import CalculateurNotes, NoteMatiere, generer_rapport
from modules_config import MODULES_DATA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="AskGL — Tuteur académique",
    description="AskGL : tutorat intelligent (informatique, mathématiques, sciences, langues, gestion).",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


class ChatMessage(BaseModel):
    """Un message de l'historique (côté client), rôle OpenAI."""

    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1, max_length=6000)


class ChatRequest(BaseModel):
    """Corps JSON attendu par l'endpoint de chat."""

    question: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="Dernière question de l'étudiant.",
    )
    history: list[ChatMessage] = Field(
        default_factory=list,
        max_length=30,
        description="Messages précédents (user / assistant) sans la question actuelle.",
    )


class ChatResponse(BaseModel):
    """Réponse JSON renvoyée au navigateur."""

    answer: str


class NoteMatiereRequest(BaseModel):
    """Notes d'une matière pour la requête API."""
    cc: float = Field(..., ge=0, le=20)
    examen: float = Field(..., ge=0, le=20)
    tp: float | None = Field(None, ge=0, le=20)


class ModuleGradesRequest(BaseModel):
    """Notes pour un module complet."""
    niveau: str
    semestre: str
    module_id: str
    parcours: str | None = None
    notes: dict[str, NoteMatiereRequest]


class AllModulesGradesRequest(BaseModel):
    """Notes pour tous les modules."""
    notes: dict[str, dict[str, NoteMatiereRequest]]


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Réponses JSON homogènes en cas d'erreur de validation Pydantic."""
    return JSONResponse(status_code=422, content={"detail": exc.errors(), "message": "Requête invalide."})


@app.get("/", response_class=HTMLResponse, tags=["Pages"])
async def index(request: Request) -> HTMLResponse:
    """Page principale : interface de chat."""
    settings = get_settings()
    boot = {
        "tutorName": settings.tutor_name,
        "offTopic": OFF_TOPIC_REPLY,
    }
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "tutor_name": settings.tutor_name,
            "boot_json": json.dumps(boot, ensure_ascii=False),
            "off_topic_message": OFF_TOPIC_REPLY,
        },
    )


@app.get("/grades", response_class=HTMLResponse, tags=["Pages"])
async def grades(request: Request) -> HTMLResponse:
    """Page de calcul de notes."""
    settings = get_settings()
    return templates.TemplateResponse(
        request=request,
        name="grades.html",
        context={
            "tutor_name": settings.tutor_name,
        },
    )


@app.post("/api/chat", response_model=ChatResponse, tags=["API"])
async def chat(payload: ChatRequest) -> ChatResponse:
    """
    Envoie la question au tuteur IA et renvoie la réponse.

    - Validation : longueur, type (Pydantic).
    - Erreurs métier : clé API manquante, erreurs OpenAI → HTTP 400 / 503 avec message clair.
    """
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="La question ne peut pas être vide.")

    history_pairs: list[tuple[str, str]] = [(m.role, m.content.strip()) for m in payload.history]

    settings = get_settings()

    try:
        answer = ask_tutor(settings, question, history_pairs)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        logger.warning("Erreur runtime tuteur : %s", exc)
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001 — filet de sécurité pour la soutenance
        logger.exception("Erreur inattendue dans /api/chat")
        raise HTTPException(
            status_code=500,
            detail="Une erreur interne est survenue. Consultez les logs du serveur.",
        ) from exc

    return ChatResponse(answer=answer)


@app.get("/health", tags=["API"])
async def health() -> dict[str, str]:
    """Vérification simple que l'application répond (utile pour démo / supervision)."""
    return {"status": "ok"}


# Routes pour le système de calcul de notes

@app.get("/api/modules", tags=["Notes"])
async def get_modules() -> dict:
    """Retourne tous les modules disponibles."""
    return MODULES_DATA


@app.get("/api/modules/{niveau}/{semestre}/{module_id}", tags=["Notes"])
async def get_module_details(niveau: str, semestre: str, module_id: str) -> dict:
    """Retourne les détails d'un module spécifique."""
    try:
        return MODULES_DATA[niveau][semestre][module_id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Module non trouvé")


@app.post("/api/grades/calculate-module", tags=["Notes"])
async def calculate_module_grades(payload: ModuleGradesRequest) -> dict:
    """Calcule les notes pour un module spécifique."""
    calculateur = CalculateurNotes()
    
    # Convertir les notes en format interne
    notes_matieres = {}
    for nom_matiere, note_req in payload.notes.items():
        notes_matieres[nom_matiere] = NoteMatiere(
            cc=note_req.cc,
            examen=note_req.examen,
            tp=note_req.tp
        )
    
    try:
        # Construire le chemin du module en tenant compte du parcours
        module_path = payload.module_id
        if payload.parcours:
            module_path = f"{payload.parcours}/{payload.module_id}"
        
        resultat = calculateur.calculer_module_with_parcours(
            payload.niveau,
            payload.semestre,
            payload.parcours,
            payload.module_id,
            notes_matieres
        )
        
        return {
            "module": resultat.nom,
            "moyenne": resultat.moyenne,
            "valide": resultat.valide,
            "niveau": resultat.niveau,
            "semestre": resultat.semestre,
            "parcours": payload.parcours,
            "matieres": [
                {
                    "nom": m.nom,
                    "moyenne": m.moyenne,
                    "valide": m.valide,
                    "coefficient": m.coefficient,
                    "notes": {
                        "cc": m.notes.cc,
                        "examen": m.notes.examen,
                        "tp": m.notes.tp
                    }
                }
                for m in resultat.matieres
            ]
        }
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Module ou matière non trouvé: {e}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/grades/calculate-all", tags=["Notes"])
async def calculate_all_grades(payload: AllModulesGradesRequest) -> dict:
    """Calcule les notes pour tous les modules."""
    calculateur = CalculateurNotes()
    
    # Convertir les notes en format interne
    notes_par_module = {}
    for module_id, notes_dict in payload.notes.items():
        notes_matieres = {}
        for nom_matiere, note_req in notes_dict.items():
            notes_matieres[nom_matiere] = NoteMatiere(
                cc=note_req.cc,
                examen=note_req.examen,
                tp=note_req.tp
            )
        notes_par_module[module_id] = notes_matieres
    
    try:
        resultats = calculateur.calculer_tous_modules(notes_par_module)
        rapport = generer_rapport(resultats)
        
        return {
            "rapport": rapport,
            "resultats": {
                niveau: [
                    {
                        "module": r.nom,
                        "moyenne": r.moyenne,
                        "valide": r.valide,
                        "semestre": r.semestre,
                        "matieres": [
                            {
                                "nom": m.nom,
                                "moyenne": m.moyenne,
                                "valide": m.valide,
                                "coefficient": m.coefficient
                            }
                            for m in r.matieres
                        ]
                    }
                    for r in modules
                ]
                for niveau, modules in resultats.items()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul: {e}")
