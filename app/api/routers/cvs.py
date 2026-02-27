from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
from app.db.session import get_db
from app.api.deps import get_current_active_user
from app.models.sqlalchemy_user import User
from app.models.cv import CV, CVCreate, CVUpdate
from app.services.cv_service import CVService

router = APIRouter()

@router.get("/", response_model=List[CV])
def read_cvs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Récupérer tous les CV de l'utilisateur.
    """
    return CVService.get_cvs(db, user_id=current_user.id, skip=skip, limit=limit)

@router.post("/", response_model=CV)
def create_cv(
    *,
    db: Session = Depends(get_db),
    cv_in: CVCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Créer un nouveau CV.
    """
    cv_in.user_id = current_user.id
    return CVService.create_cv(db, cv_in=cv_in)

@router.get("/{cv_id}", response_model=CV)
def read_cv(
    *,
    db: Session = Depends(get_db),
    cv_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Récupérer un CV spécifique par ID.
    """
    cv = CVService.get_cv(db, cv_id=cv_id, user_id=current_user.id)
    if not cv:
        raise HTTPException(status_code=404, detail="CV non trouvé")
    return cv

@router.put("/{cv_id}", response_model=CV)
def update_cv(
    *,
    db: Session = Depends(get_db),
    cv_id: int,
    cv_in: CVUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Mettre à jour un CV.
    """
    cv = CVService.get_cv(db, cv_id=cv_id, user_id=current_user.id)
    if not cv:
        raise HTTPException(status_code=404, detail="CV non trouvé")
    return CVService.update_cv(db, db_cv=cv, cv_in=cv_in)

@router.delete("/{cv_id}", response_model=CV)
def delete_cv(
    *,
    db: Session = Depends(get_db),
    cv_id: int,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Supprimer un CV.
    """
    cv = CVService.get_cv(db, cv_id=cv_id, user_id=current_user.id)
    if not cv:
        raise HTTPException(status_code=404, detail="CV non trouvé")
    return CVService.delete_cv(db, db_cv=cv)
