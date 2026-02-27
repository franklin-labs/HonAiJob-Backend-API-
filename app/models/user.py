from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    """
    Modèle de base pour l'utilisateur.
    """
    email: EmailStr
    is_active: bool = True
    full_name: Optional[str] = None

class UserCreate(UserBase):
    """
    Modèle pour la création d'un utilisateur.
    """
    password: Optional[str] = None
    google_id: Optional[str] = None

class UserUpdate(UserBase):
    """
    Modèle pour la mise à jour d'un utilisateur.
    """
    password: Optional[str] = None

class UserInDBBase(UserBase):
    """
    Modèle représentant un utilisateur dans la base de données.
    """
    id: int
    model_config = ConfigDict(from_attributes=True)

class User(UserInDBBase):
    """
    Modèle utilisateur public retourné par l'API.
    """
    pass

class UserInDB(UserInDBBase):
    """
    Modèle utilisateur complet avec mot de passe haché.
    """
    hashed_password: Optional[str] = None
