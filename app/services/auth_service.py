from typing import Optional
from sqlalchemy.orm import Session
from app.models.sqlalchemy_user import User
from app.models.user import UserCreate
from app.core.security import get_password_hash, verify_password

class AuthService:
    """
    Service gérant l'authentification et la création d'utilisateurs.
    """
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_google_id(db: Session, google_id: str) -> Optional[User]:
        return db.query(User).filter(User.google_id == google_id).first()

    @staticmethod
    def create_user(db: Session, user_in: UserCreate) -> User:
        hashed_password = None
        if user_in.password:
            hashed_password = get_password_hash(user_in.password)
            
        db_user = User(
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=hashed_password,
            google_id=user_in.google_id,
            is_active=True
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> Optional[User]:
        user = AuthService.get_user_by_email(db, email)
        if not user or not user.hashed_password:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
