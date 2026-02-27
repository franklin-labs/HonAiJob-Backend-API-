from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# Création de l'engine SQLAlchemy
engine = create_engine(
    settings.DATABASE_URL,
    # Nécessaire pour SQLite, peut être retiré pour PostgreSQL
    # connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Configuration de la session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Fournit une session de base de données asynchrone pour l'injection de dépendances.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
