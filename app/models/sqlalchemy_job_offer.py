from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, Float
from sqlalchemy.sql import func
from app.db.base_class import Base
from datetime import datetime, timedelta

class JobOffer(Base):
    """
    Modèle pour les offres d'emploi agrégées proactivement.
    """
    __tablename__ = "job_offers"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True) # ID du site source (LinkedIn, etc.)
    title = Column(String, index=True)
    company_name = Column(String, index=True)
    location = Column(String, index=True)
    description = Column(Text)
    url = Column(String)
    source_site = Column(String) # LinkedIn, Indeed, etc.
    published_at = Column(DateTime, index=True)
    collected_at = Column(DateTime, default=func.now())
    is_obsolete = Column(Boolean, default=False)
    
    # Données enrichies
    company_context = Column(Text) # Wikipedia/Brave Search info
    sector = Column(String, index=True)
    salary_estimate = Column(String, nullable=True)
    contract_type = Column(String, index=True) # CDI, CDD, etc.
    
    # Matching prédictif
    relevance_score = Column(Float, default=0.0)
    market_trend_data = Column(JSON, nullable=True) # Tendances du secteur au moment de la collecte

    @property
    def is_fresh(self) -> bool:
        """Vérifie si l'offre a moins de 15 jours."""
        if not self.published_at:
            return False
        return datetime.utcnow() - self.published_at < timedelta(days=15)

    def mark_as_obsolete(self):
        self.is_obsolete = True
