from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base_class import Base

class ApplicationStatus(str, enum.Enum):
    in_progress = "in_progress"
    interview = "interview"
    offer = "offer"
    rejected = "rejected"

class Application(Base):
    """
    Modèle SQLAlchemy pour la table 'application'.
    """
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, index=True, nullable=False)
    role = Column(String, index=True, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(SqlEnum(ApplicationStatus), default=ApplicationStatus.in_progress)
    
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=True)
    cv_id = Column(Integer, ForeignKey("cv.id"), nullable=True)
    
    project = relationship("Project", back_populates="applications")
    cv = relationship("CV")
