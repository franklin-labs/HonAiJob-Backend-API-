from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.api import api_router
from app.db.base import Base
from app.db.session import engine

# Créer les tables au démarrage (pour le développement)
# Dans un environnement de production, utilisez Alembic pour les migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Backend de l'application HonaiJob avec architecture multi-agents Agno.",
    version="1.0.0",
)

# Configuration CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Inclure les routes
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    """
    Point d'entrée de l'API.
    """
    return {"message": "Bienvenue sur l'API HonaiJob", "status": "operational"}
