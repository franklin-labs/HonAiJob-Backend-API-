from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.sqlalchemy_cv import CV
from app.models.cv import CVCreate, CVUpdate

class CVService:
    """
    Service pour la gestion des CV.
    """
    
    @staticmethod
    def get_cvs(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[CV]:
        return db.query(CV).filter(CV.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_cv(db: Session, cv_id: int, user_id: int) -> Optional[CV]:
        return db.query(CV).filter(CV.id == cv_id, CV.user_id == user_id).first()

    @staticmethod
    def create_cv(db: Session, cv_in: CVCreate) -> CV:
        db_cv = CV(**cv_in.model_dump())
        db.add(db_cv)
        db.commit()
        db.refresh(db_cv)
        return db_cv

    @staticmethod
    def update_cv(db: Session, db_cv: CV, cv_in: CVUpdate) -> CV:
        update_data = cv_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_cv, field, value)
        db.add(db_cv)
        db.commit()
        db.refresh(db_cv)
        return db_cv

    @staticmethod
    def delete_cv(db: Session, db_cv: CV) -> CV:
        db.delete(db_cv)
        db.commit()
        return db_cv
