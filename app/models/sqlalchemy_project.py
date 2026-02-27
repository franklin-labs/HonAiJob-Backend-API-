from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Project(Base):
    """
    Modèle SQLAlchemy pour la table 'project'.
    """
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    
    owner = relationship("User", back_populates="projects")
    cvs = relationship("CV", back_populates="project", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="project", cascade="all, delete-orphan")
