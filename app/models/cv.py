from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CVBase(BaseModel):
    title: str
    content: str  # JSON or text content
    user_id: int

class CVCreate(CVBase):
    pass

class CVUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class CVInDBBase(CVBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CV(CVInDBBase):
    pass
