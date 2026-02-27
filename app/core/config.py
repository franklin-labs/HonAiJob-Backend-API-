from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Configuration de l'application.
    """
    PROJECT_NAME: str = "HonaiJob Backend"
    API_V1_STR: str = "/api/v1"
    
    # Sécurité
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-for-jwt")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Base de données
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/honaijob")
    
    # Google OAuth
    GOOGLE_CLIENT_ID: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")
    
    # Agno (Phi) Configuration
    AGNO_API_KEY: Optional[str] = os.getenv("AGNO_API_KEY")

    # Groq API Key
    GROQ_API_KEY: str = ""
    
    # Models Configuration
    ORCHESTRATOR_MODEL: str = "llama-3.3-70b-versatile"
    SEARCH_MODEL: str = "llama-3.1-8b-instant"
    ANALYSIS_MODEL: str = "mixtral-8x7b-32768"
    VERIFIER_MODEL: str = "llama-3.3-70b-versatile"
    
    class Config:
        case_sensitive = True

settings = Settings()
