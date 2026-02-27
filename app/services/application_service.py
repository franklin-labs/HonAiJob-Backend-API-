from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.sqlalchemy_application import Application
from app.models.application import ApplicationCreate, ApplicationUpdate

class ApplicationService:
    @staticmethod
    def get_applications(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Application]:
        return db.query(Application).filter(Application.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_application(db: Session, application_id: int, user_id: int) -> Optional[Application]:
        return db.query(Application).filter(Application.id == application_id, Application.user_id == user_id).first()

    @staticmethod
    def create_application(db: Session, application_in: ApplicationCreate, user_id: int) -> Application:
        db_application = Application(**application_in.model_dump(), user_id=user_id)
        db.add(db_application)
        db.commit()
        db.refresh(db_application)
        return db_application

    @staticmethod
    def update_application(db: Session, db_application: Application, application_in: ApplicationUpdate) -> Application:
        update_data = application_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_application, field, value)
        db.add(db_application)
        db.commit()
        db.refresh(db_application)
        return db_application

    @staticmethod
    def delete_application(db: Session, db_application: Application) -> Application:
        db.delete(db_application)
        db.commit()
        return db_application
