from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user
from app.models.sqlalchemy_user import User
from app.models.sqlalchemy_job_offer import JobOffer
from app.schemas.job_offer import JobOfferResponse, JobOfferFilter
from app.services.job_aggregator import JobAggregatorService
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/", response_model=List[JobOfferResponse])
def get_fresh_offers(
    db: Session = Depends(get_db),
    sector: Optional[str] = None,
    location: Optional[str] = None,
    min_relevance: float = 0.5,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Récupère les offres fraîches agrégées proactivement avec filtres.
    """
    query = db.query(JobOffer).filter(JobOffer.is_obsolete == False)
    
    if sector:
        query = query.filter(JobOffer.sector.ilike(f"%{sector}%"))
    if location:
        query = query.filter(JobOffer.location.ilike(f"%{location}%"))
    
    # Tri par pertinence (matching prédictif) et date de publication
    offers = query.filter(JobOffer.relevance_score >= min_relevance)\
                  .order_by(JobOffer.relevance_score.desc(), JobOffer.published_at.desc())\
                  .offset(skip).limit(limit).all()
    return offers

@router.post("/trigger-crawl")
async def trigger_proactive_crawl(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Lance une collecte proactive en arrière-plan (nécessite des droits admin ou simulé ici).
    """
    aggregator = JobAggregatorService(db)
    background_tasks.add_task(aggregator.run_daily_crawl)
    return {"message": "Collecte proactive lancée en arrière-plan."}

@router.delete("/cleanup-obsolete")
async def cleanup_obsolete_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Supprime manuellement les offres de plus de 15 jours.
    """
    aggregator = JobAggregatorService(db)
    await aggregator.cleanup_obsolete_offers()
    return {"message": "Nettoyage des données obsolètes terminé."}

@router.get("/{offer_id}", response_model=JobOfferResponse)
def get_offer_detail(
    offer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Détail d'une offre agrégée avec contexte enrichi.
    """
    offer = db.query(JobOffer).filter(JobOffer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offre non trouvée")
    return offer
