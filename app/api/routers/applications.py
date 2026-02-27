from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
from app.db.session import get_db
from app.api.deps import get_current_active_user
from app.models.sqlalchemy_user import User
from app.models.application import Application, ApplicationCreate, ApplicationUpdate
from app.services.application_service import ApplicationService

router = APIRouter()

@router.get("/", response_model=List[Application])
def read_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    return ApplicationService.get_applications(db, user_id=current_user.id, skip=skip, limit=limit)

@router.post("/", response_model=Application)
def create_application(
    *,
    db: Session = Depends(get_db),
    application_in: ApplicationCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    return ApplicationService.create_application(db, application_in=application_in, user_id=current_user.id)

@router.get("/{application_id}", response_model=Application)
def read_application(
    *,
    db: Session = Depends(get_db),
    application_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    application = ApplicationService.get_application(db, application_id=application_id, user_id=current_user.id)
    if not application:
        raise HTTPException(status_code=404, detail="Candidature non trouvée")
    return application

@router.patch("/{application_id}", response_model=Application)
def update_application(
    *,
    db: Session = Depends(get_db),
    application_id: int,
    application_in: ApplicationUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    application = ApplicationService.get_application(db, application_id=application_id, user_id=current_user.id)
    if not application:
        raise HTTPException(status_code=404, detail="Candidature non trouvée")
    return ApplicationService.update_application(db, db_application=application, application_in=application_in)

@router.delete("/{application_id}", response_model=Application)
def delete_application(
    *,
    db: Session = Depends(get_db),
    application_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    application = ApplicationService.get_application(db, application_id=application_id, user_id=current_user.id)
    if not application:
        raise HTTPException(status_code=404, detail="Candidature non trouvée")
    return ApplicationService.delete_application(db, db_application=application)
