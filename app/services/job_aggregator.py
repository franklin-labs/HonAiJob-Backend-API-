import asyncio
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import delete
from app.models.sqlalchemy_job_offer import JobOffer
from app.core.config import settings
from agno.tools.duckduckgo import DuckDuckGo
from agno.tools.wikipedia import WikipediaTools
from crawl4ai import AsyncWebCrawler
import logging

# Configuration de la journalisation
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobAggregatorService:
    """
    Service d'agrégation proactive utilisant DuckDuckGo News et WikipediaTools.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.ddg = DuckDuckGo(search=True)
        self.wikipedia = WikipediaTools()
        self.sites_to_crawl = [
            "https://www.linkedin.com/jobs",
            "https://www.indeed.com",
            "https://www.welcometothejungle.com/fr/jobs"
        ]

    async def run_daily_crawl(self):
        """
        Exécute la collecte quotidienne, l'enrichissement et le nettoyage.
        """
        logger.info("Démarrage du crawl quotidien des offres d'emploi...")
        
        # 1. Nettoyage des offres obsolètes (> 15 jours)
        await self.cleanup_obsolete_offers()
        
        # 2. Collecte proactive par site
        async with AsyncWebCrawler() as crawler:
            for site in self.sites_to_crawl:
                try:
                    # Simulation de crawl4ai pour extraction structurée
                    # (Dans une implémentation réelle, on utiliserait crawler.arun(site))
                    raw_offers = await self._crawl_site(crawler, site)
                    
                    for offer_data in raw_offers:
                        if await self._is_valid_offer(offer_data):
                            # 3. Enrichissement via Brave & Wikipedia
                            enriched_data = await self._enrich_offer_data(offer_data)
                            
                            # 4. Sauvegarde en DB
                            await self._save_job_offer(enriched_data)
                            
                except Exception as e:
                    logger.error(f"Erreur lors du crawl de {site}: {str(e)}")

    async def cleanup_obsolete_offers(self):
        """
        Supprime les offres de plus de 15 jours.
        """
        fifteen_days_ago = datetime.utcnow() - timedelta(days=15)
        stmt = delete(JobOffer).where(JobOffer.published_at < fifteen_days_ago)
        self.db.execute(stmt)
        self.db.commit()
        logger.info(f"Offres obsolètes supprimées (plus de 15 jours).")

    async def _crawl_site(self, crawler, url: str) -> List[Dict]:
        """
        Utilise crawl4ai pour extraire les offres structurées d'un site.
        """
        # Simulation d'extraction intelligente crawl4ai
        # result = await crawler.arun(url=url, bypass_cache=True)
        # return result.extracted_content
        return [] # À implémenter avec les règles de scraping réelles

    async def _is_valid_offer(self, offer: Dict) -> bool:
        """
        Vérifie la validité (URL, champs obligatoires, date < 15 jours).
        """
        if not offer.get("url") or not offer.get("title") or not offer.get("company_name"):
            return False
            
        published_at = offer.get("published_at")
        if published_at:
            if datetime.utcnow() - published_at > timedelta(days=15):
                return False
        return True

    async def _enrich_offer_data(self, offer: Dict) -> Dict:
        """
        Enrichit les données avec DuckDuckGo et Wikipedia.
        """
        company = offer["company_name"]
        
        # Contexte Wikipedia (Secteur d'activité, histoire)
        wiki_info = self.wikipedia.search(company)
        offer["company_context"] = wiki_info if wiki_info else "Information non disponible"
        
        # Actualités via DuckDuckGo
        news = self.ddg.news(f"Actualités recrutement {company}")
        offer["market_trend_data"] = {"news": news}
            
        # Calcul du score de pertinence prédictif (simple simulation)
        offer["relevance_score"] = self._calculate_predictive_score(offer)
        
        return offer

    def _calculate_predictive_score(self, offer: Dict) -> float:
        """
        Moteur de matching prédictif basé sur les tendances du marché.
        """
        score = 0.5 # Score de base
        # Logique simplifiée : Secteurs en croissance (ex: Tech, Santé)
        growth_sectors = ["Tech", "Informatique", "Data", "IA", "Santé"]
        if any(s in offer.get("sector", "") for s in growth_sectors):
            score += 0.3
            
        # Bonus pour la fraîcheur
        if offer.get("published_at"):
            days_old = (datetime.utcnow() - offer["published_at"]).days
            score += (15 - days_old) * 0.01
            
        return min(score, 1.0)

    async def _save_job_offer(self, data: Dict):
        """
        Sauvegarde ou met à jour l'offre en base de données.
        """
        existing = self.db.query(JobOffer).filter(JobOffer.external_id == data.get("external_id")).first()
        if not existing:
            new_offer = JobOffer(**data)
            self.db.add(new_offer)
            self.db.commit()
            logger.info(f"Nouvelle offre ajoutée : {data['title']} chez {data['company_name']}")
