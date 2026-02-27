from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.auth_service import AuthService
from app.core.security import create_access_token, create_refresh_token
from app.models.user import UserCreate, User
from pydantic import BaseModel, EmailStr
from typing import Any

router = APIRouter()

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class GoogleAuthRequest(BaseModel):
    id_token: str

@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Authentification classique par email/mot de passe.
    """
    user = AuthService.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }

@router.post("/google", response_model=Token)
def google_auth(
    auth_data: GoogleAuthRequest,
    db: Session = Depends(get_db)
) -> Any:
    """
    Authentification via Google OAuth 2.0.
    Récupère uniquement l'email et l'ID utilisateur.
    """
    # Ici, on devrait normalement vérifier le token avec google-auth
    # Pour l'exemple, on simule la récupération des infos Google
    # email = verify_google_token(auth_data.id_token)
    
    # Simulation:
    google_id = "simulated_google_id"
    email = "user@example.com"
    
    user = AuthService.get_user_by_google_id(db, google_id)
    if not user:
        # Créer l'utilisateur s'il n'existe pas
        user_in = UserCreate(email=email, google_id=google_id, full_name="Google User")
        user = AuthService.create_user(db, user_in)
    
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }
