from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.sqlalchemy_project import Project
from app.models.project import ProjectCreate, ProjectUpdate

class ProjectService:
    @staticmethod
    def get_projects(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        return db.query(Project).filter(Project.user_id == user_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_project(db: Session, project_id: int, user_id: int) -> Optional[Project]:
        return db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()

    @staticmethod
    def create_project(db: Session, project_in: ProjectCreate, user_id: int) -> Project:
        db_project = Project(**project_in.model_dump(), user_id=user_id)
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project

    @staticmethod
    def update_project(db: Session, db_project: Project, project_in: ProjectUpdate) -> Project:
        update_data = project_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_project, field, value)
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project

    @staticmethod
    def delete_project(db: Session, db_project: Project) -> Project:
        db.delete(db_project)
        db.commit()
        return db_project
