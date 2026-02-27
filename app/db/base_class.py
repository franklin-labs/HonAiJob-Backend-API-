from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    """
    Classe de base pour tous les modèles SQLAlchemy.
    """
    id: Any
    __name__: str
    
    # Génère automatiquement le nom de la table en minuscules
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
