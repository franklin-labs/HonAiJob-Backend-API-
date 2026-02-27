from typing import List, Optional, Any
from pydantic import BaseModel, HttpUrl
from datetime import datetime

class JobOfferBase(BaseModel):
    title: str
    company_name: str
    location: str
    description: str
    url: str
    source_site: str
    published_at: datetime
    sector: Optional[str] = None
    contract_type: Optional[str] = None
    salary_estimate: Optional[str] = None

class JobOfferResponse(JobOfferBase):
    id: int
    collected_at: datetime
    is_obsolete: bool
    company_context: Optional[str] = None
    relevance_score: float
    market_trend_data: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

class JobOfferFilter(BaseModel):
    sector: Optional[str] = None
    location: Optional[str] = None
    min_relevance: Optional[float] = 0.5
    search_query: Optional[str] = None
