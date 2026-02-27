from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class CV(Base):
    """
    Modèle SQLAlchemy pour la table 'cv'.
    """
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.id"))
    
    project_id = Column(Integer, ForeignKey("project.id"), nullable=True)
    
    owner = relationship("User", back_populates="cvs")
    project = relationship("Project", back_populates="cvs")
